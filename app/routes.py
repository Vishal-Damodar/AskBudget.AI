# app/routes.py

import os
import tempfile
import logging
import pandas as pd
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Form
from app.parser import parse_statement
from app.categorizer import categorize_transactions
from storage.category_mappings import set_user_category

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


@router.post("/tag/")
def tag_vendor(vendor: str = Form(...), category: str = Form(...)):
    try:
        set_user_category(vendor, category)
        return {"message": f"Tagged '{vendor}' as '{category}'"}
    except Exception as e:
        return {"error": str(e)}
    

@router.post("/monthly_summary/")
def get_monthly_summary(transactions: list[dict]) -> list[dict]:
    """Get monthly summary of transactions."""
 
    print("📊 [DEBUG] Fetching monthly summary")

    df = pd.DataFrame(transactions)
    print("🧾 [DEBUG] Initial DataFrame:")
    print(df.head())

    # Convert date
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Drop rows with invalid dates
    df = df.dropna(subset=["date"])
    print("📅 [DEBUG] After date conversion:")
    print(df[['date', 'amount', 'category']].head())

    # Filter to current month
    current_month = datetime.now().month
    current_year = datetime.now().year
    df = df[(df['date'].dt.month == current_month) & (df['date'].dt.year == current_year)]
    print(f"📅 [DEBUG] Filtered to {current_year}-{current_month}:")
    print(df[['date', 'category', 'amount']])

    # Convert amount to float
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])

    # Check if 'category' column exists
    if "category" not in df.columns:
        print("⚠️ [DEBUG] 'category' column missing in data!")
        return []
    df["category"] = df["category"].str.lower().str.strip()

    # Group and summarize
    summary = df.groupby("category")["amount"].sum().reset_index()
    summary = summary.rename(columns={"amount": "total_spend"})

    print("📊 [DEBUG] Final Monthly Summary:")
    print(summary)

    return summary.to_dict(orient="records")

