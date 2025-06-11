"""
Tool: collect_news
"""
from agents.news_collector import NewsCollector

collector = NewsCollector()

def collect_news(tickers: list[str]) -> dict:
    """
    Collect the latest news articles for each ticker.
    Returns { tickers, articles }.
    """
    return collector({"tickers": tickers, "articles": []})
