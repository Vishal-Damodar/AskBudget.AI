# app/routes.py

import os
import tempfile
import logging
from fastapi import APIRouter, UploadFile, File, Form
from app.parser import parse_statement
from app.categorizer import categorize_transactions

# Setup logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("logs/backend.log"), logging.StreamHandler()]
)

router = APIRouter()

@router.post("/upload/")
async def upload_statement(
    file: UploadFile = File(...),
    source: str = Form(...)
):
    """
    Upload a bank/payment PDF and return normalized transactions.
    Supported sources: phonepe, sbi
    """
    try:
        logging.info(f"Received upload request - File: {file.filename}, Source: {source}")

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name
            logging.info(f"Saved uploaded file temporarily at {tmp_path}")

        with open(tmp_path, "rb") as f:
            transactions = parse_statement(f.read(), source)
            logging.info(f"Parsed {len(transactions)} transactions from statement")

        os.remove(tmp_path)
        logging.info(f"Deleted temporary file: {tmp_path}")

        categorized = categorize_transactions(transactions)

        return {"transactions": categorized}


    except Exception as e:
        logging.exception("Error occurred while processing the uploaded statement")
        return {"error": str(e)}
