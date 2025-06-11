# agents/pre_cleaner.py

from readability import Document
import hashlib

class PreCleaner:
    def __init__(self):
        self.seen_titles = set()  # to remove duplicate articles

    def strip_html(self, html_content):
        try:
            doc = Document(html_content)
            summary = doc.summary()  # cleaner HTML
            return summary
        except Exception:
            return ""

    def is_duplicate(self, title):
        # Simple hashing for duplicate detection
        hash_title = hashlib.md5(title.lower().encode()).hexdigest()
        if hash_title in self.seen_titles:
            return True
        self.seen_titles.add(hash_title)
        return False

    def __call__(self, state):
        articles = state.get("articles", [])
        cleaned_articles = []

        for article in articles:
            title = article.get("title", "")
            if not title or self.is_duplicate(title):
                continue  # Skip duplicates

            content = article.get("content", "") or ""
            cleaned_content = self.strip_html(content)

            cleaned_articles.append({
                "title": title,
                "url": article.get("url"),
                "publishedAt": article.get("publishedAt"),
                "content": cleaned_content,
                "source": article.get("source", {}).get("name", "")
            })

        # FIXED: Return full state
        return {
            **state,
            "articles": cleaned_articles
        }
