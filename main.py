# main.py

from langgraph.graph import StateGraph
from agents.news_collector import NewsCollector
from agents.pre_cleaner import PreCleaner
from agents.entity_extractor import EntityExtractor
from agents.sentiment_analyzer import SentimentAnalyzer
from agents.trend_aggregator import TrendAggregator
from agents.reporter import Reporter  # <--- NEW: import Reporter with Llama support

from typing import TypedDict, List, Dict, Any

# 🧩 Updated State Schema: includes llama_summary
class StockAnalyzerState(TypedDict):
    tickers: List[str]
    articles: List[Dict[str, Any]]
    trends: Dict[str, Dict[str, Any]]
    report: str
    llama_summary: str  # <--- NEW field for Llama summary

# 1️⃣ Initialize agents
collector = NewsCollector()
precleaner = PreCleaner()
entity_extractor = EntityExtractor()
sentiment_analyzer = SentimentAnalyzer()
trend_aggregator = TrendAggregator()
reporter = Reporter(use_llama=True)  # <--- NEW: Enable Llama in Reporter

# 2️⃣ Create LangGraph with State Schema
graph = StateGraph(StockAnalyzerState)

# 3️⃣ Add Nodes
graph.add_node("collect", collector)
graph.add_node("clean", precleaner)
graph.add_node("extract", entity_extractor)
graph.add_node("sentiment", sentiment_analyzer)
graph.add_node("aggregate", trend_aggregator)
graph.add_node("reporter", reporter)

# 4️⃣ Connect Nodes
graph.add_edge("collect", "clean")
graph.add_edge("clean", "extract")
graph.add_edge("extract", "sentiment")
graph.add_edge("sentiment", "aggregate")
graph.add_edge("aggregate", "reporter")

# 5️⃣ Set Entry and Finish Points
graph.set_entry_point("collect")
graph.set_finish_point("reporter")

# 6️⃣ Compile the graph
app = graph.compile()

# 7️⃣ Run the graph
if __name__ == "__main__":
    initial_state = {
        "tickers": ["AAPL", "MSFT", "GOOGL"],
        "articles": [],
        "trends": {},
        "report": "",
        "llama_summary": ""  # <--- Initialize llama_summary
    }
    output = app.invoke(initial_state)
    print(output["report"])  # <--- Print the markdown report
    print("\n\n---- Llama 3 Summary ----\n")
    print(output["llama_summary"])  # <--- Print the Llama summary
