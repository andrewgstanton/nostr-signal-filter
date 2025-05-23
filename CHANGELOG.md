# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [RELEASE-v1.0.0] - 2025-05-21

### Added
- `nostr_fetch.py`: fetches all top-level notes and articles (`kind:1`, `kind:30023`)
- `nostr_fetch_latest.py`: fetches and formats the latest note/article for reposting
- TinyURL integration to shorten all in-body links and output URL
- Markdown-safe output with post type, timestamp, and cleaned links
- Environment variable support: `PUBKEY` (npub or hex)
- Docker support with `Dockerfile`
- `requirements.txt` with dependencies (`websockets`, `requests`, `bech32`)
- GitHub-ready `README.md` with usage, install, environment, license, and contribution instructions

### Changed
- Consolidated all README edits into a single final formatting commit

---

## [RELEASE-v1.0.1] - 2025-05-21

### Fixed
- Switched to using canonical Primal URLs (`/e/{event_id}`) for all posts and articles to ensure correct rendering and redirect behavior
- Removed all slug-generation logic that could break on special characters, casing, or title mismatch
- Article and note types still clearly labeled in output

### Maintained
- TinyURL shortening of rendered links
- Markdown-safe formatting
- Docker compatibility

---

## [RELEASE-v1.0.2] - 2025-05-22

### Added
- `nostr_fetch_article.py`: fetches and formats the note/article by NoteID (noteID is formatted as neventi for notes, naddr1 for articles)
- refactored common functions used on all nostr..py scripts and moved to utils.py
- used multiple relays to find an article or note in nostr_fetch_article.py

### Maintained
- TinyURL shortening of rendered links
- Markdown-safe formatting
- Docker compatibility

---

## [RELEASE-v1.0.3] - 2025-05-22

### Added
- `shorten_links_in_text.py`: shorten links in a post
- `format_profile.py`: utility to generate profile.md from a plaintext profile


### Maintained
- TinyURL shortening of rendered links
- Markdown-safe formatting
- Docker compatibility

