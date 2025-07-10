# goquant_assignment/api/endpoints/governance_prediction.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from models import governance_outcome

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
        # Call the prediction function from our model file.
        result = governance_outcome.predict_outcome(proposal.title, proposal.body)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")
