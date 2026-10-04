from typing import Any

from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    features: list[dict[str, Any]] = Field(
        ..., description="List of feature dictionaries for prediction"
    )

class PredictResponse(BaseModel):
    predictions: list[Any] = Field(..., description="List of predicted values")

class RulesResponse(BaseModel):
    rules: list[dict[str, Any]] = Field(..., description="List of extracted association rules")
