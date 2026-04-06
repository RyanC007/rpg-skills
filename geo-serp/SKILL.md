---
name: geo-serp
description: >
 Live SERP intelligence layer powered by SerpAPI. Provides real-time data for
 AI Overview citation detection, featured snippet ownership, People Also Ask
 extraction, Knowledge Graph entity verification, competitor SERP mapping,
 keyword rank tracking, and local pack monitoring. Use when the user wants
 live search data to power any GEO audit or content strategy.
version: 1.0.0
author: geo-seo-manus
tags: [geo, serp, serpapi, aio, featured-snippet, paa, knowledge-graph, rank-tracking, local-seo]
requires:
 - SERPAPI_KEY in.env
---

# GEO SERP Intelligence Layer

## Overview

The `geo-serp` skill connects the entire geo-seo-manus stack to live Google search
data via SerpAPI. Every other skill in this toolkit can now be powered by real-time
SERP results rather than manual analysis.

**Built by [Ryan Cunningham](https://www.readyplangrow.com) | Ready, Plan, Grow!**

---

## Setup

1. Get a SerpAPI key at [serpapi.com](https://serpapi.com)
2. Add it to your `.env` file:
 ```
 SERPAPI_KEY=your_key_here
 ```
3. Install the requests library if not already installed:
 ```bash
 pip install requests python-dotenv
 ```

---

## Commands

### 1. AIO Citation Audit
**Check if your domain is being cited in Google AI Overviews**

```bash
python3 scripts/aio_audit.py \
 --domain example.com \
 --keywords "best CRM" "CRM for small business" "top CRM tools" \
 --output GEO-AIO-AUDIT.md
```

With a keywords file:
```bash
python3 scripts/aio_audit.py --domain example.com --keywords-file keywords.txt
```

**Output:** `GEO-AIO-AUDIT.md` - citation rate, per-keyword breakdown, competitor citations, recommendations.

---

### 2. Featured Snippet Audit
**Check who owns featured snippets for your target keywords**

```bash
python3 scripts/snippet_audit.py \
 --domain example.com \
 --keywords "what is CRM" "how to choose CRM software" \
 --output GEO-SNIPPET-AUDIT.md
```

**Output:** `GEO-SNIPPET-AUDIT.md` - owned snippets, competitor-owned opportunities, how-to-win guide.

---

### 3. People Also Ask Extractor
**Extract all PAA questions for a topic to power content strategy**

```bash
python3 scripts/paa_extract.py \
 --keywords "CRM software" "best CRM for small business" \
 --output GEO-PAA-QUESTIONS.md
```

**Output:** `GEO-PAA-QUESTIONS.md` - deduplicated question bank with content brief template.

---

### 4. Knowledge Graph Verifier
**Check if a brand has a Google Knowledge Panel**

```bash
python3 scripts/kg_verify.py \
 --brand "Acme Corp" \
 --output GEO-KG-REPORT.md
```

**Output:** `GEO-KG-REPORT.md` - entity status, kgmid, social profiles, entity-building recommendations.

---

### 5. Competitor SERP Mapper
**Map the competitive landscape across target keywords**

```bash
python3 scripts/competitor_map.py \
 --domain example.com \
 --keywords "CRM software" "best CRM" "CRM for startups" \
 --output GEO-COMPETITOR-MAP.md
```

**Output:** `GEO-COMPETITOR-MAP.md` - competitor frequency table, SERP features active, target rankings.

---

### 6. Rank Tracker
**Track live organic rankings across a keyword set**

```bash
# First run - save as baseline
python3 scripts/rank_tracker.py \
 --domain example.com \
 --keywords-file keywords.txt \
 --save-baseline \
 --output GEO-RANK-REPORT.md

# Monthly check - compare against baseline
python3 scripts/rank_tracker.py \
 --domain example.com \
 --keywords-file keywords.txt \
 --compare rank-baseline-example-com-2026-01-01.json \
 --output GEO-RANK-DELTA.md
```

**Output:** `GEO-RANK-REPORT.md` - keyword rankings table with delta comparison when baseline provided.

---

### 7. Local Pack Monitor
**Check local pack presence for local businesses**

```bash
python3 scripts/local_pack_monitor.py \
 --domain example.com \
 --keywords "plumber near me" "emergency plumber" \
 --location "Austin, Texas, United States" \
 --output GEO-LOCAL-PACK.md
```

**Output:** `GEO-LOCAL-PACK.md` - pack presence, position, competitor names, local SEO recommendations.

---

### 8. Full SERP Snapshot (Single Query)
**Get a complete SERP picture for one query in one API call**

```python
from scripts.serp_client import SerpClient
client = SerpClient()
snapshot = client.full_snapshot("best CRM for small business", "example.com")
print(snapshot)
```

Returns: AIO presence + citation, snippet ownership, PAA questions, organic rank, SERP features - all from one call.

---

## API Credit Usage

| Script | Credits per Run |
|---|---|
| `aio_audit.py` (10 keywords) | 10 |
| `snippet_audit.py` (10 keywords) | 10 |
| `paa_extract.py` (5 keywords) | 5 |
| `kg_verify.py` | 1 |
| `competitor_map.py` (10 keywords) | 10 |
| `rank_tracker.py` (10 keywords) | 10 |
| `local_pack_monitor.py` (5 keywords) | 5 |
| Full client audit (all scripts, 10 kw each) | ~51 |

At SerpAPI's standard plan (5,000 credits/month), a full audit for one client uses ~51 credits.
You can run approximately **98 full client audits per month** on the standard plan.

---

## Integration with Other Skills

| Skill | How geo-serp enhances it |
|---|---|
| `geo-platform-optimizer` | Feed `aio_audit.py` results directly into the AIO section |
| `geo-citability` | Use `snippet_audit.py` to verify snippet ownership claims |
| `geo-content` | Use `paa_extract.py` to populate question-based heading recommendations |
| `geo-schema` | Use `kg_verify.py` to confirm entity recognition before schema recommendations |
| `geo-prospect` | Use `competitor_map.py` to auto-populate competitor data at prospect creation |
| `geo-compare` | Use `rank_tracker.py` with `--compare` for data-driven monthly delta reports |
| `geo-technical` | Use `local_pack_monitor.py` for local business technical audits |

---

*Built by [Ryan Cunningham](https://www.readyplangrow.com) | Ready, Plan, Grow!*