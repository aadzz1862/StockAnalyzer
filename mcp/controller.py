# mcp/controller.py

# Import your agents
from agents.news_collector import NewsCollector
from agents.pre_cleaner import PreCleaner
from agents.entity_extractor import EntityExtractor
from agents.sentiment_analyzer import SentimentAnalyzer
from agents.trend_aggregator import TrendAggregator
from agents.reporter import Reporter

# Import DB and Vector Utilities
from mcp import db_utils  # <-- Save to SQLite
from mcp.vector_utils import add_article_to_vectorstore, persist_vectorstore  # <-- Save to VectorDB

# Initialize all agents
collector = NewsCollector()
precleaner = PreCleaner()
entity_extractor = EntityExtractor()
sentiment_analyzer = SentimentAnalyzer()
trend_aggregator = TrendAggregator()
reporter = Reporter(use_llama=True)  # Use Llama for summarization

def run_pipeline(tickers: list[str]) -> dict:
    """
    Main orchestrator function for the Stock Analyzer.
    Takes a list of tickers and runs the complete pipeline.
    """

    # Initial empty state
    state = {
        "tickers": tickers,
        "articles": [],
        "trends": {},
        "report": "",
        "llama_summary": ""
    }

    # 1. Collect News
    state = collector(state)

    # 2. Clean Articles
    state = precleaner(state)

    # 3. Extract Entities
    state = entity_extractor(state)

    # 4. Sentiment Analysis
    state = sentiment_analyzer(state)

    # 5. Trend Aggregation
    state = trend_aggregator(state)

    # 6. Generate Report and Llama Summary
    state = reporter(state)

    # 7. Save articles to DB and Vector DB
    for article in state["articles"]:
        # Save to SQL DB
        db_utils.save_article(article)

        # Save to Vector Store
        add_article_to_vectorstore(
            article_id=article.get("url") or article.get("title"),  # Use URL or fallback to title
            text=article.get("content", ""),
            metadata={
                "tickers": ",".join(article.get("entities", [])),
                "publishedAt": article.get("publishedAt", ""),
                "source": article.get("source", "")
            }
        )

    # 8. Save summaries to DB
    db_utils.save_summary(
        report_text=state["report"],
        llama_summary_text=state["llama_summary"]
    )

    # 9. Persist Vector DB
    persist_vectorstore()

    # Return final output
    return state
