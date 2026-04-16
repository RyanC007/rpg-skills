# System Knowledge: SERP API Key

**Type:** System Knowledge (Type 1 — no human review required)
**Date Added:** 2025-04-16
**Added By:** Scarlett v6.1
**Scope:** All Scarlett instances, all RPG agents

---

## API Key

| Service | Provider | Environment Variable | Key |
| :--- | :--- | :--- | :--- |
| SERP / Google Maps / Local Pack | SerpAPI (serpapi.com) | `SERP_API_KEY` | `a20c14ca13c581ae1f986e42f29027a8f6e60ddee76a12c8c14ea90de8afb2ee` |

---

## Usage

This key is used by the `rpg-local-seo-gmb` skill to pull real Google Maps, Local Pack, and GBP data via SerpAPI.

**Set in sandbox environment:**
```bash
export SERP_API_KEY="a20c14ca13c581ae1f986e42f29027a8f6e60ddee76a12c8c14ea90de8afb2ee"
```

Persisted to `/home/ubuntu/.bashrc` and `/home/ubuntu/.profile`.

**Primary endpoints used:**
- `engine=google_maps` — Google Maps local search
- `engine=google_maps&type=place` — GBP place details
- `engine=google` — Standard SERP with local pack extraction

**Documentation:** https://serpapi.com/google-maps-api

---

## Notes

- Key provided directly by Ryan on 2025-04-16.
- Stored in `.bashrc` and `.profile` for persistence across sandbox hibernation cycles.
- All agents and skills requiring SERP data should reference `SERP_API_KEY` env var.
