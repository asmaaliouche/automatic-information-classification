import os

import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier

from src.modeling import evaluate_model, load_model, save_model, split_data, train_model


def test_split_data():
    """Test data splitting functionality."""
    df = pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'target': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    })
    X = df[['feature1']]
    y = df['target']
    
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2)
    
    assert len(X_train) == 8
    assert len(X_test) == 2


def test_train_model():
    """Test training both supported model types."""
    X = pd.DataFrame({'f1': [1, 2, 3, 4], 'f2': [10, 20, 30, 40]})
    y = pd.Series([0, 1, 0, 1])
    
    # Random Forest
    rf = train_model(X, y, model_type='rf', n_estimators=10)
    assert hasattr(rf, "predict")
    
    # Logistic
    lr = train_model(X, y, model_type='logistic')
    assert hasattr(lr, "predict")
    
    # Invalid type
    with pytest.raises(ValueError, match="Unknown model_type"):
        train_model(X, y, model_type='invalid')


def test_evaluate_model():
    """Test model evaluation returns correct keys."""
    X = pd.DataFrame({'f1': [1, 2], 'f2': [10, 20]})
    y = pd.Series([0, 1])
    rf = train_model(X, y, model_type='rf', n_estimators=10)
    
    results = evaluate_model(rf, X, y, X, y)
    assert "f1_test" in results
    assert "recall_test" in results
    assert 0.0 <= results["f1_test"] <= 1.0


def test_load_model_not_found():
    """Test behavior when model file is missing."""
    with pytest.raises(FileNotFoundError):
        load_model("non_existent_model.joblib")


class DummyPreprocessor:
    def transform(self, X): return X


def test_save_and_load_model(tmp_path):
    """Test saving and then loading a model."""
    d = tmp_path / "models"
    d.mkdir()
    model_path = d / "test_model.joblib"
    
    model = RandomForestClassifier(n_estimators=10)
    model.fit([[1]], [1])
    preprocessor = DummyPreprocessor()
    
    save_model(model, preprocessor, path=str(model_path))
    assert os.path.exists(model_path)
    
    loaded_model, loaded_preprocessor = load_model(path=str(model_path))
    assert isinstance(loaded_model, RandomForestClassifier)
    assert hasattr(loaded_preprocessor, 'transform')
