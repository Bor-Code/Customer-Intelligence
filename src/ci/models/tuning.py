from datetime import timedelta
from typing import Any

import lightgbm as lgb
import optuna
import polars as pl
from numpy.typing import NDArray
from sklearn.metrics import roc_auc_score

def optimize_churn_model(
    X: pl.DataFrame, y: pl.Series | NDArray[Any], n_trials: int = 10, random_state: int = 42
) -> dict[str, Any]:
    if "InvoiceDate" not in X.columns:
        raise ValueError("X must contain 'InvoiceDate' for temporal split.")

    max_date = X["InvoiceDate"].max()
    split_date = max_date - timedelta(days=30)
    is_train = X["InvoiceDate"] <= split_date

    features_df = X.drop(["Customer_ID", "InvoiceDate"], strict=False)
    features = features_df.to_numpy()

    if isinstance(y, pl.Series):
        y_arr = y.to_numpy()
    else:
        y_arr = y

    mask = is_train.to_numpy()
    X_train, y_train = features[mask], y_arr[mask]
    X_test, y_test = features[~mask], y_arr[~mask]

    if len(set(y_test)) < 2:
        return {"learning_rate": 0.1, "num_leaves": 31, "max_depth": -1}

    def objective(trial: optuna.Trial) -> float:
        params = {
            "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.5, log=True),
            "num_leaves": trial.suggest_int("num_leaves", 10, 100),
            "max_depth": trial.suggest_int("max_depth", 3, 10),
            "random_state": random_state,
        }

        model = lgb.LGBMClassifier(**params)
        model.fit(X_train, y_train)

        preds = model.predict_proba(X_test)[:, 1]
        return float(roc_auc_score(y_test, preds))

    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=n_trials)

    return study.best_params
