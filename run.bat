@echo off
echo Activating virtual environment...

call .venv\Scripts\activate

echo Starting FastAPI backend...
start cmd /k "call .venv\Scripts\activate && uvicorn app.main:app --reload"

timeout /t 2

echo Starting Streamlit frontend...
start cmd /k "call .venv\Scripts\activate && streamlit run ui/dashboard.py"
