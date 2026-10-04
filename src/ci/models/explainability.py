from typing import Any

import polars as pl
import shap

from ci.models.churn import ChurnModel

def explain_churn_predictions(model: ChurnModel, X: pl.DataFrame) -> dict[str, Any]:
    features_df = X.drop(["Customer_ID", "InvoiceDate"], strict=False)

    explainer = shap.TreeExplainer(model.model)
    shap_values = explainer.shap_values(features_df.to_numpy())

    if isinstance(shap_values, list):
        vals = shap_values[1]
    else:
        vals = shap_values

    if isinstance(explainer.expected_value, list):
        base_val = explainer.expected_value[1]
    else:
        base_val = explainer.expected_value

    return {
        "shap_values": vals,
        "base_value": base_val,
        "feature_names": features_df.columns,
    }
