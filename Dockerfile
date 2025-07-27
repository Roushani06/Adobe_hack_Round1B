FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y python3-distutils && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm && \
    python -m nltk.downloader punkt stopwords

COPY . .
ENTRYPOINT ["python", "main.py"]    