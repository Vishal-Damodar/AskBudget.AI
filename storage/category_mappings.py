# app/storage.py

import json
import os

MAPPING_FILE = "data\category_mappings.json"
def load_mappings():
    """Load the vendor-category mapping file."""
    if not os.path.exists(MAPPING_FILE):
        return {}
    try:
        with open(MAPPING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
            return {}

def save_mappings(mappings: dict):
    with open(MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(mappings, f, indent=4)        

def get_user_category(vendor: str):
    mappings = load_mappings()
    return mappings.get(vendor.strip())

def set_user_category(vendor: str, category: str):
    mappings = load_mappings()
    mappings[vendor.strip()] = category.strip()
    save_mappings(mappings)