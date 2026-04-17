---
name: ryan-knowledge
description: Ryan's Portable Brain interface. Use this skill whenever Ryan asks to save, update, or retrieve knowledge, frameworks, opinions, or voice DNA. This skill provides the exact scripts and schema needed to interact with his Supabase vector database.
---

# Ryan's Portable Brain (ryan-knowledge)

This skill provides the interface to Ryan's Portable Brain — a Supabase vector database containing his frameworks, voice DNA, business context, and AI usage guidelines.

## When to Use This Skill

- **Retrieval**: When you need to know how Ryan thinks about a topic, what his frameworks are, or how he writes.
- **Storage**: When Ryan explicitly tells you to "save this to my brain", "remember this", or when you extract a new framework/opinion from a conversation.
- **Updating**: When Ryan corrects a previous assumption or updates his stance on a topic.

## Authorized Agents

The following agents have full read and write access to the Portable Brain:

| Agent | Location | Access |
| :--- | :--- | :--- |
| **Ryan's AI** | Manus Project `RErVF6WuENnabtqdL4mGvK` | Full read + write |
| **Trinity** | Manus Project (Chief of Staff) | Full read + write |
| **Seven** | Manus stack | Full read + write |
| **Morpheus** | Manus stack | Read + write only when Ryan explicitly authorizes per task |

**All other agents**: Read-only unless Ryan grants explicit write permission.

## Boundary Rules (CRITICAL)

1. **Ryan's IP Only**: This database is strictly for Ryan's personal knowledge, frameworks, and voice. Do NOT store client data, general RPG operations, or Marcela's knowledge here.
2. **High Confidence Only**: Only store information you are highly confident is accurate and represents Ryan's actual stance.
3. **No Duplication**: Before adding new knowledge, always search first to see if it already exists. If it does, update the existing chunk rather than creating a duplicate.
4. **Ryan-Triggered Writes Only**: Any agent may search the brain freely. However, new knowledge may only be written when Ryan explicitly requests it — either by direct instruction ("save this", "remember this") or as part of a structured extraction session.

## How to Use the Brain

All interactions with the Portable Brain are handled via two Python scripts located in the `scripts/` directory of this skill.

### 1. Searching the Brain (Retrieval)

Use `scripts/search_brain.py` to query the database using semantic search.

```bash
# Example usage
OPENAI_API_KEY=$OPENAI_API_KEY python3 /home/ubuntu/skills/ryan-knowledge/scripts/search_brain.py "What is Ryan's SEO framework?"
```

The script will return the top 5 most relevant knowledge chunks, including their category, title, and full content.

### 2. Adding/Updating Knowledge (Storage)

Use `scripts/upsert_brain.py` to add new knowledge or update existing chunks.

```bash
# Example usage
OPENAI_API_KEY=$OPENAI_API_KEY python3 /home/ubuntu/skills/ryan-knowledge/scripts/upsert_brain.py \
  --category "Business Context" \
  --title "Thoughts on Lean Startups" \
  --content "Ryan believes lean startups should focus on..." \
  --source "Conversation with Ryan on 2026-04-17"
```

**Required Parameters:**
- `--category`: Must be one of: `AI Usage`, `Writing Style`, `Domain Knowledge`, `Business Context`, `Identity`, `System Knowledge`, `Golden Moments`.
- `--title`: A concise, descriptive title for the chunk.
- `--content`: The actual knowledge to store (max 8000 chars).
- `--source`: Where this knowledge came from (e.g., "Slack conversation", "Direct instruction").

**Optional Parameters:**
- `--id`: If updating an existing chunk, provide its UUID. If omitted, a new UUID is generated.
- `--subcategory`: More specific grouping within the category.
- `--keywords`: Comma-separated list of keywords.

## Data Schema Reference

If you need to interact with the database directly (e.g., via Supabase MCP), the table is `ryan_knowledge_base` with the following schema:

- `id` (uuid, primary key)
- `category` (text)
- `subcategory` (text)
- `title` (text)
- `content` (text)
- `embedding` (vector 1536)
- `source` (text)
- `confidence` (text, default 'HIGH')
- `entity` (text, default 'Ryan')
- `last_updated` (text)
- `obsidian_file` (text)
- `keywords` (jsonb)
