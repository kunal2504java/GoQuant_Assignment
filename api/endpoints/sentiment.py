# goquant_assignment/api/endpoints/sentiment.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from models.sentiment_analysis import analyze_sentiment, sentiment_pipeline

router = APIRouter()

class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=1, example="This protocol upgrade is fantastic and will bring a lot of value.")

@router.post("/analyze/sentiment", tags=["Predictive Models"])
def get_sentiment_analysis(request: SentimentRequest):
    """
    Analyzes the sentiment of a given text using a pre-trained NLP model.
    """
    # Check if the model failed to load during startup.
    if sentiment_pipeline is None:
        raise HTTPException(
            status_code=503, 
            detail="Sentiment analysis service is currently unavailable."
        )
        
    try:
        # Call the analysis function from our model file.
        result = analyze_sentiment(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")