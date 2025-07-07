# goquant_assignment/api/main.py

from fastapi import FastAPI
from api.endpoints import market_data

# Create the main FastAPI application instance.
# Its only job is to define the 'app' object and include the routers.
app = FastAPI(
    title="Protocol Upgrade Monitor API",
    description="An API for monitoring blockchain protocol upgrades and assessing risk.",
    version="0.1.0",
)

# Include the router from our market_data endpoint file.
# This makes the /price/{token_id} endpoint available under the /v1 prefix.
app.include_router(market_data.router, prefix="/v1")

# A simple root endpoint to check if the API is running.
@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "message": "Welcome to the Protocol Upgrade Monitor API"}
