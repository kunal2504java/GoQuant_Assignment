# goquant_assignment/data_sources/coingecko.py

import requests

# Define the base URL for the CoinGecko API endpoint we'll be using.
# We use a f-string placeholder {} for the token IDs and currencies.
API_URL = "https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies={}"

def get_price(token_id: str, currency: str = "usd") -> float:
    """
    Fetches the current price of a given token from the CoinGecko API.

    Args:
        token_id: The ID of the token on CoinGecko (e.g., 'ethereum', 'bitcoin').
        currency: The currency to get the price in (e.g., 'usd').

    Returns:
        The price of the token as a float.

    Raises:
        requests.exceptions.RequestException: If the API call fails.
        ValueError: If the token is not found or the response is malformed.
    """
    print(f"Fetching price for '{token_id}' in '{currency}'...")
    
    # Format the URL with the specific token and currency we want.
    formatted_url = API_URL.format(token_id, currency)

    try:
        # Make the GET request to the CoinGecko API.
        response = requests.get(formatted_url, timeout=5)
        # Raise an exception for bad status codes (4xx or 5xx).
        response.raise_for_status()

        data = response.json()
        print(f"Response from CoinGecko: {data}")

        # The response is a dictionary like {'ethereum': {'usd': 3500.0}}.
        # We need to check if the token_id is in the response.
        if token_id not in data or currency not in data[token_id]:
            raise ValueError(f"'{token_id}' or '{currency}' not found in CoinGecko response.")

        # Extract and return the price.
        price = data[token_id][currency]
        return float(price)

    except requests.exceptions.RequestException as e:
        print(f"Error calling CoinGecko API: {e}")
        # Re-raise the exception to be handled by the caller (our API endpoint).
        raise
    except (KeyError, TypeError, ValueError) as e:
        print(f"Error processing CoinGecko response: {e}")
        # Raise a ValueError to be handled by the caller.
        raise ValueError(f"Could not parse price for '{token_id}'.") from e