# app/categorizer.py

import logging
from models.llm_wrapper import ask_llm  # You’ll create this in models/
from storage.category_cache import get_cached_category, cache_category
from storage.category_mappings import get_user_category

# Predefined fallback rules
RULES = {
    "food": ["swiggy", "zomato", "dominos", "ubereats"],
    "rent": ["rent", "landlord", "flat"],
    "shopping": ["amazon", "flipkart", "myntra"],
    "travel": ["ola", "uber", "irctc", "makemytrip"],
    "utilities": ["electricity", "water", "gas", "bbps"],
    "subscriptions": ["netflix", "prime", "spotify", "hotstar"],
    "salary": ["salary", "credited", "payroll"]
}

CATEGORIES = list(RULES.keys())

def rule_based_category(description: str) -> str:
    description = description.lower()
    for category, keywords in RULES.items():
        if any(kw in description for kw in keywords):
            return category
    return "other"

def categorize_transaction(txn: dict) -> str:
    description = txn.get("description", "")
    txn_type = txn.get("txn_type", "")

    user_category = get_user_category(description)
    if user_category:
        return user_category

    prompt = f"Classify the following transaction description into a category like food, rent, shopping, travel, utilities, subscriptions, salary, or other:\n\nDescription: {description}\n\Transaction Type: {txn_type}\n\nJust return a category name without any explanation."
    
     # 1. Check cache
    cached = get_cached_category(description)
    if cached:
        return cached
    
    try:
        category = ask_llm(prompt).strip().lower()
        print(category)
        if category:
            cache_category(description, category)
            return category
        
        if category not in CATEGORIES:
            category = rule_based_category(description)

    except Exception as e:
        logging.warning(f"LLM failed, using rule-based fallback. Desc: {description} — {e}")
        category = rule_based_category(description)

    # 3. Rule-based fallback
    fallback = rule_based_category(description)
    cache_category(description, fallback)
    return fallback


def categorize_transactions(transactions: list[dict]) -> list[dict]:
    """Categorize a list of transactions and return updated ones."""
    for txn in transactions:
        txn["category"] = categorize_transaction(txn)
    return transactions

