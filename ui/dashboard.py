# ui/dashboard.py

import streamlit as st
import pandas as pd
import requests
import logging

# Setup logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("logs/dashboard.log"), logging.StreamHandler()]
)

st.set_page_config(
    page_title="AskBudget.AI",
    page_icon="💸",
    layout="wide"
)

st.markdown("""
    <style>
        .big-font { font-size:30px !important; font-weight: 600; }
        .subtitle { font-size:18px; color: #6c757d; margin-bottom: 1rem; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="big-font">💬 AskBudget.AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Smart insights from your Bank & Payment Statements</div>', unsafe_allow_html=True)

st.markdown("---")

# Upload + Source Selection
with st.container():
    st.markdown("### 📥 Upload Statement", help="Upload your PDF bank or payment statement")

    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded_file = st.file_uploader("Choose your statement (PDF only)", type=["pdf"])
    with col2:
        source = st.selectbox("📄 Source", ["phonepe", "sbi"])

# Parser Logic
if uploaded_file and source:
    try:
        logging.info(f"Uploading file: {uploaded_file.name}, Source: {source}")

        with st.spinner("⏳ Parsing your statement..."):
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
                st.markdown("### 🧾 Transactions Summary")

                # Display DataFrame directly (no card container)
                if "category" in df.columns:
                    df["category"] = df["category"].str.title()  # Optional: Capitalize category names

                st.dataframe(df[["date", "description", "amount", "txn_type", "category"]], use_container_width=True)


                logging.info(f"Parsed {len(df)} transactions successfully")

            else:
                error_msg = response_json.get("error", "Unknown error")
                st.error(f"❌ Could not parse statement. Reason: {error_msg}")
                logging.warning(f"Parse error: {error_msg}")
        else:
            st.error("❌ Server error: Failed to process the request.")
            logging.error(f"HTTP {response.status_code}: {response.text}")

    except Exception as e:
        st.error(f"⚠️ Unexpected error: {str(e)}")
        logging.exception("Exception during file upload")

st.markdown("---")
st.caption("Built with ❤️ by Vishal P Damodar")
