# document_processor.py
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from typing import List, Dict
import re

class DocumentProcessor:
    def __init__(self):
        self.heading_patterns = [
            r'^[A-Z][a-zA-Z\s]+:$',  # Title case with colon
            r'^[A-Z][A-Z\s]+$',      # All caps
            r'^\*\*.+\*\*$',         # Bold text
            r'^[IVX]+\.',            # Roman numerals
            r'^\d+\.\d+',            # Numbered sections
            r'^Top \d+',             # "Top 10" style
            r'^Best \w+'             # "Best X" style
        ]
        
    def process(self, filepath: str) -> List[Dict]:
        sections = []
        current_title = "Introduction"
        current_content = []
        current_page = 1
        
        for page_num, page_layout in enumerate(extract_pages(filepath), start=1):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    text = self._clean(element.get_text())
                    if not text:
                        continue
                    
                    # Check if this is a heading
                    if self._is_heading(text):
                        # Save previous section
                        if current_content:
                            sections.append({
                                "title": current_title,
                                "content": " ".join(current_content),
                                "page": current_page
                            })
                        
                        # Start new section
                        current_title = text.strip()
                        current_content = []
                        current_page = page_num
                    else:
                        current_content.append(text)
        
        # Add the last section
        if current_content:
            sections.append({
                "title": current_title,
                "content": " ".join(current_content),
                "page": current_page
            })
        
        return [s for s in sections if len(s['content'].split()) >= 30]

    def _is_heading(self, text: str) -> bool:
        text = text.strip()
        if any(re.match(pattern, text) for pattern in self.heading_patterns):
            return True
        if len(text.split()) <= 8 and (text.isupper() or text.istitle()):
            return True
        return False

    def _clean(self, text: str) -> str:
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text