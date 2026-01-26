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

## Standards de Code et d'Expérimentation ML

### 1. Standards de Code (Python)
- **Formatage** : Le code doit suivre les conventions PEP 8. Utilisation de `ruff` pour le linting.
- **Documentation** : Chaque fonction doit avoir un docstring détaillant entrées/sorties.
- **Typage** : Utiliser les "type hints" pour la clarté.

### 2. Standards de Test
- **Couverture** : Fonctions critiques de `src/` testées via `pytest`.
- **Exécution locale** : Les tests doivent passer avant tout push.

### 3. Expérimentation ML
- **Reproductibilité** : Utilisation stricte de `random_state` dans tous les modèles.
- **Gestion des données** : Données brutes exclues de Git via `.gitignore`.

### 4. Pipeline CI/CD
- **Déploiement** : Automatique sur Hugging Face Spaces depuis la branche `main`.
- **Secrets** : Utilisation du secret `HF_TOKEN` configuré sur GitHub.



