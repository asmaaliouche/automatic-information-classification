# TechNova Attrition Analysis

## Overview
Project to identify employee attrition causes at TechNova Partners using HR data and surveys.

## Structure
- `data/`: CSV data files.
- `notebooks/`: 
  - `notebook_1.ipynb`: Data cleaning & merging.
  - `notebook_2.ipynb`: Model training & evaluation.
- `src/`: Core logic (`processing.py`, `modeling.py`, `visualization.py`).

## Setup
```bash
poetry install
poetry run jupyter notebook
```

## Key Results
The Logistic Regression model (72% recall) identified Monthly Income, Overtime, and Work-Life Balance as primary attrition drivers.
