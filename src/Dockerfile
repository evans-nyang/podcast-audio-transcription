FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    ffmpeg \ 
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip wheel setuptools

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir llama-cpp-python==0.2.77 --verbose
RUN pip install git+https://github.com/stlukey/whispercpp.py

COPY app .
COPY /content/models /app/content/models

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
