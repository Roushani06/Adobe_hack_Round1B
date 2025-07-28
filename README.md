# Persona-Driven Document Intelligence

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python version">
  <img src="https://img.shields.io/badge/spaCy-3.6+-orange.svg" alt="spaCy version">
  <img src="https://img.shields.io/badge/CPU%20Only-✓-green.svg" alt="CPU Only">
</div>

## 📌 Overview

An intelligent document analysis system that extracts and prioritizes relevant sections from documents based on specific user personas and their tasks.



## 👨‍💻 Team - ZenCode

Roushani Kumari(Leader) – [GitHub](https://github.com/Roushani06)  
Snigdha Kumar – [GitHub](https://github.com/snigdhaydv27)



## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip package manager

### Installation

#### Option 1: Using Virtual Environment
```bash
# Clone repository
git clone https://github.com/snigdhaydv27/Adobe_hack_Round1B.git
cd Adobe_hack_Round1B

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

```bash
# Running the Application
python main.py
```

#### Option 2: Using Docker
```bash
# Build Docker image
docker build -t pdf_analyser:latest .

# Run with volume mounts for input and output
docker run -v ${PWD}/input:/app/input -v ${PWD}/output:/app/output pdf_analyser:latest
```

## 📁 File Structure
```
Adobe_hack_Round1B/
├── input/
│   ├── collection1/          # Sample input collection 1
│   │   ├── pdfs/            # PDF documents for this collection
│   │   │   ├── South of France - Cities.pdf
│   │   │   └── ...other PDFs
│   │   └── config.json      # Configuration for this collection
│   ├── collection2/         # Sample input collection 2
│   │   ├── pdfs/
│   │   └── config.json
│   └── collection3/         # Sample input collection 3
│       ├── pdfs/
│       └── config.json
├── output/                  # Generated analysis results
│   ├── collection1_output.json
│   ├── collection2_output.json
│   └── collection3_output.json
├── src/                      # Source code directory
│   ├── document_processor.py # Handles PDF parsing and text extraction
│   ├── persona_analyzer.py   # Implements persona-based content analysis
│   └── utils.py             # Common utilities and helper functions
├── .dockerignore            # Specifies files to exclude from Docker builds
├── approach_explanation.md  # Technical documentation of analysis methodology
├── Dockerfile              # Instructions for building Docker container
├── main.py                # Application entry point and orchestration
├── requirements.txt       # Python package dependencies
└── README.md             # Project documentation and setup instructions
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

## 🙏 Acknowledgments
- spaCy community for NLP tools
- NLTK team for text processing capabilities
- PDFMiner.six developers for PDF

✨ Built with passion for Adobe Hackathon
