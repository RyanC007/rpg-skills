---
name: rpg-brand-content
description: Creates RPG brand content including social media posts, LinkedIn content, blog posts, and marketing copy for the Ready Plan Grow brand. Use when creating any content for the RPG brand itself (not for clients). Applies RPG brand voice and anti-BS tone. Tier 1 guardrails apply to all public outputs.
---

# Rpg Brand Content

OUTPUT_TIER: 1 (Public Outbound - strictest guardrails apply)

## Guardrails (Tier 1 - Mandatory)
- Never mention clients by name. Use "a client" or "a business we work with"
- No internal repo URLs, Google Drive links, or file paths
- No agent infrastructure details beyond high-level descriptions
- No unprovable claims or hyperbole
- No em dashes

## Purpose
Create content for the RPG brand across all channels. This skill handles RPG's own marketing, not client work.

## Brand Voice Quick Reference
- Direct and conversational. Use "you" and "we."
- Anti-BS. Call out industry nonsense.
- Sarcastic but respectful.
- Empathetic to small business pain.
- Educational without being preachy.


## Content Types

### LinkedIn Posts (RPG Brand)
- Hook in first line (question, bold statement, or pattern interrupt)
- 3-5 short paragraphs max
- No hashtag spam (3-5 max, relevant only)
- CTA at end
- Tier 1 guardrails: no client names, no internal links

### Blog Posts (RPG Website)
- SEO-optimized, 800-1500 words
- RPG voice throughout
- Internal links to relevant RPG pages where appropriate
- CTA aligned with RPG services

### Marketing Copy
- Benefit-focused headlines
- No corporate jargon
- Specific numbers and outcomes where available
- Always ends with a clear next step

## RPG Core Narrative
Ryan Cunningham and Marcela built RPG to deliver what corporate never does: real results without vendor lock-in. AI-powered, built for small businesses.

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
