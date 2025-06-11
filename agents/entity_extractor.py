# agents/entity_extractor.py

import spacy

class EntityExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")

    def extract_entities(self, text):
        doc = self.nlp(text)
        entities = []
        for ent in doc.ents:
            if ent.label_ == "ORG":  # Organizations like companies
                entities.append(ent.text)
        return list(set(entities))  # remove duplicates

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

