# agents/sentiment_analyzer.py

from transformers import pipeline
import re

class SentimentAnalyzer:
    def __init__(self):
        """Try to load FinBERT; fall back to simple rule-based sentiment."""
        try:
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="./models/finbert",
                tokenizer="./models/finbert"
            )
            self.use_model = True
        except Exception:
            self.use_model = False
            self.positive_words = {"good", "great", "positive", "up", "gain"}
            self.negative_words = {"bad", "poor", "negative", "down", "loss"}

    def analyze_sentiment(self, text):
        if not text.strip():
            return {"label": "neutral", "score": 0.0}
        
        if self.use_model:
            result = self.sentiment_pipeline(text[:512], top_k=None)
            probs = {r['label'].lower(): r['score'] for r in result}
            positive = probs.get('positive', 0.0)
            negative = probs.get('negative', 0.0)
            neutral = probs.get('neutral', 0.0)
            sentiment_score = round(positive - negative, 3)
            label = max(probs, key=probs.get)
        else:
            tokens = re.findall(r"\b\w+\b", text.lower())
            pos_count = sum(word in self.positive_words for word in tokens)
            neg_count = sum(word in self.negative_words for word in tokens)
            sentiment_score = pos_count - neg_count
            if sentiment_score > 0:
                label = "positive"
            elif sentiment_score < 0:
                label = "negative"
            else:
                label = "neutral"

        return {
            "label": label,
            "score": sentiment_score
        }

    def __call__(self, state):
        articles = state.get("articles", [])
        analyzed_articles = []

        for article in articles:
            content = article.get("content", "") or ""
            sentiment = self.analyze_sentiment(content)
            analyzed_articles.append({
                **article,
                "sentiment": sentiment
            })

        return {
            **state,
            "articles": analyzed_articles
        }

