---
name: rpg-client-content
description: Creates scheduled content for RPG clients (blog posts, landing pages, social captions). Use when generating content for any RPG client according to their content schedule. Pulls from the client knowledge base, applies their brand voice, and outputs SEO-optimized content ready for review and publishing. Supports WordPress publishing via rpg-wordpress-publisher skill.
---

# Rpg Client Content

OUTPUT_TIER: 2 (Client-Facing)

## Guardrails (Tier 2 - Mandatory)
- Client name allowed only within that client's own deliverable
- Never reference one client in another client's work
- No internal repo URLs or file paths in client deliverables
- No RPG internal costs or rate cards in client docs

## Purpose
Generate scheduled content for RPG clients. Each client has a knowledge base and content schedule. Read both and produce the correct content for the current period.

## Supported Output Types
- Blog posts (SEO-optimized, WordPress-ready)
- Landing page copy
- Social media captions (LinkedIn, Instagram, Facebook)
- Email newsletter drafts (client-facing)
- Meta titles and descriptions

## Workflow

### Step 1: Identify Client and Schedule
Confirm which client and what content is due. Check the client's content schedule in their Google Drive folder under `Scarlett-System-Files/clients/`.

### Step 2: Load Client Knowledge Base
Pull brand voice, target audience, key messages, and topic restrictions from the client's knowledge base.

### Step 3: Generate Content
For blog posts:
- Target keyword in title, first paragraph, and at least 2 subheadings
- 800-1500 words unless specified otherwise
- Meta title (under 60 characters) and meta description (under 160 characters)
- CTA aligned with client's goals

### Step 4: Quality Check
- [ ] Tier 2 guardrails applied
- [ ] Client voice matches their knowledge base
- [ ] SEO elements present
- [ ] CTA present and aligned with client goals

### Step 5: Deliver or Publish
- Save draft to client's Google Drive folder
- If publishing to WordPress, hand off to rpg-wordpress-publisher skill
- Notify Ryan or Marcela that content is ready for review

## Voice Adaptation
Never apply RPG brand voice to client content. Always read the client's knowledge base voice section before writing.

## Mandatory Output Sanitization

**BEFORE delivering any file, report, post, or content to the user or saving to Google Drive, you MUST run the sanitization tool on the output file.** This is non-negotiable and applies to every agent and every output type.

### Standard RPG Sanitization (All Agents)

```bash
python3 /home/ubuntu/knowledge_bases/rpg-skills/skills/_guardrails/sanitize_output.py --input /path/to/output_file.md
```

The tool overwrites the file in place. Use `--output /path/to/clean_file.md` to save a separate sanitized copy instead.

### Logoclothz Agents (Additional Rules)

```bash
python3 /home/ubuntu/knowledge_bases/rpg-skills/skills/_guardrails/sanitize_output.py --input /path/to/output_file.md --logoclothz
```

### Sanitization Checklist

- [ ] Sanitization tool has been run on the output file
- [ ] No errors or flagged content remain in the output
- [ ] Sanitized file (not the pre-sanitization draft) is what gets delivered or saved to Drive
