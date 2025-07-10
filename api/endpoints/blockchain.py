# goquant_assignment/api/endpoints/blockchain.py

from fastapi import APIRouter, HTTPException, Path
from data_sources import etherscan
from typing import List, Dict, Any

router = APIRouter()

@router.get("/blockchain/transactions/{contract_address}", tags=["Blockchain Data"])
def get_contract_transactions(
    contract_address: str = Path(...,
                                 title="Contract Address",
                                 description="The Ethereum smart contract address.",
                                 example="0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984") # Uniswap Token
) -> List[Dict[str, Any]]:
    """
    Provides a list of the most recent transactions for a given smart contract address.
    """
    try:
        transactions = etherscan.get_latest_transactions(contract_address)
        return transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")