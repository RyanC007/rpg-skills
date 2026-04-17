#!/usr/bin/env python3
"""
Ryan's Portable Brain — Bulk Vault Sync
========================================
Run this ONCE to load all existing notes in your Obsidian vault
into Supabase. After that, vault_watcher.py handles new/modified notes.

RUN:
  OPENAI_API_KEY=your_key python3 bulk_sync_vault.py
"""

import os
import sys
from pathlib import Path

# Add scripts dir to path so we can reuse process_file from watcher
sys.path.insert(0, os.path.dirname(__file__))

# Import shared logic from vault_watcher
from vault_watcher import VAULT_PATH, process_file, should_skip, OPENAI_API_KEY

if __name__ == "__main__":
    if not OPENAI_API_KEY:
        print("ERROR: OPENAI_API_KEY not set.")
        exit(1)

    vault = Path(VAULT_PATH)
    if not vault.exists():
        print(f"ERROR: Vault not found at {VAULT_PATH}")
        exit(1)

    md_files = [f for f in vault.rglob("*.md") if not should_skip(str(f))]
    print(f"Found {len(md_files)} notes to sync...")

    for i, filepath in enumerate(md_files, 1):
        print(f"[{i}/{len(md_files)}] {filepath.name}")
        process_file(str(filepath))

    print(f"\nDone. {len(md_files)} notes processed.")
