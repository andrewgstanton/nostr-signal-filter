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


