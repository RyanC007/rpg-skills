#!/usr/bin/env python3
"""
Search Ryan's Portable Brain
Usage: python3 search_brain.py "your query here"
"""

import os
import sys
import argparse
from openai import OpenAI
from supabase import create_client

SUPABASE_URL = "https://ugcqrptwxkwqlnzgjqir.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVnY3FycHR3eGt3cWxuemdqcWlyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjQ4MzQ3NywiZXhwIjoyMDg4MDU5NDc3fQ.SfkcBZs02KPqBaYMil3jrR0hKB-QSlm9sIGH66UA1fU"

def main():
    parser = argparse.ArgumentParser(description="Search Ryan's Portable Brain")
    parser.add_argument("query", help="The natural language query to search for")
    parser.add_argument("--limit", type=int, default=5, help="Number of results to return")
    parser.add_argument("--threshold", type=float, default=0.3, help="Similarity threshold (0.0 to 1.0)")
    
    args = parser.parse_args()
    
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is required.")
        sys.exit(1)
        
    try:
        openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        print(f"Searching Portable Brain for: '{args.query}'...")
        
        # Generate embedding for query
        emb = openai_client.embeddings.create(
            model="text-embedding-3-small", 
            input=[args.query]
        ).data[0].embedding
        
        # Search Supabase
        results = supabase.rpc(
            "search_knowledge", 
            {
                "query_embedding": emb, 
                "match_count": args.limit,
                "match_threshold": args.threshold
            }
        ).execute()
        
        if not results.data:
            print("\nNo relevant knowledge found above the similarity threshold.")
            sys.exit(0)
            
        print(f"\nFound {len(results.data)} relevant chunks:\n")
        print("=" * 80)
        
        for i, r in enumerate(results.data, 1):
            print(f"RESULT {i} | Score: {r['similarity']:.2f}")
            print(f"ID: {r['id']}")
            print(f"Category: {r['category']} > {r.get('subcategory', '')}")
            print(f"Title: {r['title']}")
            print(f"Source: {r.get('source', 'Unknown')}")
            print("-" * 40)
            print(r['content'])
            print("=" * 80)
            
    except Exception as e:
        print(f"Error searching brain: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
