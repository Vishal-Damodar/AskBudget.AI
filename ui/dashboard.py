# ui/dashboard.py

import streamlit as st
import pandas as pd
import requests
import logging

# Setup logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("dashboard.log"), logging.StreamHandler()]
)

st.set_page_config(
    page_title="AskBudget.AI",
    page_icon="💸",
    layout="wide"
)

st.title("💬 AskBudget.AI")
st.subheader("Smart Spending Insights from Your Bank & Payment Statements")

st.markdown("---")

st.markdown("### 📥 Upload Your Bank/Payment PDF Statement")
uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])
source = st.selectbox("Select Source", ["phonepe", "sbi"])

if uploaded_file and source:
    try:
        logging.info(f"Uploading file: {uploaded_file.name}, Source selected: {source}")

        with st.spinner("Parsing your statement..."):
            response = requests.post(
                "http://localhost:8000/upload/",
                files={"file": uploaded_file.getvalue()},
                data={"source": source}
            )

        if response.status_code == 200:
            response_json = response.json()
            if "transactions" in response_json:
                parsed = response_json["transactions"]
                df = pd.DataFrame(parsed)
                st.success("✅ Statement parsed successfully!")
                st.markdown("### 🧾 Parsed Transactions")
                st.dataframe(df)
                logging.info(f"Successfully parsed statement with {len(df)} transactions")
            else:
                error_msg = response_json.get("error", "Unknown error")
                st.error(f"❌ Failed to parse. Reason: {error_msg}")
                logging.error(f"Parsing failed: {error_msg}")
        else:
            st.error("❌ Server error: Failed to process the request.")
            logging.error(f"Server responded with status code {response.status_code}: {response.text}")

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
        logging.exception("Exception occurred while parsing statement")

st.markdown("---")
st.caption("Built with ❤️ by Vishal P Damodar")
