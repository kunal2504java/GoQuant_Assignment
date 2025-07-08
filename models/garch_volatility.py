# goquant_assignment/models/garch_volatility.py

import pandas as pd
import numpy as np
from arch import arch_model
from typing import List, Dict, Any

def forecast_volatility(price_data: List[Dict[str, Any]], forecast_horizon: int = 7) -> Dict[str, Any]:
    """
    Fits a GARCH(1,1) model to historical price data and forecasts volatility.

    Args:
        price_data: A list of historical price points from CoinGecko.
        forecast_horizon: The number of days into the future to forecast.

    Returns:
        A dictionary containing the forecast results.
    """
    print("\n--- Starting GARCH volatility forecast ---")
    
    # 1. Convert data to a pandas DataFrame for easier manipulation.
    # The price_data is a list of [timestamp, price] pairs.
    df = pd.DataFrame(price_data, columns=['timestamp', 'price'])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df.set_index('date')
    
    # 2. Calculate daily returns. GARCH models work on returns, not prices.
    # We multiply by 100 to express returns as percentages.
    returns = 100 * df['price'].pct_change().dropna()
    
    if returns.empty:
        raise ValueError("Not enough data to calculate returns.")

    print(f"Calculated {len(returns)} daily returns.")

    # 3. Define and fit the GARCH(1,1) model.
    # p=1, q=1 are the standard parameters for a GARCH(1,1) model.
    # 'vol="GARCH"' specifies the model type.
    # 'dist="Normal"' assumes a normal distribution for the errors.
    model = arch_model(returns, vol='Garch', p=1, q=1, dist='Normal')
    
    # 'update_freq=5' tells the model to print progress every 5 iterations.
    # 'disp="off"' turns off the full convergence output.
    results = model.fit(update_freq=5, disp="off")
    print("--- GARCH model fitting complete ---")
    print(results.summary())

    # 4. Forecast future volatility.
    forecast = results.forecast(horizon=forecast_horizon)
    
    # The forecast object contains future variance. We need to convert it to
    # annualized volatility (standard deviation), which is more interpretable.
    # We take the square root of the variance and multiply by the square root
    # of 365 (for daily data) to annualize it.
    # The forecasted variance is in the 'h.1' column for a 1-step ahead forecast.
    future_variance = forecast.variance.iloc[-1]
    annualized_volatility = np.sqrt(future_variance) * np.sqrt(365)
    
    print(f"--- Forecasted Annualized Volatility for next {forecast_horizon} days ---")
    print(annualized_volatility)
    
    # Return a structured dictionary with the results.
    return {
        "model_type": "GARCH(1,1)",
        "last_known_return": returns.iloc[-1],
        "forecast_horizon_days": forecast_horizon,
        "forecasted_annualized_volatility_percent": annualized_volatility.to_dict()
    }
