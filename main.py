import os
import json
from datetime import datetime
from src.document_processor import DocumentProcessor
from src.persona_analyzer import PersonaAnalyzer

def main():
    # Load configuration
    input_path = os.path.join('input', 'input.json')
    with open(input_path) as f:
        config = json.load(f)
    
    # Initialize components
    processor = DocumentProcessor()
    analyzer = PersonaAnalyzer(config['persona'], config['job_to_be_done'])
    
    # Process documents
    results = {
        "metadata": {
            "input_documents": [doc['filename'] for doc in config['documents']],
            "persona": config['persona']['role'],
            "job_to_be_done": config['job_to_be_done']['task'],
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }
    
    for doc in config['documents']:
        filepath = os.path.join('input', doc['filename'])
        sections = processor.process(filepath)
        ranked_sections = analyzer.rank(sections, doc['title'])
        
        # Add top sections to results
        results['extracted_sections'].extend(ranked_sections[:5])
        
        # Add refined text for analysis
        for section in ranked_sections[:3]:
            # Get the original text from the sections list
            original_section = next(
                s for s in sections 
                if s['page'] == section['page']
            )
            refined = analyzer.refine(original_section['text'])
            results['subsection_analysis'].append({
                "document": doc['filename'],
                "refined_text": refined,
                "page_number": section['page']
            })
    
    # Save results
    os.makedirs('output', exist_ok=True)
    output_path = os.path.join('output', 'output.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()