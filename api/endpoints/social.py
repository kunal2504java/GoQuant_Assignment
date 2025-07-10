# goquant_assignment/api/endpoints/social.py

from fastapi import APIRouter, HTTPException, Path
from data_sources import twitter
from models.sentiment_analysis import analyze_sentiment, sentiment_pipeline
from typing import List

router = APIRouter()

@router.get("/analyze/social-sentiment/{query}", tags=["Social Media Analysis"])
def get_social_sentiment(
    query: str = Path(...,
                      title="Search Query",
                      description="The keyword to search for on social media (e.g., 'uniswap')",
                      example="aave")
):
    """
    Fetches recent mock tweets for a query and analyzes their overall sentiment.
    """
    if sentiment_pipeline is None:
        raise HTTPException(status_code=503, detail="Sentiment analysis service is unavailable.")

    try:
        # Step 1: Get recent tweets from our mock data source.
        tweets = twitter.get_recent_tweets(query)
        
        if not tweets:
            return {"query": query, "average_sentiment": "NEUTRAL", "sentiment_score": 0, "analyzed_tweets": []}

        # Step 2: Analyze the sentiment of each tweet.
        analyzed_tweets = []
        positive_scores = []
        negative_scores = []

        for tweet in tweets:
            sentiment_result = analyze_sentiment(tweet["text"])
            analyzed_tweets.append({
                "text": tweet["text"],
                "sentiment": sentiment_result["label"],
                "score": sentiment_result["score"]
            })
            if sentiment_result["label"] == "POSITIVE":
                positive_scores.append(sentiment_result["score"])
            else:
                negative_scores.append(sentiment_result["score"])

        # Step 3: Calculate an overall sentiment score.
        # A simple average: +1 for each positive, -1 for each negative.
        total_score = len(positive_scores) - len(negative_scores)
        
        # Determine the final label.
        avg_sentiment_label = "NEUTRAL"
        if total_score > 0:
            avg_sentiment_label = "POSITIVE"
        elif total_score < 0:
            avg_sentiment_label = "NEGATIVE"

        return {
            "query": query,
            "average_sentiment": avg_sentiment_label,
            "net_sentiment_score": total_score,
            "analyzed_tweets": analyzed_tweets
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")

