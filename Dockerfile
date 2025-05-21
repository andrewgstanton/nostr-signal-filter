FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Default command; can be overridden at runtime
CMD ["python", "nostr_fetch_latest.py"]
