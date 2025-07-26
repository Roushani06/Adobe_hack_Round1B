import spacy
import nltk
from nltk.corpus import stopwords
from collections import Counter

class PersonaAnalyzer:
    def __init__(self, persona, job_desc):
        self._download_nltk_resources()
        self.nlp = spacy.load("en_core_web_sm")
        self.stop_words = set(stopwords.words('english'))
        self.keywords = self._extract_keywords(job_desc['task'])
        self.persona = persona
        self.job_desc = job_desc

    def _download_nltk_resources(self):
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)

    def rank(self, sections, doc_title):
        ranked = []
        for section in sections:
            score = self._score(section['text'])  # Accessing 'text' field
            ranked.append({
                "document": doc_title,
                "section_title": self._title(section['text']),
                "page": section['page'],
                "importance_rank": score
            })
        return sorted(ranked, key=lambda x: x['importance_rank'], reverse=True)

    def refine(self, text):
        sentences = nltk.sent_tokenize(text)
        return ' '.join(sentences[:3])

    def _extract_keywords(self, text):
        doc = self.nlp(text.lower())
        return Counter([
            token.lemma_ for token in doc
            if not token.is_stop and not token.is_punct and token.is_alpha
        ])

    def _score(self, text):
        text_keywords = self._extract_keywords(text)
        return len(set(self.keywords) & set(text_keywords))

    def _title(self, text):
        first_sentence = text.split('.')[0][:50]
        return first_sentence + "..." if len(first_sentence) == 50 else first_sentence