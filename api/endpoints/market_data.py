# goquant_assignment/api/endpoints/market_data.py

from fastapi import APIRouter, HTTPException, Path
# Corrected import: We specify the full path from the project root,
# which is possible because of the path correction in api/main.py.
from data_sources import coingecko

# Create an APIRouter instance. We will add our routes to this.
# This helps organize endpoints into separate files.
router = APIRouter()

@router.get("/price/{token_id}", tags=["Market Data"])
def get_token_price(
    # We use Path() for more detailed validation and documentation of the URL parameter.
    token_id: str = Path(..., 
                         title="Token ID", 
                         description="The CoinGecko ID of the token (e.g., 'ethereum')",
                         example="bitcoin")
):
    """
    Provides the current price of a specified cryptocurrency in USD.
    This endpoint calls our internal coingecko data source module to fetch the data,
    then formats it as a JSON response.
    """
    try:
        # Call the get_price function from our data_sources module.
        # This separation of concerns keeps our API layer clean.
        price = coingecko.get_price(token_id)
        
        # FastAPI automatically converts this dictionary to JSON.
        return {"token": token_id, "currency": "usd", "price": price}
        
    except ValueError as e:
        # If coingecko.get_price raises a ValueError (e.g., token not found),
        # we catch it and return a user-friendly 404 Not Found error.
        raise HTTPException(status_code=404, detail=str(e))
        
    except Exception as e:
        # This is a general catch-all for other errors, like a network failure
        # when calling the CoinGecko API. We return a 503 Service Unavailable error.
        raise HTTPException(status_code=503, detail=f"External API error: {e}")
