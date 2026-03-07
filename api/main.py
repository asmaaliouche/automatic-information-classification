import json
from contextlib import asynccontextmanager

import os
import pandas as pd
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session

from db.database import Base, engine, get_db
from db.models import Employee, Prediction
from src.api_schemas import EmployeeData, PredictionResponse
from src.modeling import load_model

# Global variables for model storage
MODEL = None
PREPROCESSOR = None
MODEL_PATH = 'models/model_pipeline.joblib'

# Security configuration
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Security(api_key_header)):
    """Check if the provided API key is valid."""
    expected_key = os.getenv("API_TOKEN", "futurisys-token-debug")
    if api_key == expected_key:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials. Please provide a valid access_token header.",
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model and preprocessor on startup, create tables, and cleanup resources on shutdown."""
    global MODEL, PREPROCESSOR
    try:
        # 1. Create tables if they don't exist (crucial for Docker/HF deployments)
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables confirmed/created.")

        # 2. Load the ML model
        MODEL, PREPROCESSOR = load_model(MODEL_PATH)
        print("✅ Model loaded successfully.")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
    yield
    # No specific cleanup needed for these globals, but handle shutdown if needed
    print("👋 Shutting down API.")


app = FastAPI(
    title="TechNova Attrition API",
    description="API exposing a Machine Learning model for employee attrition prediction.",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
def read_root(db: Session = Depends(get_db)):
    """Health check endpoint — verifies model and database status."""
    model_ok = MODEL is not None and PREPROCESSOR is not None

    # Check database connectivity
    db_ok = False
    try:
        db.execute(
            Employee.__table__.select().limit(1)
        )
        db_ok = True
    except Exception:
        pass

    status = {
        "model_loaded": model_ok,
        "database_connected": db_ok,
    }

    if all(status.values()):
        return {"status": "ok", "message": "TechNova API is live. Model and database are ready."}

    error_messages = []
    if not model_ok:
        error_messages.append("Model not loaded")
    if not db_ok:
        error_messages.append("Database not connected")

    return {"status": "error", "message": ". ".join(error_messages)}


@app.get("/predict/{employee_id}", response_model=PredictionResponse)
def predict_by_id(
    employee_id: int, 
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Make an attrition prediction for a single employee by their ID.
    Reads the employee from the database and logs the prediction.
    """
    if MODEL is None or PREPROCESSOR is None:
        raise HTTPException(status_code=503, detail="Model is not available.")

    try:
        # 1. Query employee from the database
        employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()

        if employee is None:
            raise HTTPException(
                status_code=404, detail=f"Employee with ID {employee_id} not found."
            )

        # 2. Build a DataFrame from the database row (features only)
        feature_cols = [
            c.name for c in Employee.__table__.columns
            if c.name not in ('id', 'a_quitte_l_entreprise', 'attrition_numeric')
        ]
        row_data = {col: getattr(employee, col) for col in feature_cols}

        # Convert heure_supplementaires from string ("Oui"/"Non") to int (1/0)
        ot_map = {'Oui': 1, 'Non': 0}
        if row_data.get('heure_supplementaires') in ot_map:
            row_data['heure_supplementaires'] = ot_map[row_data['heure_supplementaires']]

        input_df = pd.DataFrame([row_data])

        # 3. Transform and predict
        X_processed = PREPROCESSOR.transform(input_df)
        prediction = int(MODEL.predict(X_processed)[0])
        probability = float(MODEL.predict_proba(X_processed)[0][1])

        # 4. Log prediction to database
        pred_log = Prediction(
            employee_id=employee_id,
            input_data=json.dumps(row_data, ensure_ascii=False, default=str),
            prediction=prediction,
            probability=probability,
        )
        db.add(pred_log)
        db.commit()

        return PredictionResponse(
            prediction=prediction,
            probability=probability,
            status="success"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"An error occurred during prediction: {str(e)}"
        )


@app.post("/predict", response_model=PredictionResponse)
def predict(
    data: EmployeeData, 
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Make an attrition prediction from raw input data.
    Logs the prediction input and output to the database.
    """
    if MODEL is None or PREPROCESSOR is None:
        raise HTTPException(status_code=503, detail="Model currently unavailable.")

    try:
        # 1. Convert input data to DataFrame
        input_dict = data.model_dump()
        input_df = pd.DataFrame([input_dict])

        # 2. Transform data using the preprocessor
        X_processed = PREPROCESSOR.transform(input_df)

        # 3. Make prediction
        prediction = int(MODEL.predict(X_processed)[0])
        probability = float(MODEL.predict_proba(X_processed)[0][1])

        # 4. Log prediction to database
        pred_log = Prediction(
            employee_id=int(input_dict.get("employee_id")) if input_dict.get("employee_id") else None,
            input_data=json.dumps(input_dict, ensure_ascii=False, default=str),
            prediction=prediction,
            probability=probability,
        )
        db.add(pred_log)
        db.commit()

        return PredictionResponse(
            prediction=prediction,
            probability=probability,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")


@app.get("/predictions", response_model=list)
def get_predictions(
    limit: int = 50, 
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Retrieve recent prediction logs from the database.
    Provides full traceability of model interactions.
    """
    predictions = (
        db.query(Prediction)
        .order_by(Prediction.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": p.id,
            "employee_id": p.employee_id,
            "prediction": p.prediction,
            "probability": p.probability,
            "created_at": p.created_at.isoformat(),
            "input_data": json.loads(p.input_data),
        }
        for p in predictions
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
