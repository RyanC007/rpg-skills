---
name: rpg-truth-engine
description: Orchestrates comprehensive market research and competitive intelligence. Use to conduct market research, competitive analysis, and generate strategic reports.
---

# RPG Truth Engine

## Purpose
This skill serves as the master research orchestrator for Ready Plan Grow, designed to conduct comprehensive market research and competitive intelligence. It provides a holistic view of the market landscape and competitor strategies, informing strategic decisions.

## When to Activate
- "Conduct comprehensive market research."
- "Perform competitive intelligence analysis."
- "Orchestrate a full market and competitor landscape assessment."
- "Generate a battle card report."
- "Need a master research orchestrator."

## Workflow
1. **Phase 1: Market Research**
    1. Activate and coordinate 5 specialized agents for data collection:
        - Reddit Agent: Gather insights from Reddit communities.
        - LinkedIn Agent: Analyze professional networks and industry trends.
        - Twitter Agent: Monitor real-time conversations and sentiment.
        - YouTube Agent: Research video content and audience engagement.
        - Trends Agent: Identify emerging market trends and shifts.
    2. Synthesize findings from all market research agents to identify key themes, opportunities, and challenges.
2. **Phase 2: Competitive Intelligence**
    1. Identify key competitors based on market research findings.
    2. Conduct deep analysis of identified competitors, including their products, services, marketing strategies, and customer reviews.
    3. Perform a gap analysis to identify areas where the client can differentiate or improve.
    4. Generate strategic recommendations based on competitive insights.
    5. Deliver a comprehensive battle card report summarizing competitive advantages, weaknesses, and strategic implications.

## Inputs Required
| Field | Required? | Description |
|---|---|---|
| Client Name | Yes | The name of the client for whom the research is being conducted. |
| Research Objective | Yes | A clear statement of what information is needed and why. |
| Target Market | No | Specific demographics, geographies, or industries to focus on. |
| Known Competitors | No | A list of known competitors to prioritize analysis. |

## Output Format
A comprehensive market research and competitive intelligence report, including:
- Executive Summary
- Market Overview (trends, opportunities, challenges)
- Customer Sentiment Analysis
- Competitor Battle Card (strengths, weaknesses, strategies, differentiation)
- Strategic Recommendations

## Source Material
- `truth-engine-manus/` repository

## Guardrails
- MUST NOT make speculative claims without supporting data.
- MUST NOT disclose confidential client information during research or in reports.
- MUST ensure all data sources are credible and properly cited.
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
