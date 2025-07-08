# goquant_assignment/models/sentiment_analysis.py

# Import the 'pipeline' tool from the transformers library.
# This is a high-level helper that makes using pre-trained models very easy.
from transformers import pipeline
from typing import Dict

# --- Model Initialization ---
# We create a global variable for our sentiment analysis pipeline.
# This ensures the model is only loaded into memory once when the application starts,
# which is much more efficient than loading it for every request.
#
# Model used: 'distilbert-base-uncased-finetuned-sst-2-english'
# This is a lightweight, fast, and accurate model for sentiment analysis.
# It classifies text as either 'POSITIVE' or 'NEGATIVE'.
# The first time this code runs, it will download the model files (a few hundred MB).
try:
    print("\n--- Initializing Sentiment Analysis Model (this may take a moment)... ---")
    sentiment_pipeline = pipeline(
        "sentiment-analysis", 
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )
    print("--- Sentiment Analysis Model Initialized Successfully. ---")
except Exception as e:
    print(f"--- CRITICAL ERROR: Failed to initialize sentiment model: {e} ---")
    # If the model fails to load, we set the pipeline to None so our app
    # can handle it gracefully instead of crashing.
    sentiment_pipeline = None


def analyze_sentiment(text: str) -> Dict:
    """
    Analyzes a piece of text and returns its sentiment score.

    Args:
        text: The input string to analyze.

    Returns:
        A dictionary containing the sentiment label ('POSITIVE' or 'NEGATIVE')
        and a confidence score.
    """
    if sentiment_pipeline is None:
        raise RuntimeError("Sentiment analysis pipeline is not available.")

    # The pipeline returns a list with a single dictionary, e.g., [{'label': 'POSITIVE', 'score': 0.999}]
    # We truncate the text to the model's max input size to avoid errors.
    max_length = 512
    truncated_text = text[:max_length]

    try:
        results = sentiment_pipeline(truncated_text)
        # We return the first (and only) result from the list.
        return results[0]
    except Exception as e:
        print(f"Error during sentiment analysis for text: '{truncated_text[:50]}...'")
        raise RuntimeError(f"Sentiment analysis failed: {e}")