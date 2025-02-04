FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install prettier
RUN npm install -g prettier@3.4.2

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Create data directory
RUN mkdir -p /data

EXPOSE 8000

CMD ["python", "main.py"]
