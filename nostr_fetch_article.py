
import asyncio
import websockets
import json
import argparse
from utils import (
    format_event_output,
    decode_bech32_to_hex,
    decode_naddr,
    encode_bech32_event
)

RELAYS = ['wss://bitcoinmaximalists.online/', 'wss://nos.lol/', 'wss://nostr.bit4use.com/', 'wss://nostr.reelnetwork.eu/', 'wss://purplepag.es/', 'wss://relay.damus.io/', 'wss://relay.nostr.band/', 'wss://relay.primal.net/', 'wss://relay.snort.social/', 'wss://relayable.org/']

async def fetch_by_event_id(event_id, original_nevent=None):
    for relay in RELAYS:
        try:
            async with websockets.connect(relay) as ws:
                await ws.send(json.dumps(["REQ", "fetch_by_id", {"ids": [event_id]}]))
                while True:
                    try:
                        response = await asyncio.wait_for(ws.recv(), timeout=5)
                        data = json.loads(response)
                        if data[0] == "EVENT":
                            print(f"[✅ Found on {relay}]")
                            print(format_event_output(data[2]))
                            return True
                        elif data[0] == "EOSE":
                            break
                    except asyncio.TimeoutError:
                        break
        except Exception as e:
            print(f"[⚠️ Error connecting to {relay}]: {e}")
    # fallback
    if original_nevent:
        print("❌ Event not found on any relay.")
        print("🔗 View on Primal:")
        print(f"https://primal.net/e/{original_nevent}")
    else:
        print("❌ Event not found on any relay and no fallback link available.")
    return False

async def fetch_by_naddr(kind, pubkey, d_tag):
    for relay in RELAYS:
        try:
            async with websockets.connect(relay) as ws:
                query = {
                    "kinds": [kind],
                    "authors": [pubkey],
                    "#d": [d_tag]
                }
                await ws.send(json.dumps(["REQ", "resolve_naddr", query]))
                while True:
                    try:
                        response = await asyncio.wait_for(ws.recv(), timeout=5)
                        data = json.loads(response)
                        if data[0] == "EVENT":
                            print(f"[✅ Found on {relay}]")
                            print(format_event_output(data[2]))
                            return True
                        elif data[0] == "EOSE":
                            break
                    except asyncio.TimeoutError:
                        break
        except Exception as e:
            print(f"[⚠️ Error connecting to {relay}]: {e}")
    print("❌ Article not found on any relay.")
    print("🔗 View on Primal:")
    print(f"https://primal.net/e/naddr1qvzqq...")
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch a Nostr note or article from multiple relays by ID.")
    parser.add_argument("--id", required=True, help="The Nostr event ID: hex, nevent1..., or naddr1...")
    args = parser.parse_args()

    id_arg = args.id
    if id_arg.startswith("nevent1"):
        try:
            event_id = decode_bech32_to_hex(id_arg)
            asyncio.run(fetch_by_event_id(event_id, original_nevent=id_arg))
        except Exception as e:
            print(f"Failed to decode nevent ID: {e}")
    elif id_arg.startswith("naddr1"):
        try:
            kind, pubkey, d_tag = decode_naddr(id_arg)
            asyncio.run(fetch_by_naddr(kind, pubkey, d_tag))
        except Exception as e:
            print(f"Failed to decode naddr: {e}")
    else:
        asyncio.run(fetch_by_event_id(id_arg))
