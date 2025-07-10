# goquant_assignment/api/endpoints/risk.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from services.risk_assessment import calculate_multi_factor_risk
from typing import Dict, Any

router = APIRouter()

# Define a more complex data structure for the request body.
# It now expects the full output from our other model endpoints.
class MultiFactorRiskRequest(BaseModel):
    proposal_title: str
    proposal_body: str
    volatility_forecast: Dict[str, Any]
    liquidity_forecast: Dict[str, Any]
    governance_prediction: Dict[str, Any]

@router.post("/assess-risk/multi-factor", tags=["Risk Assessment"])
def assess_multi_factor_risk(request: MultiFactorRiskRequest):
    """
    Accepts proposal data and model forecasts to calculate a multi-factor risk score.
    """
    try:
        # Pass all the data from the request to our upgraded service function.
        score_data = calculate_multi_factor_risk(
            proposal_title=request.proposal_title,
            proposal_body=request.proposal_body,
            volatility_forecast=request.volatility_forecast,
            liquidity_forecast=request.liquidity_forecast,
            governance_prediction=request.governance_prediction
        )
        return score_data
    except Exception as e:
        # Add more detailed error logging for debugging.
        print(f"ERROR in multi-factor risk assessment: {e}")
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")