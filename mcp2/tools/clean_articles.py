"""
Tool: clean_articles
"""
from agents.pre_cleaner import PreCleaner

cleaner = PreCleaner()

def clean_articles(articles: list[dict]) -> list[dict]:
    """
    Remove obvious duplicates and strip boiler‑plate HTML.
    """
    result = cleaner({"articles": articles})
    return result["articles"]          # PreCleaner wraps inside result["articles"]
