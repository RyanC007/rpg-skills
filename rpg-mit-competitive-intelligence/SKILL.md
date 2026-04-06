---
name: rpg-mit-competitive-intelligence
description: This skill provides tools and workflows for gathering and analyzing competitive intelligence, specifically tailored for the RPG (Role-Playing Game) market, leveraging MIT-style analytical frameworks.
license: Complete terms in LICENSE.txt
---

# RPG MIT Competitive Intelligence

This skill is designed to assist in the collection, analysis, and strategic application of competitive intelligence within the Role-Playing Game (RPG) industry. It integrates methodologies inspired by MIT's analytical frameworks to provide a structured approach to understanding market dynamics, competitor strategies, and emerging trends.

## Purpose

The primary purpose of this skill is to empower users to make informed strategic decisions in the highly competitive RPG market. By providing a systematic way to gather and interpret competitive data, it helps identify opportunities, mitigate threats, and optimize product development and marketing efforts.

## Key Features

- **Market Trend Analysis**: Tools for identifying and tracking key trends in the RPG market, including genre popularity, platform shifts, and player demographics.
- **Competitor Profiling**: Workflows to create detailed profiles of competing RPG titles and companies, covering aspects like game mechanics, monetization strategies, community engagement, and market share.
- **SWOT Analysis Integration**: Guidance and templates for conducting Strengths, Weaknesses, Opportunities, and Threats (SWOT) analysis based on collected intelligence.
- **Data Visualization**: Capabilities to visualize competitive data, making complex information more accessible and actionable.
- **Strategic Recommendation Generation**: Frameworks to translate competitive insights into actionable strategic recommendations for product development, marketing, and business expansion.

## Use Cases

- **New RPG Development**: Informing the design and feature set of new RPG titles by understanding market gaps and competitor offerings.
- **Marketing Strategy Optimization**: Refining marketing campaigns based on competitor messaging, audience targeting, and promotional activities.
- **Investment and Partnership Decisions**: Providing data-driven insights for potential investors or partners looking to enter or expand within the RPG market.
- **Market Entry Strategy**: Developing comprehensive strategies for entering new segments or geographies within the RPG industry.

## How to Use

To effectively utilize this skill, follow these general steps:

1.  **Define Intelligence Objectives**: Clearly articulate what competitive information is needed and why.
2.  **Gather Data**: Use the provided tools and workflows to collect data from various sources (e.g., market reports, competitor websites, social media, player forums).
3.  **Analyze Information**: Apply the MIT-inspired analytical frameworks to interpret the gathered data and identify key insights.
4.  **Generate Reports and Recommendations**: Compile findings into comprehensive reports and formulate strategic recommendations.
5.  **Implement and Monitor**: Apply the recommendations and continuously monitor the market for changes.

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
