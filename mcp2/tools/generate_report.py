"""
Tool: generate_report
"""
from agents.reporter import Reporter

reporter = Reporter(use_llama=True)   # uses your local Llama‑3 via Ollama

def generate_report(trends: dict) -> dict:
    """
    Markdown + Llama summary from trend dict.
    Returns {report, llama_summary}.
    """
    state = {"trends": trends, "tickers": [], "articles": []}
    result = reporter(state)
    return {
        "report":        result["report"],
        "llama_summary": result["llama_summary"]
    }
