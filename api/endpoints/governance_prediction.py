# goquant_assignment/api/endpoints/governance_prediction.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from models import governance_outcome
from typing import List, Dict, Any

router = APIRouter()

class ProposalData(BaseModel):
    title: str = Field(..., example="[TEMP CHECK] - Uniswap V4 Upgrade")
    body: str = Field(..., example="This proposal outlines the plan to upgrade...")

@router.post("/predict/governance-outcome", tags=["Predictive Models"])
def get_governance_prediction(proposal: ProposalData):
    """
    Accepts proposal data and predicts whether it is likely to pass or fail.
    """
    try:
        result = governance_outcome.predict_outcome(proposal.title, proposal.body)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")

# --- NEW ENDPOINT ADDED BELOW ---

@router.get("/analytics/governance-feature-importance", tags=["Model Analytics"])
def get_governance_feature_importance() -> List[Dict[str, Any]]:
    """
    Returns the most influential keywords (features) from the trained
    governance outcome prediction model.
    """
    try:
        importances = governance_outcome.get_feature_importances()
        return importances
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")