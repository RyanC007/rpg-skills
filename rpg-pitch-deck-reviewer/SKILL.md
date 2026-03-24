---
name: rpg-pitch-deck-reviewer
description: 6-phase pitch deck analysis system — reviews startup decks, generates financial projections, researches market size, and produces an investor-ready report. Use this skill when a founder needs to prepare their pitch for investors or wants an objective, expert critique before a funding round.
---

# RPG Pitch Deck Reviewer

## Purpose
This skill provides a comprehensive, investor-focused review of startup pitch decks. It analyzes deck structure, clarity, and investor readiness; generates financial projections from the client's own numbers; researches market size (TAM/SAM/SOM); and produces a branded, investor-ready report. Use this skill when a founder needs to prepare their pitch for investors or wants an objective, expert critique before a funding round.

## When to Activate
- "Review my pitch deck"
- "Is my deck investor-ready?"
- "Analyse my startup pitch"
- "Help me prepare for investors"
- "Give me feedback on my pitch"
- "Generate financial projections for my pitch"

## Workflow

### Phase 1: Deck Upload and Intake
1. Request the pitch deck file (PDF, PPTX, or Google Slides link)
2. Collect the financial intake data (see Inputs Required below)
3. Confirm company name, industry, and geographic market

### Phase 2: Deck Structure Analysis
1. Review all slides for clarity, narrative flow, and completeness
2. Assess investor readiness across four dimensions:
   - **Clarity** — Is the pitch compelling and easy to follow?
   - **Objectivity** — Are there blind spots or unsupported assumptions?
   - **Investor Readiness** — What is missing (financials, projections, growth path)?
   - **Confidence** — What existing strengths build credibility?
3. Identify missing slides or sections (problem, solution, market, traction, team, ask)

### Phase 3: Financial Projections
1. Use the client's financial inputs to generate:
   - Revenue projections (3-year simple model)
   - Customer Acquisition Cost (CAC) and Lifetime Value (LTV) analysis
   - Break-even analysis
   - Growth scenarios (conservative, base, optimistic)
2. Generate a custom plug-and-play financial prompt the client can use in ChatGPT for deeper modelling

### Phase 4: Market Size Research
1. Research TAM (Total Addressable Market), SAM (Serviceable Addressable Market), and SOM (Serviceable Obtainable Market) using web research
2. Validate or challenge any market size claims already in the deck
3. Source and cite credible market data

### Phase 5: Investor Prep Package
1. Generate an Investor Readiness Checklist (competitive comparison, customer acquisition, team strengths/gaps)
2. Generate 8–10 common investor questions with model answers tailored to the client's numbers
3. Append a Confidence Builder section highlighting the deck's strongest elements

### Phase 6: Deliver Report
1. Assemble all sections into a structured, branded report
2. Deliver as a Markdown document (or Google Doc if integration is available)
3. Include a prioritised action list — what to fix before the next investor meeting

## Inputs Required

| Field | Required? | Description |
| :--- | :--- | :--- |
| Pitch deck file | Yes | PDF, PPTX, or Google Slides link |
| Company name | Yes | For branding the report |
| Industry | Yes | For market size research |
| Geographic market | Yes | For TAM/SAM/SOM scoping |
| Sales to date | Yes | Revenue generated so far |
| Average order value (AOV) | Yes | Average transaction size |
| Unit cost | Yes | Cost to produce/deliver one unit |
| Retail price | Yes | Selling price |
| Current margin | Yes | Gross margin percentage |
| Estimated repeat purchase rate | No | % of customers who buy again |
| Planned marketing spend | No | Budget allocated to marketing |
| Planned team spend | No | Budget allocated to headcount |
| Planned e-commerce spend | No | Budget allocated to digital/e-comm |

## Output Format
A comprehensive **Investor-Ready Report** in Markdown format, structured as:
1. Executive Summary
2. Deck Structure Feedback (slide-by-slide where relevant)
3. Financial Projections (3-year model, CAC/LTV, break-even)
4. Market Size Analysis (TAM/SAM/SOM with sources)
5. Investor Readiness Checklist
6. Investor Q&A Prep (8–10 questions with model answers)
7. Confidence Builder
8. Priority Action List

## Source Material
- `/home/ubuntu/knowledge_bases/rpg-pitch-deck-review/docs/rpg_workflow_design.md`
- `/home/ubuntu/knowledge_bases/rpg-pitch-deck-review/docs/base44_app_specification.md`
- `/home/ubuntu/knowledge_bases/rpg-pitch-deck-review/docs/integration_research.md`

## Guardrails
- MUST NOT provide legally binding financial advice or investment recommendations
- MUST NOT fabricate market size data — all TAM/SAM/SOM figures must be sourced and cited
- MUST NOT share the client's financial data or deck contents with any third party

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
