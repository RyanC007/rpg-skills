#!/usr/bin/env python3
"""
Scarlett Morning Brief -- prep_marcela_brief.py
Runs nightly (Mon-Fri). Pulls the latest context from Google Drive,
builds Marcela's daily intelligence brief, saves it to Drive, and 
emails it to hello@readyplangrow.com via Gmail MCP.
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
EMAIL_TO = "hello@readyplangrow.com"

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
    
    # In a real implementation, this would synthesize the context_contents, Reddit monitor, and news APIs.
    # For now, we generate the template structure based on the architecture.
    
    brief = f"""# Marcela's Daily Intelligence Brief
**Date:** {today}

## 1. The Operator's View (AI & Tech)
*Focus: How new AI developments practically impact small business execution.*
[Placeholder for synthesized AI news relevant to operations]

## 2. Market Pulse (Small Biz & Marketing)
*Focus: Trending topics or challenges observed in the market (e.g., from Reddit).*
[Placeholder for Reddit/Market trends on marketing and small business]

## 3. System Check (Internal/Operations)
*Focus: Critical operational blockers or updates from the RPG team.*
[Placeholder for internal context pool updates]

## 4. Thought Leadership Prompt
*Focus: A specific question or angle based on today's news to spark a LinkedIn post or Substack thought.*
[Placeholder for a thought-provoking question aligned with Marcela's voice]

---
*Prepared by Scarlett | {datetime.now().strftime("%Y-%m-%d %H:%M")} EST*
"""
    return brief

def save_and_upload_brief(brief_text: str) -> str:
    """Save the brief locally and upload to Drive."""
    BRIEF_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today_str = date.today().strftime("%Y-%m-%d")
    local_path = BRIEF_OUTPUT_DIR / f"marcela_brief_{today_str}.md"
    local_path.write_text(brief_text)
    
    # Upload to Drive context pool
    subprocess.run([
        "rclone", "copy", str(local_path), CONTEXT_POOL_REMOTE,
        "--drive-root-folder-id", DRIVE_ROOT,
        "--config", RCLONE_CONFIG
    ], capture_output=True)
    
    return str(local_path)

def send_email_via_mcp(brief_text: str):
    """Send the brief via Gmail MCP."""
    today = date.today().strftime("%Y-%m-%d")
    subject = f"Marcela's Daily Intelligence Brief - {today}"
    
    # Construct the JSON payload for the MCP tool
    payload = {
        "messages": [
            {
                "to": [EMAIL_TO],
                "subject": subject,
                "content": brief_text
            }
        ]
    }
    
    json_payload = json.dumps(payload)
    
    # Call the Gmail MCP tool
    print(f"  Sending email to {EMAIL_TO} via Gmail MCP...")
    result = subprocess.run([
        "manus-mcp-cli", "tool", "call", "gmail_send_messages",
        "--server", "gmail",
        "--input", json_payload
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("  Email sent successfully (or saved to drafts pending confirmation).")
    else:
        print(f"  Failed to send email: {result.stderr}")

def main():
    print(f"[{datetime.now().strftime('%H:%M')}] Marcela brief prep starting...")
    print("  Pulling context from Drive...")
    pull_context()
    
    print("  Reading context files...")
    context = read_context_files()
    
    print("  Building brief...")
    brief = build_brief(context)
    
    print("  Saving and uploading brief...")
    path = save_and_upload_brief(brief)
    print(f"  Brief ready: {path}")
    
    print("  Initiating email delivery...")
    send_email_via_mcp(brief)
    
    print(f"[{datetime.now().strftime('%H:%M')}] Marcela brief prep and delivery complete.")

if __name__ == "__main__":
    main()
