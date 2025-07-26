from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextBoxHorizontal
import re
import unicodedata

class DocumentProcessor:
    def process(self, filepath):
        sections = []
        try:
            for page_num, page_layout in enumerate(extract_pages(filepath), start=1):
                for element in page_layout:
                    if isinstance(element, (LTTextBoxHorizontal, LTTextContainer)):
                        text = self._clean(element.get_text())
                        if text:
                            sections.append({
                                "text": text,  # Using 'text' as the consistent field name
                                "page": page_num,
                                "font_size": self._get_font_size(element)
                            })
        except Exception as e:
            print(f"Error processing {filepath}: {str(e)}")
        return sections

    def _clean(self, text):
        text = unicodedata.normalize('NFKD', text)
        text = re.sub(r'[\u2022\u2023\u25E6\u2043\u00B7•‣◦]', '', text)
        text = re.sub(r'[^\w\s.,;:!?\'"\-()]', '', text)
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        return ' '.join(text.split()).strip()

    def _get_font_size(self, element):
        try:
            return element._objs[0].size
        except:
            return 12