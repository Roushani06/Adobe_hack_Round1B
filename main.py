import os
import json
from datetime import datetime
from typing import Dict, List
from src.document_processor import DocumentProcessor
from src.persona_analyzer import PersonaAnalyzer

def process_collection(collection_path: str) -> Dict:
    # Load config
    config_files = [f for f in os.listdir(collection_path) if f.endswith('.json')]
    if not config_files:
        raise FileNotFoundError(f"No config file found in {collection_path}")
    
    with open(os.path.join(collection_path, config_files[0])) as f:
        config = json.load(f)
    
    # Initialize processors
    processor = DocumentProcessor()
    analyzer = PersonaAnalyzer(config['persona'], config['job_to_be_done'])
    
    # Prepare results structure
    results = {
        "metadata": {
            "input_documents": [doc['filename'] for doc in config['documents']],
            "persona": config['persona'],
            "job_to_be_done": config['job_to_be_done'],
            "processing_timestamp": datetime.now().isoformat(),
            "processing_metrics": {
                "total_sections": 0,
                "selected_sections": 0
            }
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }
    
    # Process documents
    pdfs_dir = os.path.join(collection_path, 'pdfs')
    all_ranked_sections = []
    
    for doc in config['documents']:
        filepath = os.path.join(pdfs_dir, doc['filename'])
        if not os.path.exists(filepath):
            print(f"Warning: File {filepath} not found, skipping")
            continue
        
        sections = processor.process(filepath)
        ranked_sections = analyzer.rank(sections, doc['title'])
        all_ranked_sections.extend(ranked_sections)
    
    results['metadata']['processing_metrics']['total_sections'] = len(all_ranked_sections)
    
    # Select top sections
    all_ranked_sections.sort(key=lambda x: x['importance_rank'], reverse=True)
    max_sections = max(5, len(all_ranked_sections) // 4)  # At least 5 or 25% of sections
    top_sections = all_ranked_sections[:max_sections]
    
    # Ensure minimum 3 sections if available
    if len(top_sections) < 3 and len(all_ranked_sections) >= 3:
        top_sections = all_ranked_sections[:3]
    
    results['metadata']['processing_metrics']['selected_sections'] = len(top_sections)
    
    # Prepare output
    for section in top_sections:
        results['extracted_sections'].append({
            "document": section['document'],
            "section_title": section['section_title'],
            "importance_rank": section['importance_rank'],
            "page_number": section['page']
        })
        
        refined = analyzer.refine(section['raw_text'])
        results['subsection_analysis'].append({
            "document": os.path.basename(section['document'].replace(' ', '_') + '.pdf'),
            "refined_text": refined,
            "page_number": section['page']
        })
    
    return results

def main():
    os.makedirs('output', exist_ok=True)
    
    # Process each collection
    for collection_name in sorted(os.listdir('input')):
        collection_path = os.path.join('input', collection_name)
        if not os.path.isdir(collection_path):
            continue
        
        print(f"\nProcessing collection: {collection_name}")
        
        try:
            results = process_collection(collection_path)
            
            # Determine output filename
            output_filename = f"{collection_name}.json"
            if 'challenge_info' in results['metadata']:
                challenge_id = results['metadata']['challenge_info']['challenge_id']
                output_filename = f"{challenge_id}_output.json"
            
            # Save results
            output_path = os.path.join('output', output_filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=4, ensure_ascii=False)
            
            # Print summary
            metrics = results['metadata']['processing_metrics']
            print(f"  - Processed {metrics['total_sections']} sections")
            print(f"  - Selected {metrics['selected_sections']} sections")
            print(f"  - Saved to {output_path}")
            
        except Exception as e:
            print(f"Error processing {collection_name}: {str(e)}")

if __name__ == "__main__":
    print("Starting document processing...")
    main()
    print("\nProcessing completed.")