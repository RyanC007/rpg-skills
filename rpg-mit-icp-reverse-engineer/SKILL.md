---
name: rpg-mit-icp-reverse-engineer
description: Reverse-engineers the Ideal Customer Profile from real customer data — reviews, social comments, CRM records, and interviews.
---

# RPG MIT ICP Reverse Engineer

## Purpose
This skill creates comprehensive, data-driven Ideal Customer Profiles (ICPs) by analyzing real customer patterns — not generic buyer persona templates. It works backwards from actual customers to identify who converts, why they buy, and what they have in common. Use this skill when a client needs to sharpen their targeting, improve messaging, or understand why their best customers chose them.

## When to Activate
- "Who is my ideal customer?"
- "Help me build a customer persona"
- "Reverse-engineer my ICP"
- "I want to find more customers like my best ones"
- "Analyze my customer base"
- "Why are my customers buying from me?"

## Workflow

### Phase 1: Business Foundation Intake
1. Collect company name, industry, and business model (B2B/B2C)
2. Collect product/service description, geographic markets, and customer base size
3. Collect average deal size, customer lifetime value, and sales cycle length
4. Identify top 3 business challenges or goals

### Phase 2: Customer Data Collection
1. Request a list of 5–10 high-value existing customers (anonymized if needed)
2. Request any available CRM data, survey responses, or support ticket themes
3. Request sales call notes, win/loss analysis, or customer testimonials
4. If no data is available, pivot to social listening and review mining

### Phase 3: Pattern Analysis
1. Analyze customer demographics: industry, company size, role/title, geography
2. Identify behavioral patterns: how they found the business, what triggered purchase
3. Extract psychographic signals: language used in reviews, pain points, aspirations
4. Mine public reviews (Google, Yelp, G2, Capterra, Trustpilot) for sentiment patterns
5. Analyze social comments and community discussions for authentic customer voice

### Phase 4: ICP Construction
1. Build 2–3 distinct ICP segments ranked by value and conversion likelihood
2. For each segment: define demographics, firmographics, psychographics, triggers, and objections
3. Identify the "jobs to be done" — what outcome the customer is really hiring the product for
4. Document the language patterns to use in marketing and sales copy

### Phase 5: Deliver ICP Report
1. Produce a structured ICP document with named personas
2. Include messaging recommendations for each segment
3. Include a "where to find them" channel recommendation
4. Include a "red flags" section — who NOT to target

## Inputs Required

| Field | Required? | Description |
| :--- | :--- | :--- |
| Company name and industry | Yes | Establishes context for customer analysis |
| Business model (B2B/B2C) | Yes | Determines the type of ICP to build |
| Product/service description | Yes | Needed to understand what customers are buying |
| Customer list or data | Yes (min 3–5) | Real customers to analyze — can be anonymized |
| Reviews or testimonials | No | Enriches psychographic analysis |
| CRM or sales data | No | Accelerates pattern identification |

## Output Format
A structured **ICP Report** in Markdown, including:
- Executive summary of key findings
- 2–3 named ICP personas with full profiles (demographics, psychographics, triggers, objections)
- Messaging recommendations per segment
- Channel recommendations (where to find each ICP)
- Red flags — who to avoid targeting
- Sample copy lines in the customer's own language

## Source Material
- `/home/ubuntu/knowledge_bases/rpg-marketing-frameworks/research-intelligence/02-framework-for-reverse-engineering-your-icp.md`
- `truth-engine-manus/agents/content_customer_analysis_agent.py`

## Guardrails
- MUST NOT build personas based on assumptions alone — all claims must be grounded in data provided or researched
- MUST NOT request or store personally identifiable information beyond what is voluntarily provided
- MUST NOT recommend targeting strategies that discriminate based on protected characteristics

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
