# goquant_assignment/api/endpoints/volatility.py

from fastapi import APIRouter, HTTPException, Path, Query
from data_sources import coingecko
from models import garch_volatility

router = APIRouter()

@router.get("/forecast/volatility/{token_id}", tags=["Predictive Models"])
def get_volatility_forecast(
    token_id: str = Path(...,
                         title="Token ID",
                         description="The CoinGecko ID of the token (e.g., 'ethereum')",
                         example="bitcoin"),
    days: int = Query(90, ge=30, le=365, description="Number of past days for historical data (30-365)."),
    horizon: int = Query(7, ge=1, le=30, description="Number of future days to forecast (1-30).")
):
    """
    Forecasts future price volatility for a given token using a GARCH(1,1) model.
    """
    try:
        # Step 1: Fetch historical data from our data source.
        historical_data = coingecko.get_historical_prices(token_id, days)
        
        # Step 2: Pass the data to our GARCH model service.
        forecast_results = garch_volatility.forecast_volatility(historical_data, horizon)
        
        return {
            "token_id": token_id,
            "data_days_used": days,
            "forecast": forecast_results
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Could not generate forecast: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")