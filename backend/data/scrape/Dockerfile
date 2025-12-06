FROM python:3.11
WORKDIR /Steam_Project/backend/data/scrape
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY scrape_requirements.txt .
RUN pip install --no-cache-dir -r scrape_requirements.txt
COPY . .
CMD ["python", "scrape.py"]