# goquant_assignment/data_sources/twitter.py

import requests
import os
import random
from typing import List, Dict

# The URL for the Twitter/X API v2 recent search endpoint.
API_URL = "https://api.twitter.com/2/tweets/search/recent"
BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")

# We bring back our mock database as a reliable fallback.
MOCK_TWEETS_DB = {
    "uniswap": [
        "Just used Uniswap to swap some ETH for a new altcoin. So smooth! #DeFi",
        "The new Uniswap v4 hooks feature is going to be a game changer for liquidity providers.",
        "High gas fees on Ethereum are making my Uniswap trades so expensive... we need L2 scaling now!",
        "Is Uniswap the best DEX? I think so. The user experience is unmatched. $UNI to the moon!",
        "I'm a bit concerned about the regulatory pressure on protocols like Uniswap. Hope they can navigate it.",
    ],
    "bitcoin": [
        "Just stacking sats. Bitcoin is the only true digital gold.",
        "The halving is complete! Let's see what this does to the Bitcoin price over the next year.",
        "Bitcoin ETFs are seeing massive inflows. The institutions are here.",
    ]
}

def get_mock_tweets(query: str, count: int) -> List[Dict]:
    """Returns a list of mock tweets as a fallback."""
    print("--- FALLING BACK TO MOCK TWEET DATA ---")
    tweet_pool = MOCK_TWEETS_DB.get(query.lower(), [f"This is a generic tweet about {query}."])
    num_to_sample = min(count, len(tweet_pool))
    selected_tweets = random.sample(tweet_pool, num_to_sample)
    return [{"text": tweet} for tweet in selected_tweets]

def get_recent_tweets(query: str, count: int = 10) -> List[Dict]:
    """
    Fetches recent tweets from the live Twitter/X API, with a fallback to mock data
    in case of rate limiting or errors.
    """
    print(f"\n--- Attempting to call live Twitter API for query: '{query}' ---")
    
    if not BEARER_TOKEN:
        print("--- WARNING: TWITTER_BEARER_TOKEN not found. ---")
        return get_mock_tweets(query, count)

    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    search_query = f"({query} OR ${query}) -is:retweet lang:en"
    params = {'query': search_query, 'max_results': max(10, min(count, 100))}

    try:
        response = requests.get(API_URL, headers=headers, params=params, timeout=10)
        
        # If we are being rate-limited, fall back to mock data.
        if response.status_code == 429:
            print("--- Twitter API rate limit exceeded. ---")
            return get_mock_tweets(query, count)
            
        response.raise_for_status() # Raise an error for other bad responses
        
        json_response = response.json()
        tweets = json_response.get('data', [])
        
        print(f"--- Found {len(tweets)} live tweets. ---")
        return tweets if tweets else get_mock_tweets(query, count)

    except requests.exceptions.RequestException as e:
        print(f"--- ERROR: Failed to connect to Twitter API: {e} ---")
        return get_mock_tweets(query, count)
