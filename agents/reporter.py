# agents/reporter.py

import requests
import json

class Reporter:
    def __init__(self, use_llama=False):
        self.use_llama = use_llama
        self.ollama_url = "http://localhost:11434/api/generate"

    def generate_markdown_report(self, trends):
        if not trends:
            return "# Daily Market Sentiment Report\n\nNo significant data today."

        report = "# 📈 Daily Market Sentiment Report\n\n"
        for ticker, data in trends.items():
            report += f"## {ticker}\n"
            report += f"- **Total Articles**: {data['total_articles']}\n"
            report += f"- **Positive**: {data['positive']} | **Negative**: {data['negative']} | **Neutral**: {data['neutral']}\n"
            report += f"- **Average Sentiment Score**: {data['avg_sentiment_score']}\n\n"

        return report

    def generate_prompt(self, trends):
        prompt = "Summarize today's market sentiment for the following stocks:\n\n"
        for ticker, data in trends.items():
            prompt += (
                f"Ticker: {ticker}\n"
                f"- Total Articles: {data['total_articles']}\n"
                f"- Positive: {data['positive']}, Negative: {data['negative']}, Neutral: {data['neutral']}\n"
                f"- Average Sentiment Score: {data['avg_sentiment_score']}\n\n"
            )
        prompt += "Write a concise, professional market summary based on this data."
        return prompt

    def call_llama(self, prompt):
        payload = {
            "model": "llama3",
            "prompt": prompt,
            "temperature": 0.7,
            "max_tokens": 500
        }
        try:
            # Use streaming for NDJSON response
            response = requests.post(self.ollama_url, json=payload, stream=True)
            response.raise_for_status()

            full_response = ""
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    data = json.loads(line)
                    full_response += data.get("response", "")

            return full_response.strip()
        except Exception as e:
            print(f"Error contacting Llama 3: {e}")
            return "Failed to generate Llama summary."

    def __call__(self, state):
        trends = state.get("trends", {})
        markdown_report = self.generate_markdown_report(trends)

        llama_summary = ""
        if self.use_llama:
            prompt = self.generate_prompt(trends)
            llama_summary = self.call_llama(prompt)

        return {
            "tickers": state["tickers"],
            "articles": state["articles"],
            "trends": state["trends"],
            "report": markdown_report,
            "llama_summary": llama_summary  # <--- NEW
        }
