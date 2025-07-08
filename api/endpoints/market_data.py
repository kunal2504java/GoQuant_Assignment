# goquant_assignment/api/endpoints/market_data.py

from fastapi import APIRouter, HTTPException, Path
# We now import both of our data source modules.
from data_sources import coingecko, defillama

# Create an APIRouter instance. We'll add our routes to this.
router = APIRouter()


@router.get("/price/{token_id}", tags=["Market Data"])
def get_token_price(
    token_id: str = Path(..., 
                         title="Token ID", 
                         description="The CoinGecko ID of the token (e.g., 'ethereum')",
                         example="bitcoin")
):
    """
    Provides the current price of a specified cryptocurrency in USD.
    """
    try:
        price = coingecko.get_price(token_id)
        return {"token": token_id, "currency": "usd", "price": price}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"External API error: {e}")


# --- NEW ENDPOINT ADDED BELOW ---

@router.get("/tvl/{protocol_slug}", tags=["Market Data"])
def get_protocol_tvl(
    protocol_slug: str = Path(...,
                              title="Protocol Slug",
                              description="The DeFi Llama slug of the protocol (e.g., 'aave')",
                              example="uniswap")
):
    """
    Provides the current Total Value Locked (TVL) of a specified DeFi protocol.
    """
    try:
        # Call the new function from our defillama data source module.
        tvl = defillama.get_protocol_tvl(protocol_slug)
        return {"protocol_slug": protocol_slug, "tvl_usd": tvl}
    except ValueError as e:
        # Handle cases where the protocol is not found.
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Handle other potential errors.
        raise HTTPException(status_code=503, detail=f"External API error: {e}")
