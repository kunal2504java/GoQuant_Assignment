# goquant_assignment/run.py

import uvicorn

if __name__ == "__main__":
    """
    This is the single, official entry point to run the application.
    
    It tells uvicorn to look for the 'app' object inside the 'api.main' module.
    
    Because we are running this script from the project's root directory, 
    Python's import system will correctly find all modules and packages
    (like 'services' and 'data_sources') without any hacks.
    """
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)