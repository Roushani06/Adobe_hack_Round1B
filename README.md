# Persona-Driven Document Intelligence

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python version">
  <img src="https://img.shields.io/badge/spaCy-3.6+-orange.svg" alt="spaCy version">
  <img src="https://img.shields.io/badge/CPU%20Only-✓-green.svg" alt="CPU Only">
</div>

## 📌 Overview

An intelligent document analysis system that extracts and prioritizes relevant sections from documents based on specific user personas and their tasks.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip package manager

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/persona-doc-intel.git
cd persona-doc-intel

# Remove the existing virtual environment (if any)
Remove-Item -Recurse -Force venv

# Create and activate virtual environment
python -m venv venv

# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install --no-cache-dir numpy==1.24.0
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt stopwords
```

### Running the Application
```bash
python main.py
```

## 📁 File Structure
```
persona-doc-intel/
├── input/               # Input documents
│   ├── document1.pdf    # Sample document
│   └── input.json       # Configuration
├── output/              # Output JSON
├── src/                 # Source code
│   ├── document_processor.py
│   ├── persona_analyzer.py
│   └── utils.py
├── main.py              # Main script
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## 🛠️ Technologies Used
- **spaCy**: Natural Language Processing
- **NLTK**: Text Processing
- **PDFMiner.six**: PDF Text Extraction
- **Python 3.9+**: Core Programming Language

## 📋 Features
- Document section extraction
- Persona-based analysis
- Relevance scoring
- Section ranking
- Text refinement

## 📄 Input Format
The system expects input in JSON format with the following structure:
```json
{
  "documents": [
    {
      "filename": "document1.pdf",
      "title": "Document Title"
    }
  ],
  "persona": {
    "role": "Travel Planner"
  },
  "job_to_be_done": {
    "task": "Plan a trip for 4 days"
  }
}
```

## 📤 Output Format
The system generates a JSON output with:
- Metadata about processing
- Ranked extracted sections
- Refined subsection analysis

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments
- spaCy community for NLP tools
- NLTK team for text processing capabilities
- PDFMiner.six developers for PDF