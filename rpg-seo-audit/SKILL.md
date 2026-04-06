---
name: rpg-seo-audit
description: Runs a comprehensive technical SEO audit on a website. Use when auditing a client's or RPG's website for SEO health, identifying issues, and producing an action plan. Covers on-page SEO, technical issues, content gaps, and keyword opportunities. Delivers a structured report with prioritized recommendations.
---

# Rpg Seo Audit

OUTPUT_TIER: 2 (Client-Facing) or 3 (Internal) depending on audience

## Guardrails
- Tier 2 if delivering to client: no internal repo references, no other client names
- Tier 3 if internal RPG audit: full context allowed

## Purpose
Conduct a thorough SEO audit and produce a prioritized action plan. Uses SimilarWeb data, Google Search Console data if available, and direct site inspection.

## Audit Checklist

### Technical SEO
- [ ] Page speed (Core Web Vitals)
- [ ] Mobile responsiveness
- [ ] HTTPS and security
- [ ] XML sitemap present and submitted
- [ ] Robots.txt configured correctly
- [ ] Canonical tags in place
- [ ] No broken links (4xx errors)
- [ ] Structured data / schema markup

### On-Page SEO
- [ ] Title tags (unique, under 60 chars, keyword-targeted)
- [ ] Meta descriptions (unique, under 160 chars)
- [ ] H1 tags (one per page, keyword-relevant)
- [ ] Image alt text
- [ ] Internal linking structure
- [ ] Content quality and depth

### Content Gaps
- [ ] Target keyword coverage vs competitors
- [ ] Missing topic clusters
- [ ] Thin content pages (under 300 words)

## Report Structure
1. Executive Summary (3-5 bullet points, most critical issues)
2. Technical Issues (prioritized: Critical / High / Medium / Low)
3. On-Page Opportunities
4. Content Gap Analysis
5. Quick Wins (fixable in under 1 hour)
6. 30-Day Action Plan

## Tools
- Use similarweb-analytics skill for traffic and competitor data
- Use browser tools to inspect page source and check meta tags

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
