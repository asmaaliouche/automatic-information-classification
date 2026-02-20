from unittest.mock import patch

import numpy as np
import pandas as pd

from src.visualization import (
    plot_confusion_matrix,
    plot_correlation_matrix,
    plot_feature_importance,
)


@patch("matplotlib.pyplot.show")
def test_plot_correlation_matrix(mock_show):
    """Smoke test for correlation matrix plot."""
    df = pd.DataFrame({
        "A": [1, 2, 3],
        "B": [4, 5, 2]
    })
    plot_correlation_matrix(df)
    assert mock_show.called


@patch("matplotlib.pyplot.show")
def test_plot_feature_importance(mock_show):
    """Smoke test for feature importance plot."""
    importances = np.array([0.1, 0.5, 0.4])
    names = ["f1", "f2", "f3"]
    plot_feature_importance(importances, names)
    assert mock_show.called


@patch("matplotlib.pyplot.show")
def test_plot_confusion_matrix(mock_show):
    """Smoke test for confusion matrix plot."""
    cm = np.array([[10, 2], [1, 15]])
    plot_confusion_matrix(cm, labels=["Stay", "Leave"])
    assert mock_show.called
