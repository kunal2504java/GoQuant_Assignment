import uvicorn

if __name__ == "__main__":
    # This is the new, official way to run the application.
    # It tells uvicorn to look for the 'app' object inside the 'api/main.py' file.
    # Because we are running from the root directory, Python's import system
    # will work correctly without any hacks.
    # --reload will watch for changes in the entire project directory.
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
