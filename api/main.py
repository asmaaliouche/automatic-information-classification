import pandas as pd
from fastapi import FastAPI, HTTPException

from src.api_schemas import EmployeeData, PredictionResponse
from src.modeling import load_model

app = FastAPI(
    title="TechNova Attrition API",
    description="API exposing a Machine Learning model for employee attrition prediction.",
    version="1.0.0"
)

# Global variables for model storage
MODEL = None
PREPROCESSOR = None
MODEL_PATH = 'models/model_pipeline.joblib'

@app.on_event("startup")
def startup_event():
    """Load model and preprocessor on startup."""
    global MODEL, PREPROCESSOR
    try:
        MODEL, PREPROCESSOR = load_model(MODEL_PATH)
        print("✅ Model loaded successfully.")
    except Exception as e:
        print(f"❌ Error loading model: {e}")

@app.get("/")
def read_root():
    if MODEL is None:
        return {"status": "error", "message": "Model not loaded. Please export the model first."}
    return {"status": "ok", "message": "TechNova API is live and model is loaded."}

@app.post("/predict", response_model=PredictionResponse)
def predict(data: EmployeeData):
    if MODEL is None or PREPROCESSOR is None:
        raise HTTPException(status_code=503, detail="Model currently unavailable.")

    try:
        # 1. Convert input data to DataFrame
        input_dict = data.dict()
        input_df = pd.DataFrame([input_dict])
        
        # 2. Transform data using the exported preprocessor
        X_processed = PREPROCESSOR.transform(input_df)
        
        # 3. Make prediction
        prediction = int(MODEL.predict(X_processed)[0])
        probability = float(MODEL.predict_proba(X_processed)[0][1])
        
        return PredictionResponse(
            prediction=prediction,
            probability=probability,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
