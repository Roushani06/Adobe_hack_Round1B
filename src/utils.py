import re

def clean(text):
    """Basic text cleaning utility"""
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    return ' '.join(text.split()).strip()

def validate_json(input_json):
    """Validate input JSON structure"""
    required = ['documents', 'persona', 'job_to_be_done']
    if not all(field in input_json for field in required):
        raise ValueError("Invalid input JSON structure")
    return True