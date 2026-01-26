from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def clean_columns(dfc):
    """
    Clean column names by:
    - Converting to lowercase
    - Replacing spaces with underscores
    - Removing French accents
    
    Parameters:
    -----------
    dfc : pd.DataFrame
        DataFrame with columns to clean
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with cleaned column names
    """
    dfc = dfc.copy()
    dfc.columns = (
        dfc.columns.str.lower()
        .str.replace(" ", "_")
        .str.replace("é|è|ê", "e", regex=True)
        .str.replace("à", "a")
        .str.replace("ç", "c")
    )
    return dfc


def build_preprocessor(num_features, cat_features):
    """
    Builds a scikit-learn preprocessor to prepare data
    before training models.
    
    Parameters:
    -----------
    num_features : list
        List of numeric feature column names
    cat_features : list
        List of categorical feature column names
        
    Returns:
    --------
    ColumnTransformer
        Sklearn preprocessor ready to fit and transform data
    """
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, num_features),
            ("cat", categorical_transformer, cat_features)
        ]
    )

    return preprocessor
