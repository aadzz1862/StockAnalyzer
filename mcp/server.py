# mcp/server.py

from fastapi import FastAPI
from pydantic import BaseModel
from mcp.controller import run_pipeline  # Import the controller function

# Initialize FastAPI app
app = FastAPI(
    title="MCP - Model Context Protocol",
    description="An MCP Server to orchestrate Agents, Models, and Data Systems.",
    version="0.1.0"
)

# Input Schema
class PipelineRequest(BaseModel):
    tickers: list[str]

# Output Schema
class PipelineResponse(BaseModel):
    report: str
    llama_summary: str
    total_articles: int

# Health Check Endpoint
@app.get("/")
def root():
    return {"message": "MCP Server is running 🚀"}

# Main Pipeline Endpoint
@app.post("/run_pipeline", response_model=PipelineResponse)
def run_pipeline_endpoint(request: PipelineRequest):
    """
    Run the full news analysis pipeline.
    """
    output = run_pipeline(request.tickers)
    
    return PipelineResponse(
        report=output.get("report", ""),
        llama_summary=output.get("llama_summary", ""),
        total_articles=len(output.get("articles", []))
    )
