Protocol Upgrade Monitor
A high-performance, full-stack monitoring system that tracks blockchain protocol upgrades, predicts market shifts using machine learning, and provides actionable trading guidance.

Features
Dynamic Three-Panel UI: A responsive user interface for monitoring inputs, viewing the upgrade timeline, and receiving analytical guidance.

Multi-Source Data Integration: Connects to live data from Etherscan, Snapshot, Twitter/X, CoinGecko, and DeFi Llama.

Predictive Modeling Suite:

Volatility Forecasting: A GARCH(1,1) model forecasts future price volatility.

Liquidity Prediction: An ARIMA time-series model predicts future TVL movements.

Sentiment Analysis: A DistilBERT transformer model provides real-time sentiment scoring of social media data.

Governance Outcome Prediction: A Logistic Regression model classifies the likely success or failure of governance proposals.

Multi-factor Risk Assessment: A sophisticated risk model that synthesizes technical, market, liquidity, and governance factors into a single, weighted risk score.

Actionable Recommendations: A rule-based engine generates guidance for execution timing, portfolio rebalancing, and risk mitigation strategies.

RESTful Backend API: A clean, high-performance API built with Python and FastAPI to serve data and model outputs.

Tech Stack
Backend: Python, FastAPI

Frontend: HTML, Tailwind CSS, JavaScript

Data Science & ML: Pandas, NumPy, Scikit-learn, Statsmodels (for ARIMA), Arch (for GARCH), Transformers & PyTorch (for NLP).

API Interaction: Requests

Architecture
The project follows a clean, modular architecture to ensure maintainability and separation of concerns:

/frontend/: Contains the index.html file for the user interface.

/api/: The FastAPI backend, containing the main application (main.py) and endpoint definitions.

/data_sources/: Modules for connecting to external APIs (CoinGecko, DeFi Llama, Snapshot, etc.).

/models/: Implementations of the predictive models (GARCH, ARIMA, NLP, etc.).

/services/: The core business logic that orchestrates data and models to produce intelligent outputs (e.g., the multi-factor risk score).

Setup and Installation
Follow these steps to run the project locally.

1. Clone the Repository
git clone 

2. Set Up a Virtual Environment
It is highly recommended to use a Python virtual environment.

# Create the environment
python -m venv venv

# Activate the environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

3. Install Dependencies
Install all the required Python libraries from the requirements.txt file.

pip install -r requirements.txt

(Note: The first time you run this, the NLP models from Hugging Face will also be downloaded, which may take a few minutes).

4. Set Environment Variables
This application requires API credentials, which should be set as environment variables for security.

Etherscan API Key: Get a free API key from etherscan.io/apis.

Twitter/X Bearer Token: Get this from your X Developer account.

In your terminal, set the variables before running the server.

On Windows (PowerShell):

$env:ETHERSCAN_API_KEY="YOUR_ETHERSCAN_KEY_HERE"
$env:TWITTER_BEARER_TOKEN="YOUR_TWITTER_BEARER_TOKEN_HERE"

On macOS/Linux:

export ETHERSCAN_API_KEY="YOUR_ETHERSCAN_KEY_HERE"
export TWITTER_BEARER_TOKEN="YOUR_TWITTER_BEARER_TOKEN_HERE"

5. Run the Application
From the project's root directory, use the launcher script to start the server.

python run.py

The application will be available at http://127.0.0.1:8000.

The interactive API documentation (powered by Swagger UI) is available at http://127.0.0.1:8000/docs.
