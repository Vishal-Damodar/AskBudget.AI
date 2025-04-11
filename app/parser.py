# app/parser.py

import fitz  # PyMuPDF
import re
import pandas as pd
from io import BytesIO
from typing import List, Dict
import logging
from datetime import datetime

# Setup logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("backend.log"), logging.StreamHandler()]
)

def parse_statement(file_bytes: bytes, source: str) -> List[Dict]:
    logging.info(f"Parsing statement for source: {source}")
    text = ""

    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            logging.info(f"PDF opened with {len(doc)} pages")
            for i, page in enumerate(doc):
                page_text = page.get_text()
                logging.info(f"Extracted text from page {i+1}: {len(page_text)} characters")
                text += page_text
            logging.info(f"text: {text}")
    except Exception as e:
        logging.exception("Failed to parse PDF with fitz")

    if source.lower() == "phonepe":
        return parse_phonepe(text)
    elif source.lower() == "sbi":
        return parse_sbi(text)
    else:
        logging.error(f"Unsupported source received: {source}")
        raise ValueError("Unsupported source. Try: phonepe or sbi")

def parse_phonepe(all_text: str) -> List[Dict]:
    logging.info("Using PhonePe parser")
    all_text = all_text.replace("₹", "").strip()
    pattern = re.compile(
        r"(Apr|Mar|Feb|Jan|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2}, \d{4}\n"         # Date
        r".*\n"                                                                      # Time (ignored)
        r"(CREDIT|DEBIT)\n"                                                          # Type
        r"([\d,]+(?:\.\d{2})?)\n"                                                    # Amount
        r"(Paid to|Received from) (.+)",                                             # Description
        re.MULTILINE
    )

    transactions = []
    for match in pattern.finditer(all_text):
        month_day_year, txn_type, amount, direction, description = match.groups()
        date_line = match.group(0).splitlines()[0]
        transactions.append({
            "date": date_line,
            "description": description.strip(),
            "amount": amount.replace(",", ""),
            "txn_type": txn_type
        })
    df = pd.DataFrame(transactions)
    df["date"] = pd.to_datetime(df["date"], format="%b %d, %Y").dt.strftime("%Y-%m-%d")
    logging.info(f"Extracted {len(transactions)} PhonePe transactions")
    return df.to_dict(orient="records")
    


def parse_sbi(text: str) -> List[Dict]:
    logging.info("Using SBI parser")
    text = text.replace("₹", "").replace(",", "").strip()

    debit_pattern = re.compile(
        r'(?:^|\n)(?P<amount>\d+\.\d{2})\s*-\s*\n(?P<date>\d{2} \w{3} \d{4})\n'
        r'(?P<description>TRANSFER TO .*?UPI/DR/[^\n]+.*?)\n(?P<balance>\d+\.\d{2})',
        re.DOTALL
    )

    credit_pattern = re.compile(
        r'(?:^|\n)-\s*\n(?P<amount>\d+\.\d{2})\n(?P<date>\d{2} \w{3} \d{4})\n'
        r'(?P<description>TRANSFER FROM .*?UPI/CR/[^\n]+.*?)\n(?P<balance>\d+\.\d{2})',
        re.DOTALL
    )

    def extract_name(desc):
        match = re.search(r'UPI/(?:CR|DR)/\d+/([\w\s\.]+)', desc)
        return match.group(1).strip() if match else desc

    transactions = []
    for match in debit_pattern.finditer(text):
        transactions.append({
            "date": match.group("date"),
            "description": extract_name(match.group("description")),
            "amount": float(match.group("amount")),
            "txn_type": "DEBIT"
        })

    for match in credit_pattern.finditer(text):
        transactions.append({
            "date": match.group("date"),
            "description": extract_name(match.group("description")),
            "amount": float(match.group("amount")),
            "txn_type": "CREDIT"
        })

    logging.info(f"Extracted {len(transactions)} SBI transactions")

    df = pd.DataFrame(transactions)
    df["date"] = pd.to_datetime(df["date"], format="%d %b %Y").dt.strftime("%Y-%m-%d")
    return df.to_dict(orient="records")
