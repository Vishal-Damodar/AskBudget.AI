#!/bin/bash
echo "Starting FastAPI backend..."
uvicorn app.main:app --reload &
sleep 2
echo "Starting Streamlit frontend..."
streamlit run ui/dashboard.py
