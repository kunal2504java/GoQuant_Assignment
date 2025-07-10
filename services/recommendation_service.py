# goquant_assignment/services/recommendation_service.py

from typing import Dict, Any, List

def generate_recommendations(
    risk_score: int,
    volatility_forecast: Dict[str, Any],
    liquidity_forecast: Dict[str, Any],
    governance_prediction: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generates trading and risk management recommendations based on model outputs.

    Args:
        risk_score: The final multi-factor risk score.
        volatility_forecast: The output from the GARCH model.
        liquidity_forecast: The output from the ARIMA model.
        governance_prediction: The output from the governance outcome model.

    Returns:
        A dictionary containing actionable recommendations.
    """
    print(f"\n--- Generating recommendations for risk score: {risk_score} ---")
    
    timing_windows: List[str] = []
    rebalancing_recs: List[str] = []
    mitigation_strats: List[str] = []

    # --- Rule-based logic for recommendations ---

    # High-risk scenarios
    if risk_score > 70:
        timing_windows.append("High risk detected. Consider avoiding trades during the upgrade window.")
        timing_windows.append("Optimal Exit Window: T-24h to T-1h before upgrade.")
        rebalancing_recs.append("Reduce exposure to the primary asset by 20-30%.")
        rebalancing_recs.append("Increase allocation to stablecoins or less correlated assets.")
        mitigation_strats.append("Hedge position with perpetual futures (Short).")
        mitigation_strats.append("Purchase out-of-the-money put options for downside protection.")
        mitigation_strats.append("Avoid using high leverage.")

    # Medium-risk scenarios
    elif 40 <= risk_score <= 70:
        timing_windows.append("Medium risk. Proceed with caution.")
        timing_windows.append("Optimal Entry Window: T-48h to T-24h for potential pre-upgrade pump.")
        timing_windows.append("Optimal Exit Window: T+1h to T+6h post-upgrade.")
        rebalancing_recs.append("Consider a minor reduction in exposure (5-10%).")
        rebalancing_recs.append("Monitor correlation with market indices (e.g., ETH, BTC).")
        mitigation_strats.append("Use stop-loss orders to manage downside risk.")
        mitigation_strats.append("Consider using options spreads to define risk.")

    # Low-risk scenarios
    else: # risk_score < 40
        timing_windows.append("Low risk detected. Event may present a trading opportunity.")
        timing_windows.append("Optimal Entry Window: T-72h to T-24h to capture positive sentiment.")
        rebalancing_recs.append("No immediate rebalancing required. Monitor for alpha.")
        rebalancing_recs.append("Consider a small, speculative increase in position size.")
        mitigation_strats.append("Standard portfolio hedging is sufficient.")
        mitigation_strats.append("Monitor social media sentiment for unexpected shifts.")

    # Add specific recommendations based on model outputs
    try:
        first_day_vol = next(iter(volatility_forecast['forecast']['forecasted_annualized_volatility_percent'].values()))
        if first_day_vol > 80:
            mitigation_strats.append("High volatility predicted. Widen stop-loss orders to avoid premature exit.")
    except (KeyError, StopIteration):
        pass

    return {
        "execution_timing": timing_windows,
        "portfolio_rebalancing": rebalancing_recs,
        "risk_mitigation": mitigation_strats
    }
