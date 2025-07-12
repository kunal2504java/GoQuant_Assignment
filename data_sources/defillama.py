# goquant_assignment/data_sources/defillama.py

import requests
from typing import List, Dict, Any

API_URL = "https://api.llama.fi/protocol/{slug}"

def get_protocol_tvl(protocol_slug: str) -> float:
    print(f"Fetching TVL for protocol slug: '{protocol_slug}'...")
    formatted_url = API_URL.format(slug=protocol_slug)
    try:
        # Increased timeout from 10 to 20 seconds.
        response = requests.get(formatted_url, timeout=20)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise TypeError(f"API response for '{protocol_slug}' was not a dictionary.")
        tvl_data = data.get('tvl')
        if tvl_data is None:
            raise KeyError(f"'tvl' key not found for slug '{protocol_slug}'.")
        current_tvl = 0.0
        if isinstance(tvl_data, (int, float)):
            current_tvl = tvl_data
        elif isinstance(tvl_data, list):
            if not tvl_data:
                raise ValueError(f"TVL data for '{protocol_slug}' was an empty list.")
            latest_datapoint = tvl_data[-1]
            if not isinstance(latest_datapoint, dict):
                raise TypeError(f"Latest TVL datapoint for '{protocol_slug}' was not a dictionary.")
            if 'totalLiquidityUSD' not in latest_datapoint:
                raise KeyError(f"'totalLiquidityUSD' key not found in the latest TVL datapoint.")
            current_tvl = latest_datapoint['totalLiquidityUSD']
        else:
            raise TypeError(f"TVL data for '{protocol_slug}' has an unexpected type: {type(tvl_data)}")
        if not isinstance(current_tvl, (int, float)):
            raise TypeError(f"Final parsed TVL for '{protocol_slug}' was not a number.")
        return float(current_tvl)
    except requests.exceptions.RequestException as e:
        print(f"ERROR calling DeFi Llama API: {e}")
        raise ValueError(f"Could not fetch current TVL for '{protocol_slug}'. Reason: {e}") from e


def get_historical_tvl(protocol_slug: str) -> List[Dict[str, Any]]:
    print(f"\n--- Fetching historical TVL for protocol slug: '{protocol_slug}' ---")
    formatted_url = API_URL.format(slug=protocol_slug)
    try:
        # Increased timeout from 10 to 20 seconds.
        response = requests.get(formatted_url, timeout=20)
        response.raise_for_status()
        data = response.json()
        tvl_data = data.get('tvl')
        if not isinstance(tvl_data, list) or not tvl_data:
            raise ValueError(f"Historical TVL data for '{protocol_slug}' is not a valid, non-empty list.")
        print(f"--- Successfully fetched {len(tvl_data)} historical TVL data points ---")
        return tvl_data
    except requests.exceptions.RequestException as e:
        print(f"ERROR calling DeFi Llama Historical API: {e}")
        raise ValueError(f"Could not fetch historical TVL for '{protocol_slug}'. Reason: {e}") from e