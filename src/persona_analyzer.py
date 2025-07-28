# persona_analyzer.py
import spacy
from typing import List, Dict
import re

class PersonaAnalyzer:
    def __init__(self, persona: Dict, job_desc: Dict):
        self.nlp = spacy.load("en_core_web_sm")
        self.persona = persona
        self.job_desc = job_desc
        self._setup_keywords()
        
    def _setup_keywords(self):
        self.trip_keywords = {
            'itinerary', 'plan', 'schedule', '4 days', 'multi-day'
        }
        self.group_keywords = {
            'group', 'friends', 'college', '10 people', 'together'
        }
        self.activity_keywords = {
            'beach', 'nightlife', 'club', 'bar', 'adventure',
            'excursion', 'tour', 'activity', 'sightseeing'
        }
        self.city_keywords = {
            'Nice', 'Marseille', 'Cannes', 'Saint-Tropez', 'Antibes'
        }

    def rank(self, sections: List[Dict], doc_title: str) -> List[Dict]:
        ranked = []
        seen_titles = set()
        
        for section in sections:
            title = section['title'].strip()
            content = section['content']
            
            # Skip short sections and duplicates
            if len(content.split()) < 30 or title.lower() in seen_titles:
                continue
                
            seen_titles.add(title.lower())
            
            score = self._score_section(title, content)
            if score > 0:
                ranked.append({
                    "document": doc_title,
                    "section_title": title,
                    "page": section['page'],
                    "importance_rank": score,
                    "raw_text": content
                })
        
        # Return top 5 sections sorted by score
        return sorted(ranked, key=lambda x: x['importance_rank'], reverse=True)[:5]

    def refine(self, text: str) -> str:
        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]
        
        # Score sentences based on relevance
        scored = []
        for sent in sentences:
            score = 0
            score += 3 * sum(1 for kw in self.trip_keywords if kw.lower() in sent.lower())
            score += 3 * sum(1 for kw in self.group_keywords if kw.lower() in sent.lower())
            score += 2 * sum(1 for kw in self.activity_keywords if kw.lower() in sent.lower())
            score += sum(1 for kw in self.city_keywords if kw in sent)
            
            if score > 0:
                scored.append((score, sent))
        
        # Take top 3 scored sentences
        scored.sort(reverse=True)
        return " ".join([s for _, s in scored[:3]])

    def _score_section(self, title: str, content: str) -> float:
        text = f"{title.lower()} {content.lower()}"
        score = 0
        
        # Trip planning relevance
        score += 3 * sum(1 for kw in self.trip_keywords if kw in text)
        
        # Group relevance
        score += 3 * sum(1 for kw in self.group_keywords if kw in text)
        
        # Activity relevance
        score += 2 * sum(1 for kw in self.activity_keywords if kw in text)
        
        # City mentions
        score += sum(1 for kw in self.city_keywords if kw.lower() in text)
        
        # Boost for complete itineraries
        if "day 1" in text or "day 2" in text or "itinerary" in title.lower():
            score += 5
            
        return max(0, score)