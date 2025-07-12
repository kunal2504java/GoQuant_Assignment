# goquant_assignment/models/garch_volatility.py

import pandas as pd
import numpy as np
from arch import arch_model
from typing import List, Dict, Any

def forecast_volatility(
    price_data: List[Dict[str, Any]],
    proposal_body: str,
    forecast_horizon: int = 7
) -> Dict[str, Any]:
    """
    Fits a GARCH(1,1) model with or without an external regressor (GARCH-X), depending on proposal_body.
    Robustly handles cases where exogenous variables are not needed.
    """
    print("\n--- RUNNING LATEST GARCH MODEL CODE (v9 - EXOG ROBUST FIX) ---")

    # 1. Convert price data to a pandas DataFrame.
    df = pd.DataFrame(price_data, columns=['timestamp', 'price'])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df.set_index('date')

    # 2. Calculate daily returns.
    returns = 100 * df['price'].pct_change().dropna()

    if len(returns) < 20:
        raise ValueError("Not enough historical data to calculate returns for GARCH model.")

    # --- Feature Engineering ---
    use_exog = bool(proposal_body and proposal_body.strip())
    if use_exog:
        proposal_impact_feature = np.log(len(proposal_body) + 1)
        exog_regressor = pd.DataFrame({'proposal_impact': np.full(len(returns), proposal_impact_feature)}, index=returns.index)
        print(f"Created proposal impact feature with value: {proposal_impact_feature:.2f}")
        print(f"returns.shape: {returns.shape}, exog_regressor.shape: {exog_regressor.shape}")
        print(f"returns.index.equals(exog_regressor.index): {returns.index.equals(exog_regressor.index)}")
        print(f"exog_regressor.head():\n{exog_regressor.head()}")
        # 3. Define and fit the GARCH-X model.
        model = arch_model(returns, x=exog_regressor, vol='Garch', p=1, q=1, dist='Normal')
        results = model.fit(update_freq=0, disp="off")
        print("--- GARCH-X model fitting complete ---")
        # 4. Forecast future volatility with robust index handling.
        last_date = returns.index[-1]
        forecast_index = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_horizon)
        future_exog_df = pd.DataFrame({'proposal_impact': [proposal_impact_feature] * forecast_horizon}, index=forecast_index)
        print(f"future_exog_df.shape: {future_exog_df.shape}")
        print(f"future_exog_df.index: {future_exog_df.index}")
        print(f"future_exog_df.head():\n{future_exog_df.head()}")
        forecast = results.forecast(horizon=forecast_horizon, x=future_exog_df)
        model_type = "GARCH-X(1,1)"
    else:
        print("No proposal body provided. Using plain GARCH (no exogenous variables).")
        model = arch_model(returns, vol='Garch', p=1, q=1, dist='Normal')
        results = model.fit(update_freq=0, disp="off")
        print("--- Plain GARCH model fitting complete ---")
        last_date = returns.index[-1]
        forecast_index = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_horizon)
        forecast = results.forecast(horizon=forecast_horizon)
        model_type = "GARCH(1,1)"

    future_variance = forecast.variance.iloc[-1]
    annualized_volatility = np.sqrt(future_variance) * np.sqrt(365)

    print(f"--- Forecasted Annualized Volatility for next {forecast_horizon} days ---")

    return {
        "model_type": model_type,
        "last_known_return": returns.iloc[-1],
        "forecast_horizon_days": forecast_horizon,
        "forecasted_annualized_volatility_percent": annualized_volatility.to_dict()
    }

