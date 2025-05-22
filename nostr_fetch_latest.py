import asyncio
import websockets
import json
import os
from datetime import datetime
from utils import format_event_output, decode_npub
import urllib.parse
import requests
import re

def slugify_and_encode(title):
    return urllib.parse.quote(title.strip())

input_key = os.getenv("PUBKEY", "").strip()
pubkey_hex = decode_npub(input_key) if input_key.startswith("npub") else input_key

RELAY_URL = "wss://relay.damus.io"

def is_top_level_note(event):
    return event.get("kind") == 1 and not any(tag[0] == "e" for tag in event.get("tags", []))

async def fetch_latest_event():
    async with websockets.connect(RELAY_URL) as ws:
        await ws.send(json.dumps([
            "REQ", "fetcher_latest", {
                "kinds": [1, 30023],
                "authors": [pubkey_hex],
                "limit": 50
            }
        ]))

        all_posts = []
        while True:
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=5)
                data = json.loads(response)
                if data[0] == "EVENT":
                    event = data[2]
                    if event["kind"] == 1 and is_top_level_note(event):
                        all_posts.append(event)
                    elif event["kind"] == 30023:
                        all_posts.append(event)
                elif data[0] == "EOSE":
                    break
            except asyncio.TimeoutError:
                break

        if not all_posts:
            print("No notes or articles found.")
            return

        latest = max(all_posts, key=lambda e: e["created_at"])
        print(format_event_output(latest))

if __name__ == "__main__":
    asyncio.run(fetch_latest_event())