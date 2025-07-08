# goquant_assignment/services/risk_assessment.py

from typing import Dict

# Define keywords and their associated risk points.
# This is a simple, rule-based model to start with.
RISK_KEYWORDS: Dict[str, int] = {
    # High-risk keywords related to core contract changes
    "upgrade": 25,
    "migration": 25,
    "v4": 20,
    "v3": 20,
    "parameter change": 15,
    "smart contract": 15,
    "security": 15,
    "emergency": 30,

    # Medium-risk keywords related to treasury and tokenomics
    "treasury": 10,
    "budget": 10,
    "incentives": 10,
    "mint": 10,
    "burn": 10,
    "fee switch": 15,
    "tokenomics": 10,

    # Low-risk keywords related to community and process
    "election": 5,
    "committee": 5,
    "grant": 5,
    "partnership": 5,
    "temp check": 2,
}

def calculate_risk_score(title: str, body: str) -> int:
    """
    Calculates a risk score for a proposal based on keywords in its title and body.

    Args:
        title: The title of the governance proposal.
        body: The body content of the governance proposal.

    Returns:
        A risk score between 0 and 100.
    """
    print(f"\n--- Assessing risk for proposal: '{title}' ---")
    
    total_score = 0
    # Combine title and body and convert to lowercase for case-insensitive matching.
    content = (title + " " + body).lower()
    
    found_keywords = []

    for keyword, points in RISK_KEYWORDS.items():
        if keyword in content:
            total_score += points
            found_keywords.append(keyword)

    # Cap the score at 100 to ensure it's on a consistent scale.
    final_score = min(total_score, 100)
    
    print(f"Found keywords: {found_keywords}")
    print(f"Calculated score: {final_score}/100")
    
    return final_score
