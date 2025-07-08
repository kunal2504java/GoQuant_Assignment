# goquant_assignment/data_sources/coingecko.py

import requests
from typing import List, Dict, Any

# --- Existing code for current price ---
PRICE_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies={}"

def get_price(token_id: str, currency: str = "usd") -> float:
    # ... (this function remains unchanged)
    print(f"Fetching price for '{token_id}' in '{currency}'...")
    formatted_url = PRICE_API_URL.format(token_id, currency)
    try:
        response = requests.get(formatted_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if token_id not in data or currency not in data[token_id]:
            raise ValueError(f"'{token_id}' or '{currency}' not found in CoinGecko response.")
        price = data[token_id][currency]
        return float(price)
    except requests.exceptions.RequestException as e:
        print(f"Error calling CoinGecko API: {e}")
        raise
    except (KeyError, TypeError, ValueError) as e:
        print(f"Error processing CoinGecko response: {e}")
        raise ValueError(f"Could not parse price for '{token_id}'.") from e


# --- NEW FUNCTION FOR HISTORICAL DATA ---
HISTORICAL_API_URL = "https://api.coingecko.com/api/v3/coins/{}/market_chart?vs_currency={}&days={}&interval=daily"

def get_historical_prices(token_id: str, days: int = 90, currency: str = "usd") -> List[Dict[str, Any]]:
    """
    Fetches historical daily prices for a given token from CoinGecko.

    Args:
        token_id: The ID of the token on CoinGecko (e.g., 'ethereum').
        days: The number of past days of data to fetch.
        currency: The currency for the price data.

    Returns:
        A list of price data points.
    """
    print(f"\n--- Fetching historical prices for '{token_id}' for the last {days} days ---")
    formatted_url = HISTORICAL_API_URL.format(token_id, currency, days)
    
    try:
        response = requests.get(formatted_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # The historical prices are in the 'prices' key.
        prices = data.get('prices')
        if not prices:
            raise ValueError(f"Historical price data not found for '{token_id}'.")
        
        print(f"--- Successfully fetched {len(prices)} historical data points ---")
        return prices

    except requests.exceptions.RequestException as e:
        print(f"Network Error calling CoinGecko historical API: {e}")
        raise
    except (ValueError, KeyError) as e:
        print(f"Error processing CoinGecko historical response: {e}")
        raise ValueError(f"Could not parse historical prices for '{token_id}'.") from e