# ui/dashboard.py


import streamlit as st
import pandas as pd
import requests
import logging
import matplotlib.pyplot as plt
from datetime import datetime

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
                "http://127.0.0.1:8000/upload/",
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

                # --- User Feedback Tagging ---
                st.markdown("### 🏷️ Tag Unknown Vendors")
                with st.form("tag_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        vendor = st.selectbox("Choose a vendor to tag", df["description"].unique())
                    with col2:
                        category = st.selectbox("Assign a category", ["Food", "Rent", "Travel", "Shopping", "Subscriptions", "Salary","Family & Friends", "Others"])

                    submitted = st.form_submit_button("✅ Tag Vendor")

                    if submitted:
                        tag_response = requests.post(
                            "http://localhost:8000/tag/",
                            data={"vendor": vendor, "category": category}
                        )
                        if tag_response.status_code == 200:
                            st.success(f"Tagged '{vendor}' as '{category}' successfully!")
                        else:
                            st.error("❌ Failed to tag vendor. Please try again.")

                # Now fetch the monthly summary
                summary_response = requests.post("http://localhost:8000/monthly_summary/",json=parsed)

                
                if summary_response.status_code == 200:
                    summary_data = summary_response.json()
                    summary_df = pd.DataFrame(summary_data)

                    # Plot a Bar Chart for the Monthly Summary
                    st.markdown("### 📊 Monthly Expense Summary")
                    st.dataframe(summary_df)

                    # Plotting a bar chart
                    fig, ax = plt.subplots()
                    ax.bar(summary_df['category'], summary_df['total_spend'], color='skyblue')
                    ax.set_xlabel('Category')
                    ax.set_ylabel('Total Spend (₹)')
                    ax.set_title(f"Total Spend per Category for {datetime.now().strftime('%B %Y')}")
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

                else:
                    st.error("❌ Failed to fetch monthly summary data.")
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
