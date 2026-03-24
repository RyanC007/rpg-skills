---
name: rpg-reddit-monitor
description: Monitors Reddit for relevant conversations, trending topics, and lead opportunities for RPG. Use when running the daily Reddit monitoring workflow. Scans target subreddits for AI tool mentions, small business challenges, and marketing questions. Produces a daily digest with top threads and suggested response opportunities.
---

# Rpg Reddit Monitor

OUTPUT_TIER: 3 (Internal - for Ryan and Marcela only)

## Purpose
Monitor Reddit daily for conversations relevant to RPG's audience and business development. Identify lead opportunities, trending topics for content, and community engagement moments.

## Target Subreddits
See references/subreddit_list.md for the full monitored list. Core subreddits:
- r/smallbusiness
- r/entrepreneur
- r/marketing
- r/artificial
- r/ChatGPT
- r/AItools
- r/freelance
- r/agency

## Workflow

### Step 1: Pull Top Posts
For each target subreddit, pull top posts from the last 24 hours. Focus on posts with high engagement (100+ upvotes or 20+ comments) mentioning AI tools, automation, marketing, or small business challenges.

### Step 2: Analyze for Opportunities
For each relevant post, identify:
- Lead opportunity: Someone asking for help RPG can provide
- Content opportunity: A trending topic RPG should write about
- Engagement opportunity: A thread where RPG's perspective adds value

### Step 3: Produce Daily Digest
Format:
1. Top 3 lead opportunities (with thread link and suggested response angle)
2. Top 3 content opportunities (with topic and suggested angle)
3. Top 3 engagement opportunities (with thread link and suggested comment)
4. Trending keywords from today's posts

### Step 4: Save to Context Pool
Save the digest to Google Drive context pool as reddit_monitor_[date].md.

## Response Guidelines
When suggesting Reddit responses:
- Never pitch RPG directly in comments
- Suggest value-first responses that demonstrate expertise
- Only suggest responses where genuine helpfulness is possible

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
