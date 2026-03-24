---
name: rpg-sdr-lead-scraper
description: Scrapes and qualifies leads for RPG business development. Use when running outbound lead generation for RPG. Searches for small business owners matching RPG's ideal client profile, scrapes contact information, qualifies leads against criteria, and outputs a structured lead list ready for outreach.
---

# Rpg Sdr Lead Scraper

OUTPUT_TIER: 3 (Internal - business development use only)

## Purpose
Generate qualified lead lists for RPG outbound business development. Targets small business owners matching RPG's ideal client profile.

## Ideal Client Profile
- Small business owner (1-20 employees)
- Service-based or e-commerce
- 1-5 years in business
- Showing signs of growth or marketing investment
- No current AI/automation agency relationship

## Workflow

### Step 1: Define Campaign Parameters
Before scraping, confirm with Ryan:
- Target industry or niche
- Geographic focus
- Company size range
- Any specific signals to look for

### Step 2: Source Leads
Primary sources:
- LinkedIn (company pages, job postings, founder profiles)
- Google Maps / local business listings
- Industry directories
- Chamber of commerce member lists

### Step 3: Qualify Each Lead
- [ ] Matches ideal client profile
- [ ] Has a website (if required for campaign)
- [ ] Active on at least one social channel
- [ ] Contact information available

### Step 4: Output Lead List
Format as CSV or Excel with columns:
- Company Name, Contact Name, Title, Email, LinkedIn URL, Website, Industry, Employee Count, Qualification Score (1-3), Notes

### Step 5: Save and Report
Save to Google Drive business development folder. Report count, qualification rate, and notable observations to Ryan.

## Compliance Note
All lead generation must comply with applicable laws (CAN-SPAM, GDPR where relevant). Never scrape personal data beyond what is publicly available.

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
