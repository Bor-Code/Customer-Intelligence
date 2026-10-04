from contextlib import asynccontextmanager
from typing import Any

import pandas as pd
from fastapi import FastAPI, HTTPException

from ci.api.schemas import PredictRequest, PredictResponse, RulesResponse
from ci.monitoring.registry import load_registered_model

models: dict[str, Any] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        models["churn"] = load_registered_model("ChurnModel", "Production")
        models["segmentation"] = load_registered_model("RFMSegmentationModel", "Production")
        models["anomaly"] = load_registered_model("AnomalyDetectionModel", "Production")
        models["basket"] = load_registered_model("BasketAnalysisModel", "Production")
    except Exception as e:
        print(f"Warning: Models could not be loaded from MLflow: {e}")
    yield
    models.clear()

app = FastAPI(title="Customer Intelligence API", lifespan=lifespan)

@app.post("/predict/{model_name}", response_model=PredictResponse)
def predict(model_name: str, request: PredictRequest) -> PredictResponse:
    if model_name not in models:
        raise HTTPException(
            status_code=404, detail=f"Model '{model_name}' not found or not loaded."
        )
    if model_name == "basket":
        raise HTTPException(status_code=400, detail="Use /rules/basket for Basket Analysis.")

    try:
        df = pd.DataFrame(request.features)
        preds = models[model_name].predict(df)

        if isinstance(preds, pd.DataFrame):
            preds_list = preds.iloc[:, 0].tolist()
        elif isinstance(preds, pd.Series):
            preds_list = preds.tolist()
        else:
            preds_list = preds.tolist()

        return PredictResponse(predictions=preds_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/rules/basket", response_model=RulesResponse)
def get_basket_rules() -> RulesResponse:
    if "basket" not in models:
        raise HTTPException(status_code=404, detail="Basket model not found or not loaded.")

    try:
        rules_df = models["basket"].predict(pd.DataFrame())
        rules_list = rules_df.to_dict(orient="records")
        return RulesResponse(rules=rules_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
