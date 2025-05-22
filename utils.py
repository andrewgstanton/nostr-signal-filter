
import urllib.parse
import requests
import re
from datetime import datetime
import bech32

# bech32 decoding for naddr
def decode_naddr(naddr_str):
    hrp, data = bech32.bech32_decode(naddr_str)
    if hrp != "naddr":
        raise ValueError("Only 'naddr' format is supported.")
    
    decoded = bech32.convertbits(data, 5, 8, False)
    # print("Decoded TLV data bytes:", decoded)

    i = 0
    kind = None
    pubkey = None
    identifier = None

    while i < len(decoded):
        tag = decoded[i]
        length = decoded[i + 1]
        value = decoded[i + 2:i + 2 + length]

        # print(f"Tag: {tag}, Length: {length}, Raw Value: {value}")

        if tag == 0:  # Identifier (d tag)
            identifier = bytes(value).decode("utf-8")
            # print("Identifier:", identifier)
        elif tag in (1, 2):  # allow both tag 1 (spec) and tag 2 (actual)
            pubkey = bytes(value).hex()
            # print("Pubkey:", pubkey)
        elif tag == 3:  # Kind
            kind = int.from_bytes(bytes(value), "big")
            # print("Kind:", kind)

        i += 2 + length

    if not all([kind, pubkey, identifier]):
        raise ValueError("Failed to decode naddr data.")

    return kind, pubkey, identifier

# bech32 decoding for nevent
def decode_bech32_to_hex(bech32_str):
    hrp, data = bech32.bech32_decode(bech32_str)
    if hrp != "nevent":
        raise ValueError("Only 'nevent' format is supported in this context.")
    decoded = bech32.convertbits(data, 5, 8, False)
    return ''.join(f'{b:02x}' for b in decoded)

# Bech32 decoding for npub
def decode_npub(npub):
    hrp, data = bech32.bech32_decode(npub)
    if hrp != "npub":
        raise ValueError("Invalid prefix: expected 'npub'")
    decoded = bech32.convertbits(data, 5, 8, False)
    return ''.join(f'{b:02x}' for b in decoded)

def shorten_url(url):
    try:
        res = requests.get(f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(url)}")
        if res.status_code == 200:
            return res.text
    except:
        pass
    return url

def shorten_links_in_text(text):
    url_pattern = r'(https?://[^\s)\]]+)'
    urls = re.findall(url_pattern, text)
    url_map = {url: shorten_url(url) for url in urls}
    for original, short in url_map.items():
        text = text.replace(original, short)
    return text


def generate_link(event_id):
    return f"https://primal.net/e/{event_id}"    

def format_event_output(event):
    label = "Note" if event["kind"] == 1 else "Article"
    timestamp = datetime.utcfromtimestamp(event["created_at"]).strftime('%Y-%m-%d %H:%M:%S')
    content = event["content"].strip()
    content_clean = shorten_links_in_text(content)
    raw_url = generate_link(event['id'])
    final_short = shorten_url(raw_url)

    return (
        f"[Time] {timestamp}\n"
        f"[Type] {label} (originally posted on Nostr/primal.net)\n\n"
        f"---\n\n"
        f"{content_clean}\n\n"
        f"---\n\n"
        f"[Link] {label}: {final_short}\n"
    )



