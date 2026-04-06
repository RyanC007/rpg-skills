---
name: rpg-mit-market-trends
description: Researches current and emerging industry trends, analyzes their potential impact, and translates them into actionable strategic implications for clients. Use when asked to research market trends, identify industry shifts, or understand strategic implications of market developments.
---

# RPG MIT Market Trends

## Purpose
This skill is designed to conduct comprehensive research into current and emerging industry trends. It then analyzes these trends to identify their potential impact and translates them into actionable strategic implications tailored for the client's specific context. This helps clients anticipate market shifts and adapt their strategies proactively.

## When to Activate
* When asked to research market trends.
* When asked to identify industry shifts or emerging patterns.
* When needing to understand the strategic implications of market developments.
* When the client requires insights into future market direction.

## Workflow
1. **Understand Client Context:** Begin by clarifying the client's industry, specific business objectives, and any particular areas of interest regarding market trends.
2. **Identify Key Trend Categories:** Systematically search for trends across relevant categories such as technological advancements, consumer behavior shifts, regulatory changes, economic indicators, and competitive landscape developments.
3. **Data Collection:** Utilize web search, industry reports, news articles, and specialized databases to gather comprehensive data on identified trends. Prioritize credible and recent sources.
4. **Trend Analysis:** Evaluate the significance, trajectory, and potential impact of each trend. Assess its relevance to the client's business model and market position.
5. **Strategic Implication Development:** Translate raw trend data into clear, concise strategic implications. This involves outlining opportunities, threats, and recommended actions for the client.
6. **Report Generation:** Compile findings into a structured report, highlighting key trends, their analysis, and actionable strategic recommendations.

## Inputs Required
| Field | Required? | Description |
|---|---|---|
| Client Industry | Yes | The industry in which the client operates. |
| Client Business Objectives | Yes | The primary goals or challenges the client is facing. |
| Specific Areas of Interest | No | Any particular market segments or trend types the client wants to focus on. |

## Output Format
A comprehensive market trend intelligence report, including:
* An executive summary of key findings.
* Detailed analysis of identified market trends.
* Strategic implications for the client's business.
* Actionable recommendations based on the trend analysis.

## Source Material
* `/home/ubuntu/knowledge_bases/rpg-marketing-frameworks/research-intelligence/04-market-trend-intelligence-framework.md`
* `truth-engine-manus/agents/trends_agent.py`

## Guardrails
* MUST NOT provide financial advice or make investment recommendations.
* MUST NOT speculate on market trends without supporting data or credible sources.
* MUST ensure all strategic implications are directly derived from researched trends and client context, avoiding generic advice.
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
