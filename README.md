# Retail Customer Intelligence Platform

A complete end-to-end data engineering and machine learning platform designed for the retail sector.

## Architecture & Tech Stack

- **Data Processing**: Python 3.12, Polars, DuckDB, Pandera.
- **Machine Learning**: scikit-learn, LightGBM, mlxtend, Optuna, SHAP.
- **Orchestration**: Prefect.
- **Monitoring & Deployment**: MLflow, FastAPI, Pydantic, Streamlit, Evidently.
- **Infrastructure**: Docker Compose, GitHub Actions, Makefile.
- **Quality**: ruff, mypy, pytest, pre-commit.

## Capabilities

1. **Segmentation**: RFM extraction + KMeans clustering.
2. **Churn Prediction**: LightGBM + temporal splitting + Optuna hyperparameter tuning + SHAP explainability.
3. **Basket Analysis**: FP-Growth association rules.
4. **Anomaly Detection**: Isolation Forest utilizing return/refund ratios.
5. **API & Dashboard**: Exposes all inferences via FastAPI and visualizes results/data drift via Streamlit & Evidently.

## Quickstart

Use the built-in `Makefile` to quickly set up the project:

```bash
make install
make format
make lint
make test
```

To run the full infrastructure locally:

```bash
make build
make up
```
This spawns the MLflow server (port 5000), FastAPI server (port 8000), and Streamlit dashboard (port 8501).

```bash
make down
```
Shuts down the infrastructure.
