# goquant_assignment/api/endpoints/risk.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
# --- FIX IS HERE ---
# Instead of importing the whole module, we import the specific function we need.
# This is a more direct and reliable way to handle imports across different folders.
from services.risk_assessment import calculate_risk_score

# Create a new router for risk-assessment endpoints.
router = APIRouter()

# Define the structure of the data we expect to receive in the POST request.
# Pydantic handles all the validation for us.
class ProposalData(BaseModel):
    title: str = Field(..., example="[TEMP CHECK] - Uniswap V4 Upgrade")
    body: str = Field(..., example="This proposal outlines the plan to upgrade...")

@router.post("/assess-proposal", tags=["Risk Assessment"])
def assess_proposal_risk(proposal: ProposalData):
    """
    Accepts proposal data (title and body) and returns a calculated risk score.
    """
    try:
        # Call the imported function directly.
        score = calculate_risk_score(proposal.title, proposal.body)
        return {"proposal_title": proposal.title, "risk_score": score}
    except Exception as e:
        # A general error handler for any unexpected issues in the service.
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")