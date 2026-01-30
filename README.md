# TechNova Attrition Analysis

## Overview
Project to identify employee attrition causes at TechNova Partners using HR data and surveys.
This project focuses on structuring a machine learning project and preparing it for deployment in a production-like environment.

## Structure
- `data/`: CSV data files.
- `notebooks/`: 
  - `notebook_1.ipynb`: Data cleaning & merging.
  - `notebook_2.ipynb`: Model training & evaluation.
- `src/`: Core logic (`processing.py`, `modeling.py`, `visualization.py`).
- `api/`: FastAPI server for model serving.

## Setup
### Installation
```bash
poetry install
```

### Running Notebooks
```bash
poetry run jupyter notebook
```

### Running the API
```bash
poetry run uvicorn api.main:app --reload
```

## Version Control
This repository uses Git for version control.
Development follows a feature-based branching strategy to ensure clean history and traceability.

## Key Results
The Logistic Regression model (72% recall) identified Monthly Income, Overtime, and Work-Life Balance as primary attrition drivers.

---

## Code and ML Experimentation Standards

### 1. Code Standards (Python)
- **Formatting**: Code must follow PEP 8 conventions. Use `ruff` for linting.
- **Documentation**: Each function must have a docstring detailing inputs/outputs.
- **Typing**: Use type hints for clarity.

### 2. Testing Standards
- **Coverage**: Critical functions in `src/` tested via `pytest`.
- **Local Execution**: Tests must pass before any push.

### 3. ML Experimentation
- **Reproducibility**: Strict use of `random_state` in all models.
- **Data Management**: Raw data excluded from Git via `.gitignore`.

### 4. CI/CD Pipeline
- **Deployment**: Automatic deployment to Hugging Face Spaces from the `main` branch.
- **Secrets**: Use of `HF_TOKEN` secret configured on GitHub.



