# goquant_assignment/data_sources/etherscan.py

import requests
import os
from typing import List, Dict, Any

# The base URL for the Etherscan API.
API_URL = "https://api.etherscan.io/api"

# --- IMPORTANT ---
# To use this, you must set an environment variable named 'ETHERSCAN_API_KEY'
# with your API key from etherscan.io.
API_KEY = os.environ.get("ETHERSCAN_API_KEY")

def get_latest_transactions(contract_address: str, count: int = 10) -> List[Dict[str, Any]]:
    """
    Fetches the most recent transactions for a given contract address from Etherscan.

    Args:
        contract_address: The Ethereum address of the smart contract.
        count: The number of recent transactions to fetch.

    Returns:
        A list of transaction dictionaries.
    """
    print(f"\n--- Calling Etherscan API for address: {contract_address} ---")

    if not API_KEY:
        print("--- WARNING: ETHERSCAN_API_KEY environment variable not set. Returning empty list. ---")
        return []

    # Define the parameters for the API request.
    params = {
        "module": "account",
        "action": "txlist",
        "address": contract_address,
        "startblock": 0,
        "endblock": 99999999,
        "page": 1,
        "offset": count,
        "sort": "desc",  # 'desc' gets the most recent transactions
        "apikey": API_KEY,
    }

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()

        # Etherscan returns '1' if the request was successful.
        if data.get("status") != "1":
            print(f"--- ETHERSCAN API ERROR: {data.get('message')} ---")
            print(f"--- Result: {data.get('result')} ---")
            return []
        
        transactions = data.get("result", [])
        print(f"--- Found {len(transactions)} transactions. ---")
        return transactions

    except requests.exceptions.RequestException as e:
        print(f"--- ERROR: Failed to connect to Etherscan API: {e} ---")
        return []