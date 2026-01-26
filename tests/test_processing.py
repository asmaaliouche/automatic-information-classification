import pandas as pd
from src.processing import clean_columns

def test_clean_columns():
    """
    Testing the function clean_columns :
    1. Convert column names to lowercase
    2. Replace spaces with underscores
    3. Remove accents
    """
    # Test data
    df = pd.DataFrame(columns=["Age Client", "Retraité", "Salaire mensuel"])
    
    # Action
    df_cleaned = clean_columns(df)
    
    expected_columns = ["age_client", "retraite", "salaire_mensuel"]
    assert list(df_cleaned.columns) == expected_columns
    assert isinstance(df_cleaned, pd.DataFrame)
