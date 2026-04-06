---
name: rpg-marcela-brief
description: >-
  Runs the daily Scarlett morning brief for Marcela Shine (Mon-Fri).
  Pulls from Drive context, Reddit, and news, builds the brief, and emails it to hello@readyplangrow.com via Gmail MCP.
  Focuses on Operations, Marketing, Small Business trends, and AI industry news through an operator lens.
---

# RPG Marcela Brief Skill
OUTPUT_TIER: 3 (Internal)

## Delivery Method
- **Email:** Delivered daily to `hello@readyplangrow.com` via the Gmail MCP server.
- **Schedule:** Nightly, Mon-Fri, completes by 8 AM EST.

---

## Workflow
Run by the Manus scheduler every weekday morning. Builds the brief silently, saves it to Drive, and emails it.

```bash
python3 /home/ubuntu/skills/rpg-marcela-brief/scripts/prep_marcela_brief.py
```

The script:
1. Pulls the last 48 hours of context from `Scarlett/Daily_Updates/Context_Pool`
2. Pulls relevant marketing, operations, and small business trends from the Reddit monitor digest.
3. Synthesizes the information using Marcela's voice and perspective (Operator-First, Clarity Before Scale).
4. Builds a dated brief markdown file structured into: Marketing Pulse, Market Pulse, System Check, and Thought Leadership Prompt.
5. Saves it locally to `/home/ubuntu/scarlett_agent_context/briefs/marcela_brief_YYYY-MM-DD.md`
6. Uploads it back to the Drive context pool
7. Calls the `gmail_send_messages` tool via `manus-mcp-cli` to email the brief to `hello@readyplangrow.com`.

---

## Rules
- Brief prep runs Mon-Fri only. No weekends.
- Maintain Marcela's voice: direct, practical, human-first, no fluff.
- NO em dashes.
- Do NOT use TTS or interactive delivery for this brief.

---

## Drive Guardrail
All rclone commands MUST include:
- `--drive-root-folder-id 0AK8dAs_XgfnNUk9PVA`
- `--config /home/ubuntu/.gdrive-rclone.ini`
See `scarlett-drive-guardrail` skill for full rules.
