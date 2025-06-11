# agents/trend_aggregator.py

from collections import defaultdict
import numpy as np

class TrendAggregator:
    def __init__(self):
        pass

    def aggregate_trends(self, articles):
        ticker_sentiments = defaultdict(lambda: {
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "sentiment_scores": []
        })

        for article in articles:
            entities = article.get("entities", [])
            sentiment = article.get("sentiment", {})
            label = sentiment.get("label", "neutral").lower()
            score = sentiment.get("score", 0.0)

            for entity in entities:
                if entity.isupper() and 1 < len(entity) <= 5:
                    ticker_sentiments[entity][label] += 1
                    ticker_sentiments[entity]["sentiment_scores"].append(score)

        # Final trend calculation
        trend_summary = {}
        for ticker, data in ticker_sentiments.items():
            total_articles = sum([data["positive"], data["negative"], data["neutral"]])
            avg_sentiment = (
                np.mean(data["sentiment_scores"]) if data["sentiment_scores"] else 0.0
            )

            trend_summary[ticker] = {
                "total_articles": total_articles,
                "positive": data["positive"],
                "negative": data["negative"],
                "neutral": data["neutral"],
                "avg_sentiment_score": round(avg_sentiment, 3)
            }

        return trend_summary

    def __call__(self, state):
        articles = state.get("articles", [])
        trend_data = self.aggregate_trends(articles)

        return {
            **state,
            "trends": trend_data
        }
