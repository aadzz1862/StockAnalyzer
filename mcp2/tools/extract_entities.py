"""
Tool: extract_entities
"""
from agents.entity_extractor import EntityExtractor

extractor = EntityExtractor()

def extract_entities(articles: list[dict]) -> list[dict]:
    """
    Add .entities[] to each article (ORG, ticker, etc.).
    """
    result = extractor({"articles": articles})
    return result["articles"]
