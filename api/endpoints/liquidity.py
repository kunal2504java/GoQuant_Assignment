# goquant_assignment/api/endpoints/liquidity.py

from fastapi import APIRouter, HTTPException, Path, Query
from data_sources import defillama
from models import arima_liquidity

router = APIRouter()

@router.get("/forecast/liquidity/{protocol_slug}", tags=["Predictive Models"])
def get_liquidity_forecast(
    protocol_slug: str = Path(...,
                              title="Protocol Slug",
                              description="The DeFi Llama slug of the protocol (e.g., 'aave')",
                              example="uniswap"),
    horizon: int = Query(7, ge=1, le=30, description="Number of future days to forecast (1-30).")
):
    """
    Forecasts future Total Value Locked (TVL) for a given protocol using an ARIMA model.
    """
    try:
        # Step 1: Fetch historical TVL data.
        historical_data = defillama.get_historical_tvl(protocol_slug)
        
        # Step 2: Pass the data to our ARIMA model service.
        forecast_results = arima_liquidity.forecast_liquidity(historical_data, horizon)
        
        return {
            "protocol_slug": protocol_slug,
            "forecast": forecast_results
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Could not generate forecast: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")
