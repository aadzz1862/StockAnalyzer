"""
Tool: analyze_sentiment
"""
from agents.sentiment_analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer()

def analyze_sentiment(articles: list[dict]) -> list[dict]:
    """
    FinBERT sentiment per article → adds .sentiment{label,score}.
    """
    result = analyzer({"articles": articles})
    return result["articles"]
