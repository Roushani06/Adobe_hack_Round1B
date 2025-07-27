# Adobe_hack_Round1B# Persona-Driven Document Intelligence

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
```bash
# Create and activate virtual environment
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

# Install dependencies
```bash
pip install --no-cache-dir numpy==1.24.0
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt stopwords
```
# Run 
```bash
python main.py
```

### File Structure
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
└── README.md            # This file
```