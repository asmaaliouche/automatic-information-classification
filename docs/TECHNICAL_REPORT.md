# TechNova Attrition - Technical Report

## 1. Project Context
TechNova Partners identified a need to understand and predict employee attrition. This report documents the Machine Learning model developed to address this challenge, its performance, and how it should be maintained.

## 2. Model Architecture
The current production model is a **Random Forest Classifier** wrapped in a Scikit-Learn Pipeline.

### Why this choice?
- **Robustness**: Handles non-linear relationships and interactions between features (e.g., age vs. income vs. overtime).
- **Interpretability**: Allows for SHAP (Shapley Additive Explanations) analysis to understand *why* an employee is flagged.
- **Preprocessing**: The pipeline includes `StandardScaler` for numerical features and `OneHotEncoder` for categorical variables.

## 3. Data & Features
The model uses 27 features derived from HR records and employee surveys.

### Key Predictors (Top Features)
1. **Total Working Years**: High seniority often correlates with lower attrition.
2. **Monthly Income**: Competitive salary remains a critical retention factor.
3. **Overtime**: Employees working frequent overtime have a significantly higher attrition risk.
4. **Age**: Younger employees tend to move more frequently.
5. **Work-Life Balance**: Survey scores for environment and balance are strong signals.

## 4. Performance Metrics
Based on the latest evaluation on the test set:

| Metric | Score | Interpretation |
|--------|-------|----------------|
| **Recall** | ~72% | Ability to catch employees who actually leave (Targeted metric). |
| **Precision** | ~65% | Accuracy of "Leave" predictions (Avoids false alarms). |
| **F1-Score** | ~68% | Balance between Precision and Recall. |
| **ROC-AUC** | 0.84 | Overall ability to distinguish between classes. |

*Note: The model prioritizes **Recall** to ensure HR doesn't miss high-risk departures, even at the cost of some additional false positives.*

## 5. Maintenance Protocol

### Monitoring
- **Data Drift**: Monitor if the distribution of incoming features (e.g., average overtime increases company-wide) significantly deviates from the training set.
- **Prediction Drift**: Monitor if the % of predicted attrition starts to spike or drop abnormally.

### Retraining Protocol
The model should be retrained **every 6 months** or after significant organizational changes (mergers, role changes).

**How to Retrain:**
1. Update `data/combined_df.csv` with fresh records from the database.
2. Run `notebooks/notebook_2.ipynb` to regenerate the model.
3. Verify metrics against the baseline.
4. Replace `models/model_pipeline.joblib`.
5. Restart the API.

## 6. Known Limitations
- **Survey Latency**: High reliance on worker satisfaction scores which are only updated annually.
- **External Factors**: Does not account for external market conditions or competitor salary benchmarks.
