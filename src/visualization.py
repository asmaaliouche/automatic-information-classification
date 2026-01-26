import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_correlation_matrix(df, numeric_only=True):
    """
    Plot Pearson correlation matrix heatmap.
    """
    plt.figure(figsize=(15, 10))
    corr = df.corr(numeric_only=numeric_only)
    sns.heatmap(corr, annot=False, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Matrix (Pearson)")
    plt.show()

def plot_feature_importance(importances, feature_names, title="Feature Importances", top_n=20):
    """
    Plot feature importance bar chart.
    
    Parameters:
    -----------
    importances : array-like
        The importance values
    feature_names : list
        List of feature names corresponding to indices
    title : str
        Title of the plot
    top_n : int
        Number of top features to show
    """
    indices = np.argsort(importances)[::-1][:top_n]
    
    plt.figure(figsize=(12, 6))
    plt.title(title)
    plt.bar(range(len(indices)), importances[indices], align="center")
    plt.xticks(range(len(indices)), [feature_names[i] for i in indices], rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_confusion_matrix(conf_matrix, labels=None):
    """
    Plot confusion matrix as a heatmap.
    """
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', 
                xticklabels=labels, yticklabels=labels)
    plt.title("Confusion Matrix")
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.show()

def plot_shap_summary(model, X_transformed, feature_names):
    """
    Generate and plot SHAP summary for a tree-based model.
    """
    import shap
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_transformed)
    
    # Handle SHAP output structure (list for multi-class)
    if isinstance(shap_values, list):
        shap_to_plot = shap_values[1]
    else:
        shap_to_plot = shap_values[:, :, 1] if len(shap_values.shape) == 3 else shap_values
        
    shap.summary_plot(shap_to_plot, X_transformed, feature_names=feature_names)
    return explainer, shap_to_plot

def plot_shap_waterfall(explainer, shap_values, X_transformed, feature_names, sample_index):
    """
    Plot SHAP waterfall for a specific sample.
    """
    import shap
    expected_value = explainer.expected_value[1] if isinstance(explainer.expected_value, (list, np.ndarray)) else explainer.expected_value
    
    exp = shap.Explanation(
        values=shap_values[sample_index],
        base_values=expected_value,
        data=X_transformed[sample_index],
        feature_names=feature_names
    )
    shap.plots.waterfall(exp)
