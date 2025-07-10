# goquant_assignment/services/risk_assessment.py

from typing import Dict, Any

# Define keywords for the technical risk component.
RISK_KEYWORDS: Dict[str, int] = {
    "upgrade": 25, "migration": 25, "v4": 20, "v3": 20,
    "parameter change": 15, "smart contract": 15, "security": 15,
    "emergency": 30, "treasury": 10, "budget": 10, "incentives": 10,
    "mint": 10, "burn": 10, "fee switch": 15, "tokenomics": 10,
    "election": 5, "committee": 5, "grant": 5, "partnership": 5,
    "temp check": 2,
}

def calculate_multi_factor_risk(
    proposal_title: str,
    proposal_body: str,
    volatility_forecast: Dict[str, Any],
    liquidity_forecast: Dict[str, Any],
    governance_prediction: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Calculates a multi-factor risk score based on several inputs.

    Args:
        proposal_title: The title of the governance proposal.
        proposal_body: The body content of the governance proposal.
        volatility_forecast: The output from the GARCH model.
        liquidity_forecast: The output from the ARIMA model.
        governance_prediction: The output from the governance outcome model.

    Returns:
        A dictionary containing the final score and the breakdown of sub-scores.
    """
    print(f"\n--- Starting Multi-factor Risk Assessment for: '{proposal_title}' ---")
    
    # --- 1. Technical Risk (Keywords) ---
    technical_risk_score = 0
    content = (proposal_title + " " + (proposal_body or "")).lower()
    for keyword, points in RISK_KEYWORDS.items():
        if keyword in content:
            technical_risk_score += points
    technical_risk_score = min(technical_risk_score, 100)
    print(f"Technical Risk (Keywords): {technical_risk_score}")

    # --- 2. Market Risk (Volatility) ---
    # We'll take the first day's forecasted annualized volatility.
    # We can create a simple scale: e.g., >50% vol is high risk.
    market_risk_score = 0
    try:
        first_day_vol = next(iter(volatility_forecast['forecast']['forecasted_annualized_volatility_percent'].values()))
        if first_day_vol > 100: market_risk_score = 100
        elif first_day_vol > 75: market_risk_score = 75
        elif first_day_vol > 50: market_risk_score = 50
        else: market_risk_score = 25
    except (KeyError, StopIteration):
        market_risk_score = 20 # Default if data is missing
    print(f"Market Risk (Volatility): {market_risk_score}")

    # --- 3. Liquidity Risk (TVL Trend) ---
    # Compare the last known TVL to the 7-day forecast.
    liquidity_risk_score = 0
    try:
        last_tvl = liquidity_forecast['forecast']['last_known_tvl_usd']
        forecast_tvl = next(iter(reversed(liquidity_forecast['forecast']['forecasted_tvl_usd'].values())))
        if last_tvl > 0:
            percent_change = ((forecast_tvl - last_tvl) / last_tvl) * 100
            if percent_change < -10: liquidity_risk_score = 90 # >10% drop is high risk
            elif percent_change < -5: liquidity_risk_score = 60 # >5% drop is medium risk
            else: liquidity_risk_score = 20
    except (KeyError, StopIteration):
        liquidity_risk_score = 20 # Default
    print(f"Liquidity Risk (TVL Trend): {liquidity_risk_score}")

    # --- 4. Governance Risk (Prediction) ---
    governance_risk_score = 0
    try:
        if governance_prediction['prediction'] == 'Likely to Fail':
            # A controversial or failing proposal adds risk.
            governance_risk_score = 70
        else:
            governance_risk_score = 30
    except KeyError:
        governance_risk_score = 20 # Default
    print(f"Governance Risk (Prediction): {governance_risk_score}")

    # --- 5. Final Weighted Score ---
    # Define weights for each risk factor. They must sum to 1.0.
    weights = {
        "technical": 0.40,
        "market": 0.20,
        "liquidity": 0.20,
        "governance": 0.20
    }
    
    final_score = (
        technical_risk_score * weights["technical"] +
        market_risk_score * weights["market"] +
        liquidity_risk_score * weights["liquidity"] +
        governance_risk_score * weights["governance"]
    )
    final_score = int(min(final_score, 100)) # Ensure score is an int and capped at 100
    print(f"--- Final Multi-factor Score: {final_score}/100 ---")

    return {
        "final_risk_score": final_score,
        "risk_breakdown": {
            "technical_risk": technical_risk_score,
            "market_risk": market_risk_score,
            "liquidity_risk": liquidity_risk_score,
            "governance_risk": governance_risk_score,
        },
        "weights": weights
    }
