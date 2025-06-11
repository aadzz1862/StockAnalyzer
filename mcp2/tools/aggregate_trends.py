"""
Tool: aggregate_trends
"""
from agents.trend_aggregator import TrendAggregator

aggregator = TrendAggregator()

def aggregate_trends(articles: list[dict]) -> dict:
    """
    Produce {ticker → counts, avg_score}.
    """
    result = aggregator({"articles": articles})
    return result["trends"]
