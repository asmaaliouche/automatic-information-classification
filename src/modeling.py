import os

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, fbeta_score
from sklearn.model_selection import train_test_split


def split_data(X, y, test_size=0.2, random_state=42):
    """
    Split data into training and testing sets.
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)

def train_model(X_train, y_train, model_type='rf', **kwargs):
    """
    Initialize and train a model.
    """
    if model_type == 'rf':
        model = RandomForestClassifier(random_state=42, **kwargs)
    elif model_type == 'logistic':
        model = LogisticRegression(max_iter=1000, random_state=42, **kwargs)
    else:
        raise ValueError(f"Unknown model_type: {model_type}")
        
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_train, y_train, X_test, y_test):
    """
    Evaluate model and print main metrics for both train and test sets.
    """
    from sklearn.metrics import f1_score, precision_score, recall_score
    
    # Predictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    # Scores
    results = {
        "precision_train": precision_score(y_train, y_pred_train, zero_division=0),
        "recall_train": recall_score(y_train, y_pred_train, zero_division=0),
        "f1_train": f1_score(y_train, y_pred_train, zero_division=0),
        "f2_train": fbeta_score(y_train, y_pred_train, beta=2, zero_division=0),
        "precision_test": precision_score(y_test, y_pred_test, zero_division=0),
        "recall_test": recall_score(y_test, y_pred_test, zero_division=0),
        "f1_test": f1_score(y_test, y_pred_test, zero_division=0),
        "f2_test": fbeta_score(y_test, y_pred_test, beta=2, zero_division=0),
    }

    # Print results
    print("=== Confusion matrix (TRAIN) ===")
    print(confusion_matrix(y_train, y_pred_train))

    print("\n=== Confusion matrix (TEST) ===")
    print(confusion_matrix(y_test, y_pred_test))

    print("\n=== Classification report (TEST) ===")
    print(classification_report(y_test, y_pred_test, digits=3, zero_division=0))

    return results

def save_model(model, preprocessor, path='models/model_pipeline.joblib'):
    """Save model and preprocessor."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump({'model': model, 'preprocessor': preprocessor}, path)

def load_model(path='models/model_pipeline.joblib'):
    """Load model and preprocessor."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"No model found at {path}")
    data = joblib.load(path)
    return data['model'], data['preprocessor']
