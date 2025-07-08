# goquant_assignment/api/main.py

from fastapi import FastAPI
# Import all of our endpoint routers, including the new 'sentiment' one.
from api.endpoints import market_data, governance, risk, volatility, liquidity, sentiment

# Create the main FastAPI application instance.
app = FastAPI(
    title="Protocol Upgrade Monitor API",
    description="An API for monitoring blockchain protocol upgrades and assessing risk.",
    version="0.1.0",
)

# A simple root endpoint to check if the API is running.
@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "message": "Welcome to the Protocol Upgrade Monitor API"}

# Include all the routers from our endpoint files.
app.include_router(market_data.router, prefix="/v1")
app.include_router(governance.router, prefix="/v1")
app.include_router(risk.router, prefix="/v1")
app.include_router(volatility.router, prefix="/v1")
app.include_router(liquidity.router, prefix="/v1")
app.include_router(sentiment.router, prefix="/v1") # <-- ADD THIS LINE
