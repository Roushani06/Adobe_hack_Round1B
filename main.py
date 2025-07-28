import os
import json
from datetime import datetime
from src.document_processor import DocumentProcessor
from src.persona_analyzer import PersonaAnalyzer

def process_collection(collection_path, collection_name):
    # Find config file in collection directory
    config_files = [f for f in os.listdir(collection_path) if f.endswith('.json') and f != 'output.json']
    if not config_files:
        print(f"No config file found in {collection_path}")
        return
    
    config_path = os.path.join(collection_path, config_files[0])
    
    # Load configuration
    with open(config_path) as f:
        config = json.load(f)
    
    # Initialize components
    processor = DocumentProcessor()
    analyzer = PersonaAnalyzer(config['persona'], config['job_to_be_done'])
    
    # Process documents
    results = {
        "metadata": {
            "collection": collection_name,
            "input_documents": [doc['filename'] for doc in config['documents']],
            "persona": config['persona']['role'],
            "job_to_be_done": config['job_to_be_done']['task'],
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }
    
    pdfs_dir = os.path.join(collection_path, 'pdfs')
    for doc in config['documents']:
        filepath = os.path.join(pdfs_dir, doc['filename'])
        if not os.path.exists(filepath):
            print(f"Warning: File {filepath} not found, skipping")
            continue
            
        sections = processor.process(filepath)
        ranked_sections = analyzer.rank(sections, doc['title'])
        
        # Add top sections to results
        results['extracted_sections'].extend(ranked_sections[:5])
        
        # Add refined text for analysis
        for section in ranked_sections[:3]:
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
    
    return results

def main():
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Process each collection in input directory
    for collection_name in os.listdir('input'):
        collection_path = os.path.join('input', collection_name)
        if not os.path.isdir(collection_path):
            continue
            
        print(f"Processing collection: {collection_name}")
        results = process_collection(collection_path, collection_name)
        
        if results:
            # Save results with collection name
            output_path = os.path.join('output', f"{collection_name}.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"Saved results to {output_path}")

if __name__ == "__main__":
    main()