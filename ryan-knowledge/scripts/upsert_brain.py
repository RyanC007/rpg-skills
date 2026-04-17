#!/usr/bin/env python3
"""
Add or Update Knowledge in Ryan's Portable Brain
Usage: python3 upsert_brain.py --category "AI Usage" --title "Test" --content "Test content" --source "Test"
"""

import os
import sys
import argparse
import uuid
import datetime
from openai import OpenAI
from supabase import create_client

SUPABASE_URL = "https://ugcqrptwxkwqlnzgjqir.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVnY3FycHR3eGt3cWxuemdqcWlyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjQ4MzQ3NywiZXhwIjoyMDg4MDU5NDc3fQ.SfkcBZs02KPqBaYMil3jrR0hKB-QSlm9sIGH66UA1fU"

VALID_CATEGORIES = [
    "AI Usage", "Writing Style", "Domain Knowledge", 
    "Business Context", "Identity", "System Knowledge", "Golden Moments"
]

def main():
    parser = argparse.ArgumentParser(description="Add or update knowledge in Ryan's Portable Brain")
    parser.add_argument("--category", required=True, help=f"Must be one of: {', '.join(VALID_CATEGORIES)}")
    parser.add_argument("--title", required=True, help="Concise title for the knowledge chunk")
    parser.add_argument("--content", required=True, help="The actual knowledge content")
    parser.add_argument("--source", required=True, help="Where this knowledge came from")
    
    parser.add_argument("--id", help="UUID of existing chunk to update (optional)")
    parser.add_argument("--subcategory", default="", help="More specific grouping")
    parser.add_argument("--keywords", default="", help="Comma-separated keywords")
    
    args = parser.parse_args()
    
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is required.")
        sys.exit(1)
        
    if args.category not in VALID_CATEGORIES:
        print(f"Warning: '{args.category}' is not a standard category. Using anyway, but consider standardizing.")
        
    try:
        openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        chunk_id = args.id if args.id else str(uuid.uuid4())
        action = "Updating" if args.id else "Adding new"
        
        print(f"{action} knowledge chunk: {chunk_id}")
        print(f"Title: {args.title}")
        print(f"Category: {args.category}")
        
        # Generate embedding
        print("Generating embedding...")
        emb = openai_client.embeddings.create(
            model="text-embedding-3-small", 
            input=[args.content[:8000]]
        ).data[0].embedding
        
        # Prepare row
        keywords_list = [k.strip() for k in args.keywords.split(",")] if args.keywords else []
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        row = {
            "id": chunk_id,
            "category": args.category,
            "subcategory": args.subcategory,
            "title": args.title[:500],
            "content": args.content[:10000],
            "embedding": emb,
            "source": args.source[:500],
            "confidence": "HIGH",
            "entity": "Ryan",
            "last_updated": today,
            "obsidian_file": "",
            "keywords": keywords_list
        }
        
        # Upsert to Supabase
        print("Saving to Supabase...")
        result = supabase.table("ryan_knowledge_base").upsert(row).execute()
        
        print("\n✅ Success! Knowledge saved to Portable Brain.")
        print(f"ID: {chunk_id}")
        
    except Exception as e:
        print(f"\n❌ Error saving to brain: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
