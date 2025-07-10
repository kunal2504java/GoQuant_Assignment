Protocol Upgrade Monitor: System Architecture
1. Overview
The Protocol Upgrade Monitor is a full-stack application designed to provide real-time risk assessment and predictive analytics for blockchain protocol upgrades. The system is built on a modular, service-oriented architecture using Python for the backend and a dynamic HTML/JavaScript interface for the frontend.

The core design philosophy is the separation of concerns, where different parts of the application have distinct and independent responsibilities:

Frontend: Handles user interaction and data presentation.

API Layer: Serves as the central gateway between the frontend and the backend logic.

Data Source Layer: Manages all communication with external, third-party APIs.

Modeling Layer: Contains all the predictive models (GARCH, ARIMA, NLP, etc.).

Service Layer: Contains the business logic that orchestrates the data and models to produce intelligent outputs.

2. Project Structure
The project is organized into a series of directories, each with a specific purpose:

/frontend/: Contains the index.html file, which is the complete user interface. It is responsible for rendering the dashboard and making API calls to the backend.

/api/: This is the heart of the backend.

main.py: The main application file that initializes the FastAPI server, includes all the API routers, and serves the frontend.

endpoints/: This sub-directory contains individual files that define the API routes, grouped by functionality (e.g., market_data.py, governance.py, risk.py). This keeps the API organized and easy to maintain.

/data_sources/: This layer acts as an abstraction for all external data providers. Each file in this directory is responsible for connecting to a specific external API (e.g., coingecko.py, defillama.py, snapshot.py), fetching the raw data, and handling any errors.

/models/: This directory contains the implementations of all the advanced predictive models. Each file represents a specific model (e.g., garch_volatility.py, arima_liquidity.py, sentiment_analysis.py), making them reusable and easy to test independently.

/services/: This layer contains the core business logic of the application. It orchestrates the flow of data from the data_sources layer, processes it through the models layer, and produces the final analytical outputs (e.g., risk_assessment.py, recommendation_service.py).

run.py: A simple launcher script in the root directory, providing a single, reliable entry point for starting the web server.

3. Data and Logic Flow
The application follows a clear, request-response data flow, initiated by the user.

Step 1: User Interaction

The user opens the application at http://127.0.0.1:8000.

The FastAPI backend serves the frontend/index.html file.

The user clicks the "Start Monitoring" button.

Step 2: Fetching Governance Proposals

The frontend's JavaScript makes an API call to the backend endpoint: /api/v1/proposals/{space_id}.

The governance.py endpoint receives the request and calls the get_proposals() function in the data_sources/snapshot.py module.

The snapshot.py module sends a GraphQL query to the live Snapshot API.

The list of proposals is returned to the frontend and displayed in the center panel.

Step 3: Comprehensive Analysis

The user clicks on a specific proposal in the timeline.

The frontend's JavaScript triggers a series of parallel API calls to the backend for a full analysis:

/api/v1/forecast/volatility/{token_id}

/api/v1/forecast/liquidity/{protocol_slug}

/api/v1/predict/governance-outcome (with proposal text)

Each of these endpoints calls its respective data source and model (e.g., coingecko.py -> garch_volatility.py).

Step 4: Multi-Factor Risk & Recommendations

Once the initial analyses are complete, the frontend makes two final API calls, passing the results from the previous step:

/api/v1/risk/assess-risk/multi-factor: This endpoint calls the risk_assessment.py service, which uses the volatility, liquidity, and governance predictions to calculate the final, weighted risk score.

/api/v1/generate-recommendations: This endpoint calls the recommendation_service.py, which uses the final risk score and model outputs to generate rule-based trading guidance.

Step 5: Displaying Results

The frontend receives the final risk score and recommendations.

The JavaScript dynamically updates the right-hand "Execution Guidance" panel, rendering the charts and recommendation lists for the user.

4. API Endpoints
The backend exposes a RESTful API with a clear structure, prefixed by /api/v1/. The main categories of endpoints are:

Market Data: For fetching current and historical prices and TVL.

Governance: For fetching governance proposals.

Predictive Models: Endpoints for each model (volatility, liquidity, governance outcome).

Risk Assessment: For calculating the multi-factor risk score.

Execution Guidance: For generating actionable recommendations.

Blockchain Data: For fetching on-chain transaction data.
