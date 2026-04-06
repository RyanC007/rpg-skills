#!/usr/bin/env python3
"""
Scarlett Morning Brief -- prep_brief.py
Runs nightly (Mon-Fri). Pulls the latest context from Google Drive,
builds a prioritized blocker/question queue, and saves the brief to Drive
so it is ready and waiting when Ryan opens Manus in the morning.

Schedule: Mon-Fri, runs at 7:00 AM EST (giving 1 hour buffer before 8 AM)
Trigger: Scheduled via Manus scheduler -- do not run manually unless testing.
"""

import os
import subprocess
import json
from datetime import datetime, date
from pathlib import Path

DRIVE_ROOT = "0AK8dAs_XgfnNUk9PVA"
RCLONE_CONFIG = "/home/ubuntu/.gdrive-rclone.ini"
CONTEXT_POOL_REMOTE = "manus_google_drive:Scarlett/Daily_Updates/Context_Pool"
CONTEXT_LOCAL = Path("/home/ubuntu/scarlett_agent_context/context_pool")
BRIEF_OUTPUT_DIR = Path("/home/ubuntu/scarlett_agent_context/briefs")

def pull_context():
    """Pull last 48 hours of context from Drive."""
    CONTEXT_LOCAL.mkdir(parents=True, exist_ok=True)
    result = subprocess.run([
        "rclone", "copy", CONTEXT_POOL_REMOTE, str(CONTEXT_LOCAL),
        "--drive-root-folder-id", DRIVE_ROOT,
        "--config", RCLONE_CONFIG,
        "--max-age", "48h"
    ], capture_output=True, text=True)
    return result.returncode == 0

def read_context_files() -> list[str]:
    """Read all context files pulled from Drive."""
    files = sorted(CONTEXT_LOCAL.glob("*.md"), reverse=True)
    contents = []
    for f in files[:5]:  # Read the 5 most recent
        try:
            contents.append(f"### {f.name}\n{f.read_text()}")
        except Exception:
            pass
    return contents

def build_brief(context_contents: list[str]) -> str:
    """Build the morning brief markdown from context."""
    today = date.today().strftime("%A, %B %d, %Y")
    context_block = "\n\n".join(context_contents) if context_contents else "No new context in the last 48 hours."

    brief = f"""# Scarlett Morning Brief
**Date:** {today}
**Status:** READY -- Awaiting Ryan

---

## Context Summary
{context_block}

---

## Blocker Queue
<!-- Scarlett: When Ryan triggers the brief, read the context above and build
     the prioritized blocker list dynamically from the open items found.
     Present one item at a time. Do not dump the full list. -->

---

## Session Log
<!-- Scarlett: Log each of Ryan's updates here during the session. -->

---
*Prepared by Scarlett | {datetime.now().strftime("%Y-%m-%d %H:%M")} EST*
*Deliver only when Ryan says: "good morning scarlett", "run morning brief", or "let's do the brief"*
"""
    return brief

def save_and_upload_brief(brief_text: str) -> str:
    """Save the brief locally and upload to Drive."""
    BRIEF_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today_str = date.today().strftime("%Y-%m-%d")
    local_path = BRIEF_OUTPUT_DIR / f"morning_brief_{today_str}.md"
    local_path.write_text(brief_text)

    # Upload to Drive context pool
    subprocess.run([
        "rclone", "copy", str(local_path), CONTEXT_POOL_REMOTE,
        "--drive-root-folder-id", DRIVE_ROOT,
        "--config", RCLONE_CONFIG
    ], capture_output=True)

    return str(local_path)

def main():
    print(f"[{datetime.now().strftime('%H:%M')}] Scarlett brief prep starting...")

    print("  Pulling context from Drive...")
    pull_context()

    print("  Reading context files...")
    context = read_context_files()

    print("  Building brief...")
    brief = build_brief(context)

    print("  Saving and uploading brief...")
    path = save_and_upload_brief(brief)

    print(f"  Brief ready: {path}")
    print(f"[{datetime.now().strftime('%H:%M')}] Morning brief prep complete. Ready for Ryan.")

if __name__ == "__main__":
    main()
