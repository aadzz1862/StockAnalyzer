# agents/entity_extractor.py

import re
import spacy

class EntityExtractor:
    def __init__(self):
        """Load spaCy model if available, otherwise fall back to regex."""
        try:
            self.nlp = spacy.load("en_core_web_lg")
            self.use_spacy = True
        except Exception:
            # Fall back when the large model isn't installed
            self.nlp = None
            self.use_spacy = False

    def extract_entities(self, text):
        if self.use_spacy:
            doc = self.nlp(text)
            entities = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
            return list(set(entities))  # remove duplicates

        # Simple regex fallback for potential ticker symbols
        return list(set(re.findall(r"\b[A-Z]{2,5}\b", text)))

    def __call__(self, state):
        articles = state.get("articles", [])
        enriched_articles = []

        for article in articles:
            content = article.get("content", "") or ""
            entities = self.extract_entities(content)
            enriched_articles.append({
                **article,  # Keep original fields
                "entities": entities  # Add extracted entities
            })

        return {
            **state,
            "articles": enriched_articles
        }

