# Portable Brain — Connection Reference

**INTERNAL USE ONLY — Tier 3. Do not include in any public or client-facing output.**

## Supabase Connection

```python
SUPABASE_URL = "https://ugcqrptwxkwqlnzgjqir.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVnY3FycHR3eGt3cWxuemdqcWlyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjQ4MzQ3NywiZXhwIjoyMDg4MDU5NDc3fQ.SfkcBZs02KPqBaYMil3jrR0hKB-QSlm9sIGH66UA1fU"
```

## Python Quick Connect

```python
from supabase import create_client
from openai import OpenAI
import os

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
```

## Semantic Search Snippet

```python
def search_brain(query, limit=5, threshold=0.3):
    emb = openai_client.embeddings.create(
        model="text-embedding-3-small", input=[query]
    ).data[0].embedding
    return supabase.rpc("search_knowledge", {
        "query_embedding": emb,
        "match_count": limit,
        "match_threshold": threshold
    }).execute().data
```

## Upsert Snippet

```python
import uuid, datetime

def upsert_chunk(category, context, title, content, source, subcategory="", keywords=[]):
    emb = openai_client.embeddings.create(
        model="text-embedding-3-small", input=[content[:8000]]
    ).data[0].embedding
    supabase.table("ryan_knowledge_base").upsert({
        "id": str(uuid.uuid4()),
        "category": category,
        "subcategory": subcategory,
        "context": context,  # "personal" or "business"
        "title": title,
        "content": content,
        "embedding": emb,
        "source": source,
        "confidence": "HIGH",
        "entity": "Ryan",
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d"),
        "obsidian_file": "",
        "keywords": keywords
    }).execute()
```
