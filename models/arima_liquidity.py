# goquant_assignment/models/arima_liquidity.py

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from typing import List, Dict, Any

def forecast_liquidity(tvl_data: List[Dict[str, Any]], forecast_horizon: int = 7) -> Dict[str, Any]:
    """
    Fits an ARIMA(5,1,0) model to historical TVL data and forecasts future TVL.

    Args:
        tvl_data: A list of historical TVL data points from DeFi Llama.
        forecast_horizon: The number of days into the future to forecast.

    Returns:
        A dictionary containing the forecast results.
    """
    print("\n--- Starting ARIMA liquidity forecast ---")

    # 1. Convert the data into a pandas DataFrame.
    df = pd.DataFrame(tvl_data)
    # Convert the 'date' (which is a Unix timestamp) to a proper datetime object.
    df['date'] = pd.to_datetime(df['date'], unit='s')
    df = df.set_index('date')

    # We are interested in the 'totalLiquidityUSD' column.
    series = df['totalLiquidityUSD']

    if len(series) < 20:
        raise ValueError("Not enough historical data to fit the ARIMA model. Need at least 20 data points.")

    print(f"Using {len(series)} data points to fit the model.")

    # 2. Define and fit the ARIMA model.
    # The order (5,1,0) is a common starting point for financial time series:
    # p=5: Autoregressive part (uses 5 previous observations).
    # d=1: Integrated part (uses first-order differencing to make the series stationary).
    # q=0: Moving Average part (not used in this configuration).
    model = ARIMA(series, order=(5, 1, 0))
    results = model.fit()
    print("--- ARIMA model fitting complete ---")
    print(results.summary())

    # 3. Get the forecast for the specified number of days (horizon).
    forecast = results.get_forecast(steps=forecast_horizon)
    
    # Extract the predicted mean values (the actual forecast).
    forecast_values = forecast.predicted_mean
    
    # Extract the confidence intervals to give a range for the forecast.
    confidence_intervals = forecast.conf_int()

    print(f"--- Forecasted TVL for next {forecast_horizon} days ---")
    print(forecast_values)

    # 4. Return a structured dictionary with the results.
    return {
        "model_type": "ARIMA(5,1,0)",
        "forecast_horizon_days": forecast_horizon,
        "last_known_tvl_usd": series.iloc[-1],
        "forecasted_tvl_usd": forecast_values.to_dict(),
        "confidence_interval_lower": confidence_intervals.iloc[:, 0].to_dict(),
        "confidence_interval_upper": confidence_intervals.iloc[:, 1].to_dict(),
    }