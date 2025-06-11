import sys, os, sys
from fastmcp import FastMCP

# so we can import agents from project root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# import wrapper functions
from tools.collect_news      import collect_news
from tools.clean_articles    import clean_articles
from tools.extract_entities  import extract_entities
from tools.analyze_sentiment import analyze_sentiment
from tools.aggregate_trends  import aggregate_trends
from tools.generate_report   import generate_report

mcp = FastMCP("stock_analyzer_mcp")

# ── register each tool by decorating the func on‑the‑fly ──
mcp.add_tool(mcp.tool(name="collect_news")(collect_news))
mcp.add_tool(mcp.tool(name="clean_articles")(clean_articles))
mcp.add_tool(mcp.tool(name="extract_entities")(extract_entities))
mcp.add_tool(mcp.tool(name="analyze_sentiment")(analyze_sentiment))
mcp.add_tool(mcp.tool(name="aggregate_trends")(aggregate_trends))
mcp.add_tool(mcp.tool(name="generate_report")(generate_report))
# ----------------------------------------------------------

if __name__ == "__main__":
    print("🚀 Stock‑Analyzer MCP server running …", file=sys.stderr)
    mcp.run(transport="stdio")
