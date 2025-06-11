import sqlite3
import json
import os
from datetime import datetime

# Define where your database will be
DB_PATH = os.path.join("data", "raw_news.db")

def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create table for raw news articles
    c.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            title TEXT,
            url TEXT,
            published_at TEXT,
            content TEXT,
            source TEXT,
            entities TEXT,         -- JSON list
            sentiment_label TEXT,
            sentiment_score REAL,
            raw_json TEXT           -- Full raw article JSON
        )
    """)
    
    # Create table for daily summaries
    c.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            report TEXT,
            llama_summary TEXT,
            trends TEXT             -- JSON of trend aggregation
        )
    """)
    
    conn.commit()
    conn.close()

def save_articles(tickers, articles):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    for article in articles:
        c.execute("""
            INSERT INTO articles (
                ticker, title, url, published_at, content, source, entities,
                sentiment_label, sentiment_score, raw_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            json.dumps(tickers),
            article.get("title", ""),
            article.get("url", ""),
            article.get("publishedAt", ""),
            article.get("content", ""),
            article.get("source", ""),
            json.dumps(article.get("entities", [])),
            article.get("sentiment", {}).get("label", ""),
            article.get("sentiment", {}).get("score", 0.0),
            json.dumps(article)
        ))
    
    conn.commit()
    conn.close()

def save_summary(report, llama_summary, trends):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        INSERT INTO summaries (date, report, llama_summary, trends)
        VALUES (?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d"),
        report,
        llama_summary,
        json.dumps(trends)
    ))
    
    conn.commit()
    conn.close()

def fetch_recent_articles(limit=20):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT title, url, published_at, content, sentiment_label, sentiment_score
        FROM articles
        ORDER BY published_at DESC
        LIMIT ?
    """, (limit,))
    
    rows = c.fetchall()
    conn.close()
    return rows

def fetch_trend_history():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT date, trends
        FROM summaries
        ORDER BY date DESC
        LIMIT 30
    """)
    
    rows = c.fetchall()
    conn.close()
    return rows
