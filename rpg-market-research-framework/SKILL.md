---
name: rpg-market-research-framework
description: A repeatable framework for identifying and validating product or service opportunities for Ready, Plan, Grow! by analyzing market language, pain points, and competitive gaps. Use when you need to find a new market opportunity, validate a product idea, or sharpen the positioning of an existing offer.
---

# RPG Market Research Framework

This skill provides a repeatable framework for identifying and validating product or service opportunities for Ready, Plan, Grow! by analyzing market language, pain points, and competitive gaps.

## Core Principles

1.  **Start with the language, not the idea.** The goal is to find what the market is already saying, not to validate a preconceived notion.
2.  **Go where the pain is.** The best product ideas come from places where people are actively complaining.
3.  **The gap is the opportunity.** The most durable product ideas live in the space between what people want and what competitors are offering.

## The Framework

This framework is a four-step process. Execute each step in order.

### Step 1: Broad Market Scan (Language Mapping)

**Goal:** Understand the current language the market is using to talk about the problem space.

**Sources:**

*   **Product Hunt:** Scan the top launches in the relevant category from the last 30-60 days. What problems are they solving? What language do they use in their taglines and descriptions?
*   **YouTube:** Search for videos on the topic with 100k+ views. Read the comments. How do people describe their struggles? What questions do they ask?
*   **Amazon Book Reviews:** Search for top-rated books on the topic. Read the 3 and 4-star reviews. What did people hope to learn? What was missing?

**Output:** A list of common phrases, keywords, and recurring themes.

### Step 2: Deep Dive (Pain Point Extraction)

**Goal:** Find where the target audience is actively complaining and pull their exact words.

**Sources:**

*   **Reddit:** Find the top 3-5 subreddits where the target audience hangs out. Search for terms like "struggling," "overwhelmed," "frustrated," "don't know where to start." Pull the most upvoted posts and comments.
*   **Quora:** Search for questions related to the problem space. Look for questions with a high number of followers and answers.
*   **LinkedIn:** Search for posts from influencers in the space and read the comments. Look for replies from small business owners expressing frustration or confusion.

**Output:** A collection of raw, direct quotes from the target audience. This is your voice-of-customer data.

### Step 3: Competitor Analysis (Gap Identification)

**Goal:** Understand what competitors are offering, how they are priced, and what their customers complain about.

**Sources:**

*   **G2 & Trustpilot:** Look up the top 3-5 competitors. Read the 1, 2, and 3-star reviews. What are the common complaints? What features are missing? What do people say they wish the product did?
*   **Competitor Websites:** Analyze their pricing pages, feature lists, and landing page copy. What is their core value proposition? Who are they targeting?

**Output:** A clear understanding of the competitive landscape and the specific gaps in the market.

### Step 4: Synthesis & Reporting

**Goal:** Synthesize all the research into a clear, actionable report.

**Deliverables:**

1.  **Voice-of-Customer Language Bank:** A spreadsheet containing all the raw language, categorized by theme (e.g., Emotional State, Desire Language, Failure Language). Use the template in `templates/language_bank_template.xlsx`.
2.  **Market Gaps Report:** A document outlining the top 5-10 unmet needs in the market, with supporting evidence from the research. Use the template in `references/market_gaps_report.md`.
3.  **Positioning Brief:** A one-page summary that includes a one-line positioning statement, a draft pitch, and headline options.

## Bundled Resources

*   **`templates/language_bank_template.xlsx`:** A pre-formatted Excel template for the Voice-of-Customer Language Bank.
*   **`references/market_gaps_report.md`:** A Markdown template for the final Market Gaps Report.

## How to Use This Skill

1.  **Clarify the goal.** Before starting, confirm with the user what they are trying to achieve (e.g., find a new product idea, sharpen positioning for an existing offer).
2.  **Execute the framework.** Follow the four steps in order. Do not skip steps.
3.  **Use the templates.** The bundled templates are designed to produce a consistent, high-quality output.
4.  **Deliver the final report.** The Market Gaps Report and Language Bank are the primary deliverables.

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
