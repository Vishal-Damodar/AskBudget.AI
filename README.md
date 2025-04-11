# 💸 Budget Buddy – Your AI-Powered Expense Assistant

Budget Buddy is a smart personal finance assistant that helps you understand where your money goes. Upload your bank or payment app statements (like PhonePe, Google Pay, SBI, etc.), and let AI categorize, analyze, and summarize your expenses – all with privacy-first, offline-friendly tech.

---

## 🚀 Features

- 📥 **Bank/Wallet Statement Upload**
  - Supports statements from major banks and UPI apps
- 🤖 **Automatic Expense Categorization**
  - Uses LLMs to classify spending intelligently
- 🔁 **Recurring Transaction Detection**
  - Identify patterns like rent, subscriptions, or monthly bills
- 🧠 **Smart Labeling for Unknowns**
  - Asks for your input when a transaction is unclear (e.g., “Arun Kumar” for rent)
- 💬 **Ask Your Data (NLQ)**
  - “What did I spend on food last month?”
- 📊 **Monthly Summary View**
  - Clear charts and spending breakdowns
- 🔒 **Privacy-First**
  - Local-only processing (no cloud uploads required)

---

## ⚙️ Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: Streamlit (MVP)
- **AI Models**: Azure OpenAI (GPT-3.5 or GPT-4)
- **Storage**: SQLite / JSON
- **Libraries**: pandas, langchain (optional), matplotlib, etc.

---

## 📦 Getting Started

```bash
git clone https://github.com/your-username/budget-buddy.git
cd budget-buddy
pip install -r requirements.txt
```
---

## 🧠 Setup LLM (Optional)
Configure your OpenAI / Azure API key in .env

Default categorization will work without LLM too (rule-based fallback)

---

## ▶️ Run App
bash
Copy
Edit
uvicorn app.main:app --reload   # FastAPI backend
streamlit run app/ui.py         # UI to upload & view summaries
📸 Screenshots
Coming soon...

---

## 📜 License
MIT – Use it, build on it, share it.

---

## 🙌 Credits
Built by Vishal Damodar