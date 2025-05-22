FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# allow any python script to be run; be overridden at runtime
ENTRYPOINT ["python"]
CMD ["nostr_fetch_latest.py"]
