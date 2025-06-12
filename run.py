# run.py
import sys
import os

# Add the project directory to sys.path
project_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_dir)
print(sys.path)  # Debug: Print the Python path to verify

from backend.main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)