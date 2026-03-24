---
name: rpg-newsletter
description: Drafts the weekly RPG subscriber newsletter. Use when generating the weekly Ready Plan Grow newsletter for the RPG subscriber list. Runs every Wednesday. Pulls from the Google Drive context pool to summarize the week's work, applies RPG brand voice, and saves a draft for Ryan and Marcela to review before sending. Never auto-sends.
---

# RPG Newsletter Skill

OUTPUT_TIER: 1 (Public Outbound - strictest guardrails apply)

## Guardrails (Tier 1 - Mandatory)
- Never mention clients by name. Use "a client" or "a business we work with"
- Never include GitHub repo URLs, Google Drive links, Manus task links, or internal file paths
- Never reference internal repo names or agent infrastructure details
- Never include subscriber emails or contact data
- Keep "how we built it" descriptions high-level only

## Purpose
Draft the weekly RPG newsletter summarizing what the team built, shipped, and learned. Written from Scarlett's perspective. Audience is small business owners and RPG subscribers.

## Cadence
- Every Wednesday
- Draft saved to Google Drive `Weekly Newsletters/` folder
- Ryan and Marcela review and approve before sending
- Never auto-send

## Workflow

### Step 1: Pull Week's Context
Read the last 7 days of context pool entries from Google Drive:
```bash
rclone ls "manus_google_drive:Scarlett-System-Files/context_pool" --config /home/ubuntu/.gdrive-rclone.ini
```
Extract: what was built or shipped, anonymized client wins, new capabilities, time saved (use numbers where available).

### Step 2: Identify Content Series Topic
Check `Weekly Newsletters/` for the last edition to identify which series topic is next. Current active series: "Before AI Agents, You Need an AI-Ready Brain."

### Step 3: Draft the Newsletter
Structure:
1. Subject line - direct, benefit-focused, no clickbait
2. Opening hook - one punchy paragraph, RPG voice
3. What we built this week - 2-3 paragraphs, anonymized, time saved with numbers
4. Educational section - current series topic, practical and actionable
5. Why it matters for you - connect to reader's small business reality
6. The bottom line - short, confident close
7. Sign-off: "Until next week, Scarlett, Master Orchestrator, Ready Plan Grow! AI Agent Ecosystem"
8. About RPG boilerplate footer (see `templates/newsletter_footer.md`)

### Step 4: Include GPT Prompt Deliverable
Per RPG newsletter standard, include one short, immediately useful GPT prompt relevant to the week's theme. Label it clearly as a bonus for the reader.

### Step 5: Save Draft
```bash
rclone copy /tmp/newsletter_draft.md "manus_google_drive:Weekly Newsletters/" --config /home/ubuntu/.gdrive-rclone.ini
```
File naming: `rpg_weekly_newsletter_[month]_[day]_[year].md`

### Step 6: Notify for Review
Drop a notification in the context pool that the draft is ready. Ryan or Marcela reviews and sends via Substack or email platform.

## Voice Reminders
- Conversational, direct, no corporate jargon
- Sarcastic but respectful
- Second person ("you") focused
- No em dashes
- No hyperbole or unprovable claims
- 2-3 sentences max per paragraph
- Active voice preferred

## Resources
- `templates/newsletter_footer.md` - Standard About RPG boilerplate footer text

## Mandatory Output Sanitization

**BEFORE delivering any file, report, post, or content to the user or saving to Google Drive, you MUST run the sanitization tool on the output file.** This is non-negotiable and applies to every agent and every output type.

### Standard RPG Sanitization (All Agents)

```bash
python3 /home/ubuntu/knowledge_bases/rpg-branded-agents/skills/_guardrails/sanitize_output.py --input /path/to/output_file.md
```

The tool overwrites the file in place. Use `--output /path/to/clean_file.md` to save a separate sanitized copy instead.

### Logoclothz Agents (Additional Rules)

```bash
python3 /home/ubuntu/knowledge_bases/rpg-branded-agents/skills/_guardrails/sanitize_output.py --input /path/to/output_file.md --logoclothz
```

### Sanitization Checklist

- [ ] Sanitization tool has been run on the output file
- [ ] No errors or flagged content remain in the output
- [ ] Sanitized file (not the pre-sanitization draft) is what gets delivered or saved to Drive
