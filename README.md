
# 📊 StockAnalyzer  
**Multi‑agent, local‑first market‑sentiment platform with LangGraph + FinBERT + Llama 3, dual MCP servers, vector search, and Streamlit dashboard**

---

## ✨ Features
| Layer                  | Details                                                                                                     |
|------------------------|--------------------------------------------------------------------------------------------------------------|
| **Agents**             | `NewsCollector → PreCleaner → EntityExtractor → SentimentAnalyzer → TrendAggregator → Reporter`              |
| **LLMs / Models**      | • `ProsusAI/finbert` for finance‑tuned sentiment<br>• Local **Llama‑3 8B** (quantised via **Ollama**) for reporting |
| **Pipelines**          | 1. **LangGraph** standalone runner (`main.py`)<br>2. **MCP‑FastAPI** server (`mcp/`) exposed as REST & CLI<br>3. **Anthropic MCP (`fastmcp`)** server (`mcp2/`) discoverable by Claude Desktop |
| **Storage**            | • SQLite (`data/raw_news.db`) ‑ raw articles / summaries<br>• ChromaDB (`data/embeddings/`) ‑ MiniLM vectors |
| **UI / Clients**       | • Streamlit dashboard (`dashboard.py`)<br>• `fastmcp` CLI pipes<br>• Claude Desktop (via MCP) |
| **Local‑first**        | Runs entirely on CPU; no OpenAI / cloud costs                                                               |

---

## 🗂️ Repo Structure
```

StockAnalyzer/
├─ agents/                  # core agent logic
├─ models/finbert/          # local FinBERT weights
├─ data/
│  ├─ raw\_news.db           # SQLite DB
│  └─ embeddings/           # Chroma vector store
├─ mcp/                     # FastAPI + LangGraph MCP server (REST)
├─ mcp2/                    # Anthropic "fastmcp" server (stdio / Claude)
│  ├─ tools/                # thin wrappers that expose agents as tools
│  └─ utils/                # db helpers reused from mcp
├─ dashboard.py             # Streamlit dashboard
├─ main.py                  # LangGraph runner (no DB)
└─ README.md

````

---

## 🚀 Quick‑start

```bash
git clone https://github.com/<you>/StockAnalyzer.git
cd StockAnalyzer
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
````

Create **`.env`** for NewsAPI key & others:

```env
NEWSAPI_KEY=xxxxxxxxxxxxxxxx
```

### 1. LangGraph (one‑shot)

```bash
python main.py
```

### 2. FastAPI MCP server (REST)

```bash
uvicorn mcp.server:app --reload
# Swagger UI: http://127.0.0.1:8000/docs
```

### 3. Anthropic `fastmcp` server (Claude Desktop / CLI)

```bash
python mcp2/server.py            # runs on stdio
fastmcp list mcp2/server.py      # see tools
fastmcp call mcp2/server.py collect_news --json '{"tickers":["AAPL"]}' --pretty
```

*(Claude Desktop → click 🔌 → select **stock\_analyzer\_mcp** and instruct it in natural language.)*

### 4. Streamlit Dashboard

```bash
streamlit run dashboard.py
```

---

## 📐 Agent Details

| Agent                 | Role / Libs                                                     |
| --------------------- | --------------------------------------------------------------- |
| **NewsCollector**     | Hits NewsAPI (RSS, GNews ready) with exponential back‑off.      |
| **PreCleaner**        | `readability-lxml`, sim‑hash duplicate removal.                 |
| **EntityExtractor**   | `spaCy en_core_web_lg` + simple ORG filter → potential tickers. |
| **SentimentAnalyzer** | HF pipeline with local **FinBERT** (`ProsusAI/finbert`).        |
| **TrendAggregator**   | `pandas`, `numpy`; z‑score, per‑ticker aggregates.              |
| **Reporter**          | Markdown report + Llama‑3 summary via **Ollama** HTTP API.      |

---

## 💾 Data Persistence

* **SQLite** `articles` table – title, url, content, entities, sentiment, JSON blob.
* **SQLite** `summaries` table – markdown report + llama summary (+ ISO date).
* **ChromaDB** – MiniLM embeddings keyed by article URL for semantic lookup / RAG.

---

## 🔗 Using the Tools from CLI (pipes)

```bash
fastmcp call mcp2/server.py collect_news      --json '{"tickers":["AAPL","MSFT"]}' |
fastmcp call mcp2/server.py clean_articles    --stdin |
fastmcp call mcp2/server.py extract_entities  --stdin |
fastmcp call mcp2/server.py analyze_sentiment --stdin |
fastmcp call mcp2/server.py aggregate_trends  --stdin |
fastmcp call mcp2/server.py generate_report   --stdin --pretty
```

---

## 📈 Dashboard Preview

| Section             | What it shows                                    |
| ------------------- | ------------------------------------------------ |
| **Markdown Report** | Daily ticker breakdown (counts, avg score).      |
| **Llama Summary**   | 200‑word prose summary.                          |
| **Sentiment Chart** | Matplotlib bar of positive / negative / neutral. |
| **Download**        | Saves `report_YYYY‑MM‑DD.md`.                    |

---

## 🛠️ Development Notes

* Python 3.11, no Conda.
* Tested on Windows 11 + WSL, Ubuntu 22, macOS 14 (Apple Silicon).
* FinBERT and Llama 3 are loaded once and cached.
* Vector search optional; turn off by commenting `mcp/vector_utils.py` calls.

---

## 🏆 Impact

* End‑to‑end pipeline generates actionable sentiment brief in **< 30 s** on laptop CPU.
* **Zero cloud costs** (all local models).
* MCP integration lets **Claude** or any tool‑calling LLM orchestrate analysis autonomously.
* Modular design—drop‑in new agents (e.g., price scraper) or swap models easily.

---

## 📜 License

MIT — use, fork, star ⭐, enjoy!

```

> Save the block above as **`README.md`** at repo root.  
> Feel free to tweak badges, add screenshots, or redact keys before publishing.
```
