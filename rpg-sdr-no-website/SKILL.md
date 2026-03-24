---
name: rpg-sdr-no-website
description: Identifies and qualifies business prospects who do not have a website. Use when running outbound campaigns targeting early-stage businesses or local businesses without an online presence. These are high-potential RPG leads who need foundational digital infrastructure.
---

# Rpg Sdr No Website

OUTPUT_TIER: 3 (Internal - business development use only)

## Purpose
Find and qualify businesses with no website or severely outdated web presence. Prime RPG prospects for foundational digital services.

## Why This Segment
Businesses without websites are at the earliest stage of digital growth. They need exactly what RPG offers. Lower competition from agencies who won't target them.

## Workflow

### Step 1: Identify Target Area
Confirm with Ryan:
- Geographic area or industry vertical
- Business type
- Volume target for this campaign

### Step 2: Find Businesses Without Websites
Sources:
- Google Maps search for business type + location. Filter for listings with no website link.
- Yelp listings without website URLs
- Facebook business pages with no website listed
- Local chamber directories

### Step 3: Verify No Website
- No website URL in Google Maps listing
- No website in social profiles
- If a URL exists, check if it is functional

### Step 4: Qualify the Prospect
- [ ] Business appears active (recent reviews, social posts)
- [ ] Has a phone number or email available
- [ ] Business type aligns with RPG services
- [ ] Not a franchise or corporate chain

### Step 5: Output Lead List
Format as CSV or Excel:
- Business Name, Business Type, Location, Phone, Email, Google Maps URL, Social Profile URL, Last Active Date, Notes

### Step 6: Outreach Preparation
For each qualified lead, note the specific gap (no website, broken website, no social presence) so outreach can be personalized to their exact situation.

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
