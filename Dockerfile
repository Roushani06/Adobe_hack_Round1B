FROM python:3.9-slim

WORKDIR /app

# Install system dependencies including gcc
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies in a single layer
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm --no-deps && \
    python -m nltk.downloader -d /usr/local/share/nltk_data punkt stopwords

# Copy only necessary files
COPY ./src ./src
COPY main.py .

ENTRYPOINT ["python", "main.py"]