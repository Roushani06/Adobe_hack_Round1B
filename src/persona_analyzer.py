# src/persona_analyzer.py
import spacy
import nltk
from nltk.corpus import stopwords
from collections import Counter

class PersonaAnalyzer:
    def __init__(self, persona, job_desc):
        self._download_nltk_resources()
        self.nlp = spacy.load("en_core_web_sm")
        self.stop_words = set(stopwords.words('english'))
        self.persona = persona
        self.job_desc = job_desc
        self.keywords = self._extract_keywords(job_desc['task'])
        
        # Define persona-specific scoring rules
        self.scoring_rules = {
            "Travel Planner": self._score_travel,
            "HR professional": self._score_hr,
            "Food Contractor": self._score_food,
            "default": self._score_default
        }

    def _download_nltk_resources(self):
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)

    def rank(self, sections, doc_title):
        ranked = []
        for section in sections:
            text = section['text']
            if len(text.split()) < 15:  # Skip very short sections
                continue
                
            score = self._score_section(text)
            if score == 0:  # Skip irrelevant sections
                continue
                
            ranked.append({
                "document": doc_title,
                "section_title": self._create_title(text),
                "page": section['page'],
                "importance_rank": score,
                "raw_text": text  # Store for refinement
            })
        
        # Sort by score and take top sections
        return sorted(ranked, key=lambda x: x['importance_rank'], reverse=True)

    def refine(self, text):
        sentences = nltk.sent_tokenize(text)
        # Return first 3-5 most informative sentences
        return ' '.join(sentences[:min(5, len(sentences))])

    def _extract_keywords(self, text):
        doc = self.nlp(text.lower())
        return Counter([
            token.lemma_ for token in doc
            if not token.is_stop and not token.is_punct and token.is_alpha
        ])

    def _score_section(self, text):
        # Get the appropriate scoring function for the persona
        score_fn = self.scoring_rules.get(self.persona['role'], self.scoring_rules['default'])
        return score_fn(text)

    def _score_travel(self, text):
        travel_keywords = {
            'trip', 'itinerary', 'hotel', 'restaurant', 'activity', 'guide',
            'plan', 'visit', 'experience', 'adventure', 'explore', 'recommend',
            'attraction', 'nightlife', 'packing', 'travel', 'group', 'friends'
        }
        text_keywords = self._extract_keywords(text)
        
        # Base score from keyword matches
        score = sum(text_keywords[term] for term in travel_keywords if term in text_keywords)
        
        # Bonus for practical information
        if any(term in text.lower() for term in {'tip', 'trick', 'advice', 'suggestion'}):
            score += 3
            
        # Bonus for group-related content
        if any(term in text.lower() for term in {'group', 'friends', 'multiple', 'together'}):
            score += 2
            
        return score

    def _score_hr(self, text):
        hr_keywords = {'form', 'fillable', 'signature', 'document', 'field', 'compliance'}
        text_keywords = self._extract_keywords(text)
        return sum(text_keywords[term] for term in hr_keywords if term in text_keywords)

    def _score_food(self, text):
        food_keywords = {'recipe', 'ingredient', 'vegetarian', 'gluten-free', 'buffet', 'dish'}
        text_keywords = self._extract_keywords(text)
        return sum(text_keywords[term] for term in food_keywords if term in text_keywords)

    def _score_default(self, text):
        text_keywords = self._extract_keywords(text)
        return len(set(self.keywords) & set(text_keywords))

    def _create_title(self, text):
        # Get the most informative part of the text for the title
        doc = self.nlp(text)
        
        # Try to find a heading-like sentence
        for sent in doc.sents:
            if len(sent.text.split()) > 5 and sent.text.endswith(':'):
                return sent.text[:-1]  # Remove trailing colon
            if len(sent.text.split()) > 5 and any(tok.is_title for tok in sent):
                return sent.text
        
        # Fallback to first sentence
        first_sent = next(doc.sents).text
        return first_sent[:100] + ("..." if len(first_sent) > 100 else "")