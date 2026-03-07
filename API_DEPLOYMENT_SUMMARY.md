# API Documentation Summary - TechNova Attrition

## 1. API Status and Documentation

The Machine Learning API is fully functional and ready for deployment. The core logic and serving infrastructure are built using **FastAPI**.

*   **Local Access:** The API can be run locally using `uvicorn api.main:app`.
*   **Interactive Documentation (Swagger UI):** Accessible at `http://127.0.0.1:8000/docs` when running locally. This interface provides a full overview of available endpoints, request schemas, and allowed data types.
*   **Deployment Readiness:** A CI/CD pipeline is configured in `.github/workflows/main.yml` to automate testing and deployment to Hugging Face Spaces.

## 2. API Overview

The API serves a **Random Forest Classifier** trained to predict employee attrition based on 27 features (HR records and employee surveys).

### Key Endpoints:
| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/` | Health check (verifies model & database status) |
| `GET` | `/predict/{id}` | Predict attrition for an employee by their ID from the DB |
| `POST` | `/predict` | Predict attrition from raw JSON feature data |
| `GET` | `/predictions` | Retrieve history of logged predictions for traceability |

## 3. Test Coverage Summary

The API and core logic are validated by a comprehensive suite of tests ensuring robustness and reliability.

*   **Total Project Coverage:** 81%
*   **API Implementation Coverage:** 80% (`api/main.py`)
*   **Core Logic Coverage:** 100% (`src/modeling.py`, `src/api_schemas.py`)

*Detailed breakdown is available in the `COVERAGE_REPORT.txt` file.*

## 4. Technical Rigor

*   **Modern Lifespan Management:** Uses FastAPI's `lifespan` context manager for optimized resource loading (model and preprocessor).
*   **Data Traceability:** Every prediction made via the API is logged into a PostgreSQL database, including input features, model prediction, and probability score.
*   **Automated Quality Control:** The CI/CD pipeline enforces linting (`ruff`) and testing (`pytest`) on every code change.
