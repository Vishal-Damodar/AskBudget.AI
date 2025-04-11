
---

## 📅 `ROADMAP.md`

# 🛣️ Budget Buddy – Project Roadmap

A plan to build the smartest personal finance tracker powered by LLMs.

---

## ✅ MVP Phase 1 (Core Features)

- [x] Upload support for PhonePe / GPay CSV
- [x] Normalize transaction structure
- [x] LLM-based expense categorization
- [x] Store user-specific vendor-category mapping (Arun Kumar → Rent)
- [x] Detect recurring patterns by name/amount/date
- [ ] Categorization fallback if LLM fails
- [ ] Streamlit frontend for upload & results
- [ ] Monthly summary chart with total & category-wise breakdown
- [ ] Export categorized transactions as CSV

---

## 🚧 MVP Phase 2 (Nice-to-Have)

- [ ] Natural Language Query (NLQ): “How much on food last month?”
- [ ] Date-wise filters: This month / last 3 months / custom range
- [ ] Manual editing of categories via UI
- [ ] Flag large or unusual transactions
- [ ] Budget goal tracking (per category)

---

## 🌐 Post-MVP Ideas

- [ ] Support PDF bank statements (OCR or pattern-based)
- [ ] Link bank APIs (if available in India)
- [ ] Visualize spending trends over time
- [ ] Mobile-friendly frontend (React Native / Flutter)
- [ ] Auto-email monthly summary
- [ ] Cloud sync option (optional)

---

## 🐞 Known Issues / Bugs

- [ ] LLM misclassifies UPI transfers with unknown names
- [ ] Parsing sometimes fails on Google Pay statements with new formats

---

## 📌 Notes

- No financial data is ever sent to the cloud unless user explicitly opts in.
- Designed to be privacy-first and work offline (or locally).

---

