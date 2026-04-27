---
name: rpg-brand-audit
description: Conducts a comprehensive, data-backed Brand 360 Audit for any client. Use when a user requests a brand audit, wants to evaluate a client's brand presence before onboarding, or needs to run the RPG 5-area Brand 360 framework. Analyzes Website, Brand Voice, SEO & Search Visibility, Social Media, and Competitive Position using real-time SERP data. Produces a scored, cited, prioritized audit report ready for client delivery.
---

# RPG Brand 360 Audit Skill

## Purpose

This skill runs the Ready, Plan, Grow! Brand 360 Audit. It is used at the start of every new client engagement to establish a baseline, identify what is costing the client customers, and build a prioritized fix plan. The output is a professional, cited audit report that can be delivered directly to the client.

## Core Rules

1. **No guessing.** Every claim about search rankings, visibility, or competitive position must be backed by real-time SERP data from the `serp_audit.py` script. Never invent or estimate rankings.
2. **Cite everything.** All SERP data must be cited in the report with the keyword queried and the position returned.
3. **Score 1-5 per area.** Use the scoring rubric in the `references/scoring_rubric.md` file. Do not deviate from it.
4. **Prioritize by impact.** The action plan must rank fixes by what is actively costing the client customers, not by what is easiest to fix.
5. **Tier 2 guardrails apply.** Client name is permitted in their own deliverable. No other client names. No internal RPG links or repo paths.

---

## Workflow

### Step 1: Intake

Ask the user for the following. Do not proceed without at least the brand name, domain, and 3-5 target keywords.

| Input | Required | Notes |
| :--- | :--- | :--- |
| Brand Name | Yes | The client's business name |
| Primary Domain | Yes | e.g., `example.com` |
| Target Keywords | Yes | 3-5 terms the client should rank for |
| Known Competitors | Preferred | 3 ideally; if unknown, SERP data will surface them |
| Business Type | Yes | Local, regional, national, or e-commerce |
| Social Profiles | Preferred | URLs to LinkedIn, Instagram, Facebook, etc. |

---

### Step 2: SERP Data Collection

Set the API key and run the SERP audit script. This is mandatory before writing any analysis.

```bash
export SERP_API_KEY="a20c14ca13c581ae1f986e42f29027a8f6e60ddee76a12c8c14ea90de8afb2ee"

python3 /home/ubuntu/skills/rpg-brand-audit/scripts/serp_audit.py \
  --brand "Client Brand Name" \
  --domain "clientdomain.com" \
  --keywords "keyword one, keyword two, keyword three"
```

The script outputs a JSON file saved to `/tmp/serp_audit_results.json`. Read this file before proceeding to Step 3.

**What the script collects:**
- Organic ranking position for each target keyword (or "Not in top 20")
- Whether the brand appears in the Local Pack for any keyword
- The top 5 competitor domains surfaced in organic results
- Whether a Google Knowledge Panel is present for the brand name

---

### Step 3: Website Analysis

Browse the client's website directly. Check the following and record findings:

**Clarity Test (10-second rule)**
- Can a first-time visitor understand what the business does within 10 seconds?
- Is the value proposition above the fold?

**Conversion Path**
- Are CTAs present, specific, and visible?
- Is there a clear next step on every major page?

**Mobile & Speed**
- Is the site mobile-responsive?
- Does it load in under 3 seconds? (Use browser observation, not a tool.)

**Content Structure**
- Is there a clear H1 on every page?
- Are service or product pages present and descriptive?

Score this area using `references/scoring_rubric.md` Area 1.

---

### Step 4: Brand Voice Analysis

Review the homepage copy, About page, and any social profiles available.

**Consistency Check**
- Does the brand sound the same across the website and social channels?
- Is there a clear tone (professional, casual, technical, friendly)?

**Clarity Check**
- Does the messaging speak directly to the ideal customer?
- Is it clear who the business serves and what problem it solves?

**Jargon Check**
- Does the copy use industry jargon that a customer would not understand?
- Does it make vague claims ("best in class," "industry-leading") without proof?

Score this area using `references/scoring_rubric.md` Area 2.

---

### Step 5: SEO & Search Visibility Analysis

Use the SERP data from Step 2 as the primary source. Do not guess or estimate.

**Keyword Rankings**
- For each target keyword, report the exact position returned by the SERP script.
- If the brand does not appear in the top 20, report "Not in top 20."

**Local Pack**
- Does the brand appear in the Local Pack for any keyword? (From SERP data.)
- Is the Google Business Profile complete? (Check directly if a GBP URL is available.)

**On-Page Basics**
- Does the homepage have a descriptive meta title and meta description? (View page source or use browser dev tools.)
- Is the H1 tag present and keyword-relevant?

Score this area using `references/scoring_rubric.md` Area 3.

---

### Step 6: Social Media Analysis

Review each social profile provided by the user. If no profiles were provided, check for common platforms (LinkedIn, Facebook, Instagram) by searching `[Brand Name] site:linkedin.com` etc.

**Profile Completeness**
- Is the bio/about section complete?
- Is the profile photo and cover image branded?
- Is the website link present?

**Content Activity**
- When was the last post?
- What is the approximate posting frequency?
- What is the content mix (educational, promotional, personal, engagement)?

**Engagement Signal**
- Are posts receiving comments, shares, or reactions?
- Is the brand responding to comments?

Score this area using `references/scoring_rubric.md` Area 4.

---

### Step 7: Competitive Position Analysis

Use the competitor domains surfaced in the SERP data from Step 2, plus any competitors provided by the user.

**Search Share Comparison**
- For each target keyword, note which competitor ranks above the client.
- Identify the competitor that appears most frequently across all keywords.

**Positioning Gaps**
- Browse the top competitor's website briefly. What are they doing well?
- What is the client doing that the competitor is not? (This is a potential differentiator.)
- Are there keywords the competitors rank for that the client does not? (These are content opportunities.)

Score this area using `references/scoring_rubric.md` Area 5.

---

### Step 8: Score Calculation

After completing all five area analyses, calculate the overall Brand Health Score.

```
Overall Score = (Area 1 + Area 2 + Area 3 + Area 4 + Area 5) / 5
```

Map the overall score to a band:

| Score | Band | Description |
| :--- | :--- | :--- |
| 4.5 - 5.0 | Strong | Brand is well-positioned. Focus on optimization. |
| 3.5 - 4.4 | Healthy | Solid foundation with clear improvement areas. |
| 2.5 - 3.4 | Developing | Functional but missing key elements. Needs structured work. |
| 1.5 - 2.4 | At Risk | Multiple areas actively costing the business customers. |
| 1.0 - 1.4 | Critical | Foundational issues across the board. Immediate action required. |

---

### Step 9: Build the Action Plan

Identify the top 3-5 fixes. Rank them by business impact, not ease of execution.

**Prioritization Logic:**
1. Anything scoring 1 or 2 in an area is a priority.
2. Within low-scoring areas, prioritize fixes that affect customer acquisition first (SEO visibility, website conversion path).
3. Brand voice and social media fixes are secondary unless they are creating active reputational harm.

---

### Step 10: Generate the Report

Write the final audit report using the template at `templates/brand_audit_report.md`.

**Mandatory report elements:**
- Client name and date
- Executive summary (2-3 sentences, plain language)
- Score table for all 5 areas
- Detailed findings for each area with citations from SERP data
- Overall Brand Health Score and band
- Prioritized action plan with specific next steps

Save the completed report to `/tmp/[client_name]_brand_audit.md`.

---

## Output Standard

The final report must be written in plain, direct language consistent with the RPG brand voice. No corporate jargon. No vague claims. Every data point must be traceable to either the SERP script output or direct observation of the client's website or social profiles.

The report is a Tier 2 deliverable. The client's name may appear throughout. No other client names, no internal RPG links, no agent infrastructure details.

---

## Resources

- `scripts/serp_audit.py` — Runs real-time SERP queries for keyword rankings, local pack presence, and competitor surfacing.
- `references/scoring_rubric.md` — Detailed scoring criteria for all 5 areas.
- `templates/brand_audit_report.md` — The final report template.
