import os

import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier

from src.modeling import load_model, save_model, split_data


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
    assert len(y_train) == 8
    assert len(y_test) == 2

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
    
    # Create a dummy model and preprocessor
    model = RandomForestClassifier()
    
    preprocessor = DummyPreprocessor()
    
    # Save
    save_model(model, preprocessor, path=str(model_path))
    assert os.path.exists(model_path)
    
    # Load
    loaded_model, loaded_preprocessor = load_model(path=str(model_path))
    assert isinstance(loaded_model, RandomForestClassifier)
    assert hasattr(loaded_preprocessor, 'transform')
