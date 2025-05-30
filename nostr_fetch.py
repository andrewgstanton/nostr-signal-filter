import asyncio
import websockets
import json
import os
from datetime import datetime
from utils import format_event_output, decode_npub

# Get pubkey from environment and decode if needed
input_key = os.getenv("PUBKEY", "").strip()
if input_key.startswith("npub"):
    pubkey_hex = decode_npub(input_key)
else:
    pubkey_hex = input_key

RELAY_URL = "wss://relay.damus.io"

def is_top_level_note(event):
    return (
        event.get("kind") == 1 and
        not any(tag[0] == "e" for tag in event.get("tags", []))
    )

async def fetch_events():
    async with websockets.connect(RELAY_URL) as ws:
        subscription_id = "fetcher"
        request = [
            "REQ",
            subscription_id,
            {
                "kinds": [1, 30023],
                "authors": [pubkey_hex],
                "limit": 50
            }
        ]
        await ws.send(json.dumps(request))

        notes = []
        articles = []

        while True:
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=5)
                data = json.loads(response)

                if data[0] == "EVENT" and data[1] == subscription_id:
                    event = data[2]
                    timestamp = datetime.utcfromtimestamp(event["created_at"]).strftime('%Y-%m-%d %H:%M:%S')

                    if event["kind"] == 1 and is_top_level_note(event):
                        notes.append(event)

                    elif event["kind"] == 30023:
                        articles.append(event)

                elif data[0] == "EOSE":
                    break

            except asyncio.TimeoutError:
                break

        # Output results
        print("\n📝 Top-Level Nostr Notes:\n")
        for note in notes:
            print(format_event_output(note))

        print("\n📚 Long-Form Nostr Articles:\n")
        for article in articles:
            print(format_event_output(article))

if __name__ == "__main__":
    asyncio.run(fetch_events())
