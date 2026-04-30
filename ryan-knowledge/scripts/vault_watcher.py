#!/usr/bin/env python3
"""
Ryan's Portable Brain — Obsidian Vault Watcher
===============================================
Watches /Users/ryancunnningham/Ryan_Portable_Brain/Obsidian_Vault/
for new or modified .md files and automatically embeds + upserts
them into the ryan_knowledge_base Supabase table.

SETUP (one-time):
  pip3 install watchdog openai supabase

RUN (keep terminal open or use launchd to auto-start):
  OPENAI_API_KEY=your_key python3 vault_watcher.py

Or run in background:
  nohup OPENAI_API_KEY=your_key python3 vault_watcher.py &
"""

import os
import re
import time
import uuid
import hashlib
import datetime
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from openai import OpenAI
from supabase import create_client

# ─── CONFIG ────────────────────────────────────────────────────────────────────
VAULT_PATH = "/Users/ryancunnningham/Ryan_Portable_Brain/Obsidian_Vault"
SUPABASE_URL = "https://ugcqrptwxkwqlnzgjqir.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVnY3FycHR3eGt3cWxuemdqcWlyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjQ4MzQ3NywiZXhwIjoyMDg4MDU5NDc3fQ.SfkcBZs02KPqBaYMil3jrR0hKB-QSlm9sIGH66UA1fU"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Folders to skip (never sync these)
SKIP_FOLDERS = {"_attachments", ".obsidian", ".trash"}

# Map folder names to Supabase categories
FOLDER_CATEGORY_MAP = {
    "00 - Daily Notes":    "Golden Moments",
    "01 - Identity":       "Identity",
    "02 - AI Usage":       "AI Usage",
    "03 - Writing Style":  "Writing Style",
    "04 - Business Context": "Business Context",
    "05 - Domain Knowledge": "Domain Knowledge",
    "06 - Golden Moments": "Golden Moments",
    "07 - Frameworks":     "Domain Knowledge",
    "08 - People":         "Identity",
    "09 - Projects":       "Business Context",
    "10 - Journal":        "Identity",
}

# Map folder names to personal/business context
FOLDER_CONTEXT_MAP = {
    "00 - Daily Notes":    "personal",
    "01 - Identity":       "personal",
    "02 - AI Usage":       "business",
    "03 - Writing Style":  "business",
    "04 - Business Context": "business",
    "05 - Domain Knowledge": "business",
    "06 - Golden Moments": "business",
    "07 - Frameworks":     "business",
    "08 - People":         "personal",
    "09 - Projects":       "business",
    "10 - Journal":        "personal",
}

# ─── INIT ──────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.expanduser("~/vault_watcher.log")),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

openai_client = OpenAI(api_key=OPENAI_API_KEY)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ─── HELPERS ───────────────────────────────────────────────────────────────────
def strip_wiki_links(text):
    """Convert [[Note Name]] to Note Name for clean embedding."""
    return re.sub(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', r'\1', text)

def extract_frontmatter(content):
    """Extract YAML frontmatter if present."""
    meta = {}
    if content.startswith("---"):
        end = content.find("---", 3)
        if end > 0:
            fm = content[3:end].strip()
            for line in fm.split("\n"):
                if ":" in line:
                    k, _, v = line.partition(":")
                    meta[k.strip()] = v.strip()
            content = content[end+3:].strip()
    return meta, content

def chunk_content(content, max_chars=3000):
    """Split long notes into overlapping chunks."""
    if len(content) <= max_chars:
        return [content]
    chunks = []
    paragraphs = content.split("\n\n")
    current = ""
    for para in paragraphs:
        if len(current) + len(para) > max_chars:
            if current:
                chunks.append(current.strip())
            current = para
        else:
            current += "\n\n" + para
    if current.strip():
        chunks.append(current.strip())
    return chunks if chunks else [content[:max_chars]]

def get_folder_name(filepath):
    """Get the immediate parent folder name."""
    return Path(filepath).parent.name

def should_skip(filepath):
    """Check if this file should be skipped."""
    path = Path(filepath)
    for part in path.parts:
        if part in SKIP_FOLDERS or part.startswith("."):
            return True
    if path.suffix.lower() != ".md":
        return True
    return False

def process_file(filepath):
    """Read, chunk, embed, and upsert a note to Supabase."""
    try:
        if should_skip(filepath):
            return

        path = Path(filepath)
        folder = get_folder_name(filepath)
        category = FOLDER_CATEGORY_MAP.get(folder, "Domain Knowledge")
        context = FOLDER_CONTEXT_MAP.get(folder, "business")
        title = path.stem
        obsidian_file = str(path.relative_to(VAULT_PATH))

        with open(filepath, "r", encoding="utf-8") as f:
            raw = f.read()

        if not raw.strip():
            return

        meta, content = extract_frontmatter(raw)
        content = strip_wiki_links(content)

        # Override category/context from frontmatter if present
        if "category" in meta:
            category = meta["category"]
        if "context" in meta:
            context = meta["context"]
        if "title" in meta:
            title = meta["title"]

        chunks = chunk_content(content)
        log.info(f"Processing: {title} ({len(chunks)} chunk(s)) [{context}/{category}]")

        for i, chunk_text in enumerate(chunks):
            if not chunk_text.strip():
                continue

            # Stable ID based on file path + chunk index
            stable_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{obsidian_file}::{i}"))

            emb = openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=[chunk_text[:8000]]
            ).data[0].embedding

            chunk_title = title if len(chunks) == 1 else f"{title} (Part {i+1})"

            row = {
                "id": stable_id,
                "category": category,
                "subcategory": folder,
                "context": context,
                "title": chunk_title,
                "content": chunk_text[:10000],
                "embedding": emb,
                "source": f"Obsidian Vault — {obsidian_file}",
                "confidence": "HIGH",
                "entity": "Ryan",
                "last_updated": datetime.datetime.now().strftime("%Y-%m-%d"),
                "obsidian_file": obsidian_file,
                "keywords": []
            }

            supabase.table("ryan_knowledge_base").upsert(row).execute()
            log.info(f"  ✓ Upserted chunk {i+1}/{len(chunks)}: {chunk_title}")

    except Exception as e:
        log.error(f"Error processing {filepath}: {e}")

# ─── WATCHER ───────────────────────────────────────────────────────────────────
class VaultHandler(FileSystemEventHandler):
    def __init__(self):
        self._debounce = {}

    def _handle(self, filepath):
        now = time.time()
        last = self._debounce.get(filepath, 0)
        if now - last < 3:  # 3-second debounce
            return
        self._debounce[filepath] = now
        process_file(filepath)

    def on_modified(self, event):
        if not event.is_directory:
            self._handle(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self._handle(event.src_path)

# ─── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if not OPENAI_API_KEY:
        print("ERROR: OPENAI_API_KEY environment variable not set.")
        print("Run: export OPENAI_API_KEY=your_key && python3 vault_watcher.py")
        exit(1)

    vault = Path(VAULT_PATH)
    if not vault.exists():
        print(f"ERROR: Vault path not found: {VAULT_PATH}")
        print("Make sure the vault folder exists at: " + VAULT_PATH)
        exit(1)

    log.info(f"Ryan's Portable Brain — Vault Watcher STARTED")
    log.info(f"Watching: {VAULT_PATH}")
    log.info(f"Any .md file you save will be auto-synced to Supabase.")

    observer = Observer()
    observer.schedule(VaultHandler(), VAULT_PATH, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        log.info("Vault Watcher stopped.")
    observer.join()
