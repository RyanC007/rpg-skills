---
name: rpg-mit-social-listening
description: "Monitors brand mentions, sentiment, and conversations across social platforms. Use when social media monitoring is requested, public sentiment needs understanding, campaign impact requires tracking, or key influencers and communities need identification."
---

# rpg-mit-social-listening

## Purpose
This skill monitors and analyzes brand mentions, sentiment, and conversations across various social media platforms. It provides insights into public perception, tracks campaign performance, and identifies emerging trends related to a specific brand or topic.

## When to Use
*   Monitor social media for a brand or topic.
*   Understand public sentiment towards a product or service.
*   Track the impact of a marketing campaign on social platforms.
*   Identify key influencers or communities discussing a specific subject.

## Workflow
1.  **Define Monitoring Parameters:** Identify the brand, keywords, hashtags, and social platforms to monitor.
2.  **Data Collection:** Utilize `twitter_agent.py` and other relevant tools to collect social media data (mentions, posts, comments) based on the defined parameters.
3.  **Sentiment Analysis:** Process collected data to determine the overall sentiment (positive, negative, neutral) towards the brand or topic.
4.  **Conversation Analysis:** Identify key themes, topics, and recurring discussions within the social media data.
5.  **Trend Identification:** Detect emerging trends, popular content, and influential voices related to the monitored subject.
6.  **Reporting:** Compile findings into a comprehensive report detailing brand mentions, sentiment, key conversations, and identified trends.

## Inputs Required
| Field              | Required? | Description                                                                                             |
| :----------------- | :-------- | :------------------------------------------------------------------------------------------------------ |
| `brand_name`       | Yes       | The name of the brand or entity to monitor.                                                             |
| `keywords`         | Yes       | A list of keywords and hashtags to track across social platforms.                                       |
| `social_platforms` | No        | A list of specific social media platforms to monitor (e.g., Twitter, Reddit). If not provided, default to common platforms. |
| `date_range`       | No        | The period for which social data should be collected (e.g., "past week", "last month").             |

## Output Format
The agent delivers a comprehensive social listening report, typically in Markdown or PDF format. This report includes: a summary of brand mentions, sentiment analysis results (overall and by topic), identification of key themes and conversations, a list of influential users, and detected trends. The report will provide actionable insights based on the analysis.

## Source Material
*   `/home/ubuntu/rpg-branded-agents/knowledge_bases/rpg-marketing-frameworks/research-intelligence/06-social-listening-intelligence-framework.md`
*   `truth-engine-manus/agents/twitter_agent.py`

## Guardrails
*   MUST NOT engage in any form of direct interaction or posting on social media platforms.
*   MUST only collect publicly available data and adhere strictly to platform terms of service and privacy policies.
*   MUST NOT identify or store personal identifiable information (PII) of individuals unless explicitly authorized and anonymized.
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
