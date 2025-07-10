# goquant_assignment/api/endpoints/recommendations.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.recommendation_service import generate_recommendations
from typing import Dict, Any

router = APIRouter()

# Define the structure of the data we expect to receive.
class RecommendationRequest(BaseModel):
    risk_score: int
    volatility_forecast: Dict[str, Any]
    liquidity_forecast: Dict[str, Any]
    governance_prediction: Dict[str, Any]

@router.post("/generate-recommendations", tags=["Execution Guidance"])
def get_recommendations(request: RecommendationRequest):
    """
    Accepts model outputs and generates actionable trading recommendations.
    """
    try:
        recs = generate_recommendations(
            risk_score=request.risk_score,
            volatility_forecast=request.volatility_forecast,
            liquidity_forecast=request.liquidity_forecast,
            governance_prediction=request.governance_prediction
        )
        return recs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")