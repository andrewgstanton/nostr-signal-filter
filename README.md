# nostr-signal-filter

**A minimal tool for fetching, filtering, and formatting your original Nostr content — ready for archiving, republishing, or cross-posting.**

---

## 🚀 Overview

This project contains two Docker-friendly Python scripts for working with your Nostr posts:

- `nostr_fetch.py`: fetches a **summary of all top-level notes and articles**
- `nostr_fetch_latest.py`: fetches your **latest post or long-form article**, formats it cleanly, and shortens any links for easy reposting (LinkedIn, Facebook, etc.)

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

1. Fetch All Top-Level Posts

```bash
docker run --rm -e PUBKEY=npub1yourkeyhere nostr-fetcher nostr_fetch.py
```

2. Fetch and Format the Latest Post or Article

```bash
docker run --rm -e PUBKEY=npub1yourkeyhere nostr-fetcher > latest.md
```
Outputs a LinkedIn-safe file (latest.md) with:

Timestamp

Label ("Note" or "Article")

Full content with TinyURL-shortened links

Final link back to the post

3. Fetch and Format a specific Post or Article

```bash
docker run --rm -e PUBKEY=npub1yourkeyhere nostr-fetcher nostr_fetch_article.py --id EVENTIDorADDRESSID > latest.md
```
Outputs a LinkedIn-safe file (latest.md) with:

Timestamp

Label ("Note" or "Article")

Full content with TinyURL-shortened links

Final link back to the post


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





