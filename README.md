# nostr-signal-filter

**A minimal tool for fetching, filtering, and formatting your original Nostr content — ready for archiving, republishing, or cross-posting.**

---

## 🚀 Overview

This project contains four Docker-friendly Python scripts for working with your Nostr posts:

- `nostr_fetch.py`: fetches a **summary of all top-level notes and articles**
- `nostr_fetch_latest.py`: fetches your **latest post or long-form article**, formats it cleanly, and shortens any links for easy reposting (LinkedIn, Facebook, etc.)
- `nostr_fetch_article.py`: fetches your **post or long-form article**, by NoteID (either an nevent1 (for note) or naddr1 (for article), formats it cleanly, and shortens any links for easy reposting (LinkedIn, Facebook, etc.)
- `shorten_links_in_text.py` shorten links in a post
- `format_profile.py` takes your raw text profile.txt and outputs clean marked-down sutiable for github bio or nostr

---

## 🧰 Features

- ✅ Filters for top-level `kind:1` posts (no replies or reposts)
- ✅ Supports `kind:30023` long-form articles
- ✅ Accepts `npub` or hex pubkeys
- ✅ Outputs in plain text, Markdown, or post-ready format
- ✅ Replaces all links in content with TinyURLs
- ✅ Dockerized for quick, portable usage

---

## 📦 Installation

### Prerequisites

- Docker installed on your machine
- Your Nostr public key (`npub...` or hex)

### Clone and Build

```bash
git clone https://github.com/andrewgstanton/nostr-signal-filter.git
cd nostr-signal-filter
docker build -t nostr-fetcher .
```
---

## ▶️ Usage

1. Fetch All Top-Level Posts (nostr_fetch.py_

```bash
docker run --rm -e PUBKEY=npub1yourkeyhere nostr-fetcher nostr_fetch.py
```

2. Fetch and Format the Latest Post or Article (nostr_fetch_latest.py)

```bash
docker run --rm -e PUBKEY=npub1yourkeyhere nostr-fetcher > latest.md
```
Outputs a LinkedIn-safe file (latest.md) with:

Timestamp

Label ("Note" or "Article")

Full content with TinyURL-shortened links

Final link back to the post

3. Fetch and Format a specific Post or Article (nostr_fetch_article.py)

```bash
docker run --rm -e PUBKEY=npub1yourkeyhere nostr-fetcher nostr_fetch_article.py --id EVENTIDorADDRESSID > latest.md
```
Outputs a LinkedIn-safe file (latest.md) with:

Timestamp

Label ("Note" or "Article")

Full content with TinyURL-shortened links

Final link back to the post

4. shorten links in a post (short_links_in_text.py)
   
**From a file:**
```bash
python shorten_links_in_text.py --input original_post.md --output shortened_post.md
```

**Or from stdin:**
```bash
cat original_post.md | python shorten_links_in_text.py
```

This helps ensure links are preserved exactly as you intend when pasting into clients like Primal.net, which may otherwise alter long URLs.

**Inside Docker :**
```bash
docker run --rm  nostr-fetcher shorten_links_in_text.py --input=post.md
```

5. format your profile (format_profile.py)
You can format your professional or personal profile with styled markdown and clean TinyURLs.

**From a file:**
```bash
python format_profile.py --input profile.txt --output profile.md
```

- Converts raw bio text into styled markdown
- Replaces all URLs with TinyURLs
- Ideal for GitHub profile README or Nostr bio

**Inside Docker:**
```bash
docker run --rm nostr-fetcher format_profile.py --input=profile.txt
```   
---

## ⚙️ Environment Variables

| Variable | Description                            | Required |
|----------|----------------------------------------|----------|
| `PUBKEY` | Your Nostr public key (npub or hex)    | ✅       |


---

## ⚙️ License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Contributions are welcome!

To contribute:
- Fork the repository
- Create a new branch (`git checkout -b feature-name`)
- Commit your changes
- Open a pull request

You can also open issues for feedback or suggestions.


---

## 🔁 Fallback Behavior

If an event ID (note or article) is not found on any queried relays, the tool will now output a direct Primal link using the original `nevent1...` or `naddr1...` string.

This ensures that even if an event is not publicly retrievable via relays, users can still view it through a client like Primal:

```
❌ Event not found on any relay.
🔗 View on Primal:
https://primal.net/e/nevent1...
```




