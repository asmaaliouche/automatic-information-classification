# TechNova API - User Documentation

## Introduction
The TechNova Attrition API provides real-time access to the employee attrition model. It allows HR systems to query risk levels for specific employees or submit raw data for batch processing.

## Base URL
Local development: `http://127.0.0.1:8000`

---

## Endpoints

### 1. Health Check
`GET /`
Verifies if the API is running and if the Model + Database are correctly connected.

**Response Example:**
```json
{
  "status": "ok",
  "message": "TechNova API is live. Model and database are ready."
}
```

### 2. Predict by Employee ID
`GET /predict/{employee_id}`
Fetches the employee's features from the PostgreSQL database and returns a prediction.

**Parameters:**
- `employee_id` (integer): The unique ID of the employee.

**Success Response:**
```json
{
  "prediction": 1,
  "probability": 0.842,
  "status": "success"
}
```

### 3. Predict from Raw Data
`POST /predict`
Submit an employee's data directly as JSON. Useful for systems not yet integrated into the database.

**Payload Example:**
```json
{
  "age": 41,
  "revenu_mensuel": 5993,
  "heure_supplementaires": 1,
  "statut_marital": "Célibataire",
  "..." : "..."
}
```

### 4. Prediction Logs (Traceability)
`GET /predictions`
Returns the recent history of predictions made through the API.

**Query Parameters:**
- `limit` (default: 50): Number of logs to retrieve.

**Response Example:**
```json
[
  {
    "id": 1,
    "employee_id": 42,
    "prediction": 1,
    "probability": 0.75,
    "created_at": "2026-02-20T14:30:00",
    "input_data": { ... }
  }
]
```

---

## Error Handling

The API uses standard HTTP status codes:
- `200`: Success.
- `400`: Bad request (e.g., malformed input).
- `404`: Employee not found.
- `422`: Validation error (missing required fields).
- `503`: Model not loaded.

## Interactive Documentation
When the API is running, you can access interactive documentation at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
