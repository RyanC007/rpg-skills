---
name: rpg-mit-influencer-research
description: Identify, evaluate, and recommend influencers for marketing campaigns. Use when researching potential influencer partnerships, analyzing audience quality, or assessing engagement rates.
---

# RPG MIT Influencer Research

## Purpose
This skill systematically identifies and evaluates potential influencers for marketing partnerships. It provides a comprehensive analysis of an influencer\'s audience demographics, engagement metrics, and overall brand alignment to ensure optimal partnership fit and maximize campaign ROI. Use this skill when strategic guidance on influencer marketing is required or when vetting potential collaborators.

## When to Activate
*   When the user requests influencer identification or research.
*   When evaluating potential influencer partnerships for a client.
*   When analyzing audience quality and engagement rates for influencers.
*   When developing an influencer marketing strategy.

## Workflow
1.  **Define Campaign Objectives:** Clarify the client\'s marketing goals, target audience, and desired outcomes for the influencer campaign.
2.  **Initial Influencer Identification:** Utilize search tools and social media platforms to identify potential influencers based on keywords, niche, and audience relevance.
3.  **Audience Quality Analysis:** Evaluate influencer\'s audience demographics, authenticity, and potential for fraud using available tools and data.
4.  **Engagement Rate Assessment:** Calculate and analyze engagement rates across various platforms (likes, comments, shares) to determine audience interaction levels.
5.  **Partnership Fit Evaluation:** Assess the influencer\'s content style, brand values, and past collaborations to ensure alignment with the client\'s brand.
6.  **Compile Research Report:** Synthesize all findings into a comprehensive report detailing suitable influencers, their metrics, and partnership recommendations.

## Inputs Required
| Field                 | Required? | Description                                                              |
| :-------------------- | :-------- | :----------------------------------------------------------------------- |
| Client Campaign Goals | Yes       | Specific objectives for the influencer marketing campaign.               |
| Target Audience       | Yes       | Detailed description of the desired audience demographics and interests. |
| Niche/Keywords        | Yes       | Relevant industry, topics, or keywords for influencer search.            |
| Budget (Optional)     | No        | Available budget for influencer compensation.                            |

## Output Format
A detailed Influencer Research Report in Markdown format, including:
*   Executive Summary
*   List of Recommended Influencers with profiles and contact information.
*   Audience Demographics and Quality Analysis for each influencer.
*   Engagement Rate Metrics across platforms.
*   Assessment of Partnership Fit and potential risks.
*   Strategic Recommendations for collaboration.

## Source Material
*   `/home/ubuntu/knowledge_bases/rpg-marketing-frameworks/research-intelligence/03-influencer-partnership-research-framework.md`

## Guardrails
*   MUST NOT recommend influencers with a history of unethical behavior or controversial content.
*   MUST prioritize audience authenticity and engagement over follower count alone.
*   MUST ensure all data sources for audience and engagement metrics are credible and verifiable.

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
