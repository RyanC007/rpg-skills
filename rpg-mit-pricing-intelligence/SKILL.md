---
name: rpg-mit-pricing-intelligence
description: This skill analyses competitor pricing strategies and recommends optimal positioning.
---

# rpg-mit-pricing-intelligence

## Purpose
This skill is designed to conduct in-depth analysis of competitor pricing strategies. It helps agents understand the market landscape, identify pricing benchmarks, and ultimately recommend optimal pricing positions for products or services to maximize client profitability and market share.

## When to Activate
*   "Analyze competitor pricing"
*   "Develop a pricing strategy"
*   "Recommend optimal pricing"
*   "Conduct pricing intelligence"
*   "Evaluate market pricing"

## Workflow
1.  **Identify Key Competitors:** Determine the primary competitors in the target market.
2.  **Gather Pricing Data:** Collect pricing information for competitor products/services, including features, bundles, and discount structures.
3.  **Analyze Pricing Models:** Evaluate the pricing models (e.g., subscription, one-time, tiered) and strategies (e.g., value-based, cost-plus, penetration) employed by competitors.
4.  **Perform Comparative Analysis:** Create a detailed comparison matrix highlighting pricing differences, value propositions, and market positioning.
5.  **Identify Gaps and Opportunities:** Pinpoint areas where the client's pricing can be optimized for competitive advantage.
6.  **Formulate Pricing Recommendations:** Develop data-driven recommendations for optimal pricing strategies and positioning.
7.  **Deliver Pricing Intelligence Report:** Present a comprehensive report outlining findings, analysis, and actionable pricing recommendations.

## Inputs Required
| Field                 | Required? | Description                                                                                             |
| :-------------------- | :-------- | :------------------------------------------------------------------------------------------------------ |
| Client Product/Service Details | Yes       | Comprehensive information about the client's product or service, including features, costs, and target audience. |
| Target Market         | Yes       | Definition of the specific market segment or industry to analyze.                                       |
| Known Competitors     | No        | A list of known competitors to prioritize research; if not provided, the skill will identify them.      |
| Pricing Objectives    | Yes       | The client's goals for pricing (e.g., market share, profit margin, premium positioning).                |

## Output Format
A comprehensive "Pricing Intelligence Report" in Markdown format. The report will include:
*   Executive Summary
*   Competitor Overview
*   Detailed Pricing Analysis (including comparison matrices)
*   Identified Gaps and Opportunities
*   Optimal Pricing Strategy Recommendations
*   Actionable Implementation Steps

## Source Material
`/home/ubuntu/knowledge_bases/rpg-marketing-frameworks/research-intelligence/05-competitive-pricing-intelligence-framework.md`

## Guardrails
*   MUST NOT recommend pricing strategies that violate ethical guidelines or anti-trust laws.
*   MUST NOT make pricing decisions without explicit client approval.
*   MUST NOT disclose proprietary client information to competitors or third parties.
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
