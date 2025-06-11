# agents/sentiment_analyzer.py

from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        # Load FinBERT from local path
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="./models/finbert",      # Load local model
            tokenizer="./models/finbert"
        )

    def analyze_sentiment(self, text):
        if not text.strip():
            return {"label": "neutral", "score": 0.0}
        
        # Get all scores for each label
        result = self.sentiment_pipeline(text[:512], top_k=None)


        # Map label probabilities
        probs = {r['label'].lower(): r['score'] for r in result}
        positive = probs.get('positive', 0.0)
        negative = probs.get('negative', 0.0)
        neutral = probs.get('neutral', 0.0)

        # Compute sentiment score: positive - negative
        sentiment_score = round(positive - negative, 3)

        # Choose label with highest probability
        label = max(probs, key=probs.get)

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

