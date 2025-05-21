import asyncio
import websockets
import json
import os
from datetime import datetime
import bech32
import urllib.parse
import requests
import re

# --- Decode npub to hex ---
def decode_npub(npub):
    hrp, data = bech32.bech32_decode(npub)
    if hrp != "npub":
        raise ValueError("Invalid prefix")
    decoded = bech32.convertbits(data, 5, 8, False)
    return ''.join(f'{b:02x}' for b in decoded)

# --- Clean article title into slug format ---
def slugify(title):
    title = re.sub(r'[^\w\s-]', '', title)
    title = title.replace("’", "'").replace("‘", "'")
    title = title.replace("“", '"').replace("”", '"')
    return re.sub(r'\s+', '-', title.strip()).lower()

# --- Shorten using TinyURL ---
def shorten_url(url):
    try:
        res = requests.get(f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(url)}")
        return res.text if res.status_code == 200 else url
    except:
        return url

# --- Replace all in-body URLs with TinyURLs ---
def shorten_links_in_text(text):
    url_pattern = r'(https?://[^\s\)\]]+)'
    urls = re.findall(url_pattern, text)
    url_map = {url: shorten_url(url) for url in urls}
    for original, short in url_map.items():
        text = text.replace(original, short)
    return text

# --- Setup pubkey from env ---
input_key = os.getenv("PUBKEY", "").strip()
pubkey_hex = decode_npub(input_key) if input_key.startswith("npub") else input_key

RELAY_URL = "wss://relay.damus.io"

def is_top_level_note(event):
    return event.get("kind") == 1 and not any(tag[0] == "e" for tag in event.get("tags", []))

def generate_note_link(event_id):
    return f"https://primal.net/e/{event_id}"

def generate_article_link(pubkey_hex, content):
    lines = content.strip().splitlines()
    if not lines:
        return None
    title = slugify(lines[0])
    return f"https://primal.net/{pubkey_hex}/{title}"

# --- Main fetch logic ---
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
        label = "Note" if latest["kind"] == 1 else "Article"
        original_post_location = " (originally posted on Nostr/primal.net)"
        timestamp = datetime.utcfromtimestamp(latest["created_at"]).strftime('%Y-%m-%d %H:%M:%S')
        content = latest["content"].strip()

        # Shorten links in content
        content_clean = shorten_links_in_text(content)

        # Shorten final link
        if latest["kind"] == 30023:
            raw_url = generate_article_link(pubkey_hex, content)
        else:
            raw_url = generate_note_link(latest["id"])
        final_short = shorten_url(raw_url)

        # Output
        print(f"""🕒 {timestamp}  
📄 {label}{original_post_location}

---

{content_clean}

---

🔗 View on Nostr:  
{final_short}
""")

# --- Run it ---
if __name__ == "__main__":
    asyncio.run(fetch_latest_event())
