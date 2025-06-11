import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class NewsCollector:
    def __init__(self, api_key=None):
        # Load API key from argument or environment
        self.api_key = api_key or os.getenv("NEWSAPI_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided either as a parameter or in the .env file.")

    def __call__(self, state):
        tickers = state.get("tickers", [])
        query = " OR ".join(tickers)
        url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&pageSize=10&apiKey={self.api_key}"

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching news: {response.status_code} {response.text}")
            return {
                **state,
                "articles": []
            }

        data = response.json()
        articles = data.get("articles", [])
        return {
            **state,
            "articles": articles
        }
