import json
import os

# Path to category cache file
CACHE_FILE = "data/category_cache.json"

# Initialize cache file if not present
if not os.path.exists(CACHE_FILE):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump({}, f)

def load_cache() -> dict:
    """Load the category cache from JSON file."""
    with open(CACHE_FILE, "r") as f:
        return json.load(f)

def save_cache(cache: dict):
    """Save the updated category cache."""
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def get_cached_category(description: str) -> str | None:
    """Return cached category if available."""
    cache = load_cache()
    return cache.get(description.strip())

def cache_category(description: str, category: str):
    """Cache the given description and its category."""
    description = description.strip()
    category = category.strip()

    cache = load_cache()
    cache[description] = category
    save_cache(cache)
