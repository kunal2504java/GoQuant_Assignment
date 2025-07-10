# goquant_assignment/api/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Import all of our endpoint routers
from api.endpoints import market_data, governance, risk, volatility, liquidity, sentiment, social, governance_prediction, recommendations, blockchain

# Create the main FastAPI application instance.
app = FastAPI(
    title="Protocol Upgrade Monitor API",
    description="An API for monitoring blockchain protocol upgrades and assessing risk.",
    version="0.1.0",
)

# --- CORS MIDDLEWARE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API ROUTERS ---
app.include_router(market_data.router, prefix="/api/v1")
app.include_router(governance.router, prefix="/api/v1")
app.include_router(risk.router, prefix="/api/v1")
app.include_router(volatility.router, prefix="/api/v1")
app.include_router(liquidity.router, prefix="/api/v1")
app.include_router(sentiment.router, prefix="/api/v1")
app.include_router(social.router, prefix="/api/v1")
app.include_router(governance_prediction.router, prefix="/api/v1")
app.include_router(recommendations.router, prefix="/api/v1")
app.include_router(blockchain.router, prefix="/api/v1") # <-- ADD THIS LINE


# --- SERVE FRONTEND ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
frontend_dir = os.path.join(project_root, 'frontend')
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")