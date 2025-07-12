# goquant_assignment/models/governance_outcome.py

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from typing import Dict, Any, List

# --- Mock Training Data ---
TRAINING_DATA = [
    {"text": "AIP-1: Treasury diversification into stablecoins", "passed": 1},
    {"text": "Proposal to increase protocol fees by 5%", "passed": 1},
    {"text": "Emergency security patch for critical vulnerability", "passed": 1},
    {"text": "Partnership with new ecosystem project", "passed": 1},
    {"text": "Grant request for community marketing campaign", "passed": 1},
    {"text": "Temp check for controversial tokenomics change", "passed": 0},
    {"text": "Proposal to mint 1 billion new tokens", "passed": 0},
    {"text": "Radical change to the governance voting structure", "passed": 0},
    {"text": "Request to fund an unproven experimental feature", "passed": 0},
]

# --- Model and Vectorizer Initialization ---
vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
model = LogisticRegression()
# Global variable to store feature importances after training
feature_importances: List[Dict[str, Any]] = []

def train_model():
    """
    Trains the Logistic Regression model and calculates feature importances.
    """
    global feature_importances
    print("\n--- Training Governance Outcome Prediction Model... ---")
    try:
        texts = [d['text'] for d in TRAINING_DATA]
        labels = np.array([d['passed'] for d in TRAINING_DATA])
        X_features = vectorizer.fit_transform(texts)
        model.fit(X_features, labels)
        
        # --- NEW: Calculate and store feature importances ---
        # Get the feature names (words) from the vectorizer.
        feature_names = vectorizer.get_feature_names_out()
        # Get the coefficients from the trained model.
        # The magnitude of the coefficient indicates the word's importance.
        coefficients = model.coef_[0]
        
        # Combine them and sort by the absolute value of the coefficient.
        importance_list = sorted(
            zip(feature_names, coefficients), 
            key=lambda item: abs(item[1]), 
            reverse=True
        )
        
        # Store the top 10 most important features.
        feature_importances = [
            {"feature": name, "importance": round(coef, 4), "direction": "Pass" if coef > 0 else "Fail"}
            for name, coef in importance_list[:10]
        ]
        
        print("--- Governance Outcome Model Trained Successfully. ---")
        print(f"--- Top Features Identified: {[f['feature'] for f in feature_importances]} ---")

    except Exception as e:
        print(f"--- CRITICAL ERROR: Failed to train governance model: {e} ---")
        raise

# Train the model when the module is first loaded.
train_model()

def predict_outcome(title: str, body: str) -> Dict[str, Any]:
    """
    Predicts the outcome of a new governance proposal.
    """
    print(f"\n--- Predicting outcome for proposal: '{title}' ---")
    full_text = title + " " + (body or "")
    X_new = vectorizer.transform([full_text])
    prediction_result = model.predict(X_new)[0]
    prediction_proba = model.predict_proba(X_new)[0]
    prediction_label = "Likely to Pass" if prediction_result == 1 else "Likely to Fail"
    confidence = prediction_proba[prediction_result] * 100
    print(f"Prediction: {prediction_label} with {confidence:.2f}% confidence.")
    return {
        "prediction": prediction_label,
        "confidence_percent": round(confidence, 2)
    }

def get_feature_importances() -> List[Dict[str, Any]]:
    """
    Returns the most important features identified during model training.
    """
    return feature_importances