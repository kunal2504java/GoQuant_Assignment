# goquant_assignment/api/endpoints/governance.py

from fastapi import APIRouter, HTTPException, Path
from data_sources import snapshot
from typing import List, Dict, Any

router = APIRouter()

@router.get("/proposals/{space_id}", tags=["Governance"])
def get_space_proposals(
    space_id: str = Path(...,
                         title="Snapshot Space ID",
                         description="The ENS name of the Snapshot space (e.g., 'aave.eth')",
                         example="uniswap.eth")
) -> List[Dict[str, Any]]:
    """
    Provides a list of the most recent governance proposals for a specified protocol
    from Snapshot.org.
    """
    try:
        # Call the new function from our snapshot data source module.
        proposals = snapshot.get_proposals(space_id)
        return proposals
    except ValueError as e:
        # Handle cases where the space is not found or data is malformed.
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Handle other potential errors.
        raise HTTPException(status_code=503, detail=f"External API error: {e}")