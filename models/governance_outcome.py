# goquant_assignment/models/governance_outcome.py

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from typing import Dict, Any

# --- Mock Training Data ---
# In a real-world scenario, this would be a large dataset of thousands of past proposals.
# Here, we simulate a small dataset to train our model.
# Each proposal has text and a label (1 for 'Passed', 0 for 'Failed').
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
# We create global variables for our model and vectorizer.
# This ensures they are trained only once when the application starts.
vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
model = LogisticRegression()

def train_model():
    """
    Trains the Logistic Regression model on our mock data.
    """
    print("\n--- Training Governance Outcome Prediction Model... ---")
    try:
        # Separate the text data and the labels (passed/failed).
        texts = [d['text'] for d in TRAINING_DATA]
        labels = np.array([d['passed'] for d in TRAINING_DATA])

        # Convert the text data into numerical features using TF-IDF.
        # TF-IDF measures how important a word is to a document in a collection.
        X_features = vectorizer.fit_transform(texts)

        # Train (fit) the logistic regression model on the features and labels.
        model.fit(X_features, labels)
        print("--- Governance Outcome Model Trained Successfully. ---")
    except Exception as e:
        print(f"--- CRITICAL ERROR: Failed to train governance model: {e} ---")
        # In a real app, you might want to handle this more gracefully.
        raise

# Train the model when the module is first loaded.
train_model()


def predict_outcome(title: str, body: str) -> Dict[str, Any]:
    """
    Predicts the outcome of a new governance proposal.

    Args:
        title: The title of the proposal.
        body: The body content of the proposal.

    Returns:
        A dictionary containing the prediction and the confidence probability.
    """
    print(f"\n--- Predicting outcome for proposal: '{title}' ---")
    
    # Combine title and body for a complete analysis.
    full_text = title + " " + (body or "")
    
    # Transform the new text using the *already fitted* vectorizer.
    X_new = vectorizer.transform([full_text])
    
    # Predict the outcome (0 or 1).
    prediction_result = model.predict(X_new)[0]
    
    # Predict the probability of each outcome ([prob_of_0, prob_of_1]).
    prediction_proba = model.predict_proba(X_new)[0]

    prediction_label = "Likely to Pass" if prediction_result == 1 else "Likely to Fail"
    confidence = prediction_proba[prediction_result] * 100 # Get the probability of the predicted class

    print(f"Prediction: {prediction_label} with {confidence:.2f}% confidence.")

    return {
        "prediction": prediction_label,
        "confidence_percent": round(confidence, 2)
    }