---
name: ryan-knowledge
description: Ryan's Portable Brain interface. Use this skill whenever Ryan asks to save, update, or retrieve knowledge, frameworks, opinions, or voice DNA. This skill is the single source of truth for all Portable Brain operations — schema, scripts, connection details, and all knowledge updates live here.
---

# Ryan's Portable Brain (ryan-knowledge)

This skill is the **single source of truth** for Ryan's Portable Brain — a Supabase pgvector database containing his frameworks, voice DNA, business context, AI usage guidelines, and personal identity. Every schema change, operational update, and new knowledge addition is recorded here.

## When to Use This Skill

- **Retrieval**: When you need to know how Ryan thinks, what his frameworks are, or how he writes.
- **Storage**: When Ryan says "save this to my brain", "remember this", or when a structured extraction session produces new knowledge.
- **Updating**: When Ryan corrects a previous assumption or updates his stance on a topic.
- **Schema changes**: Any ALTER TABLE or new column additions must be documented in the Schema Changelog below.

## Authorized Agents

| Agent | Location | Access |
| :--- | :--- | :--- |
| **Ryan's AI** | Manus Project `RErVF6WuENnabtqdL4mGvK` | Full read + write |
| **Trinity** | Manus Project (Chief of Staff) | Full read + write |
| **Seven** | Manus stack | Full read + write |
| **Morpheus** | Manus stack | Read + write only when Ryan explicitly authorizes per task |

**All other agents**: Read-only unless Ryan grants explicit write permission.

## Boundary Rules (CRITICAL)

1. **Ryan's IP Only**: Strictly for Ryan's personal knowledge, frameworks, and voice. Do NOT store client data, RPG operations, or Marcela's knowledge here.
2. **High Confidence Only**: Only store information you are highly confident represents Ryan's actual stance.
3. **No Duplication**: Search first. If a chunk exists, update it — do not create a duplicate.
4. **Ryan-Triggered Writes Only**: Any agent may search freely. New knowledge is only written when Ryan explicitly triggers it.
5. **Personal vs. Business**: Every chunk MUST include a `context` field — either `"personal"` or `"business"`. Never mix both in one chunk.

## Personal vs. Business Context Rule

Every knowledge chunk must be tagged with one of two context values:

- `"context": "personal"` — Ryan as a person: values, family, personality, beliefs, habits, health, life experiences, personal goals.
- `"context": "business"` — Ryan as a business operator: companies, clients, services, frameworks, marketing, AI stack, strategy, tools.

**If a topic spans both, create two separate chunks** — one personal, one business.

## How to Use the Brain

### 1. Search (Retrieval)

```bash
OPENAI_API_KEY=$OPENAI_API_KEY python3 /home/ubuntu/skills/ryan-knowledge/scripts/search_brain.py "What is Ryan's SEO framework?"
```

Optional flags: `--limit 10` (default 5), `--threshold 0.3` (default 0.3)

### 2. Add / Update Knowledge (Storage)

```bash
OPENAI_API_KEY=$OPENAI_API_KEY python3 /home/ubuntu/skills/ryan-knowledge/scripts/upsert_brain.py \
  --category "Business Context" \
  --context "business" \
  --title "Ryan's Pricing Philosophy" \
  --content "Ryan believes..." \
  --source "Conversation 2026-04-17"
```

**Required:** `--category`, `--context`, `--title`, `--content`, `--source`

**Optional:** `--id` (UUID of existing chunk to update), `--subcategory`, `--keywords`

**Valid categories:** `AI Usage`, `Writing Style`, `Domain Knowledge`, `Business Context`, `Identity`, `System Knowledge`, `Golden Moments`

**Valid context values:** `personal`, `business`

## Full Table Schema

Table name: `ryan_knowledge_base`
Database: Supabase project `ugcqrptwxkwqlnzgjqir` (East US, Ohio — Nano plan)

| Column | Type | Default | Notes |
| :--- | :--- | :--- | :--- |
| `id` | uuid | gen_random_uuid() | Primary key |
| `category` | text | — | Required. One of the 7 valid categories |
| `subcategory` | text | '' | Optional grouping |
| `context` | text | 'business' | **Required.** `personal` or `business` |
| `title` | text | — | Concise, max 10 words |
| `content` | text | — | 3 sentences to 400 words, third person |
| `embedding` | vector(1536) | — | text-embedding-3-small |
| `source` | text | — | Where this knowledge came from |
| `confidence` | text | 'HIGH' | HIGH / MEDIUM / LOW |
| `entity` | text | 'Ryan' | Always 'Ryan' for this database |
| `last_updated` | text | — | YYYY-MM-DD format |
| `obsidian_file` | text | '' | Linked Obsidian file if applicable |
| `keywords` | jsonb | [] | Array of keyword strings |

## Schema Changelog

| Date | Change | Reason |
| :--- | :--- | :--- |
| 2026-04-17 | Initial table created with pgvector, search function, RLS | Portable Brain v1 build |
| 2026-04-17 | `context` column added (`text`, default `'business'`) | Personal vs. business knowledge distinction |

## Connection Details

- **Project URL**: `https://ugcqrptwxkwqlnzgjqir.supabase.co`
- **Service Role Key**: Stored in `references/connection.md` (do not expose in public outputs)
- **Embedding Model**: `text-embedding-3-small` (1536 dimensions)
- **Search Function**: `search_knowledge(query_embedding, match_count, match_threshold)`

See `references/connection.md` for the full service role key and Python connection snippet.
