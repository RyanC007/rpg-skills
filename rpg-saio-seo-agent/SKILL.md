---
name: rpg-saio-seo-agent
description: "Develop and execute comprehensive SEO and AEO (Answer Engine Optimization) strategies. Use for generating SEO/AEO strategies, keyword research, competitor analysis, and creating 6-month content plans for business growth. Supports both new businesses (Foundational Track) and existing websites (Supercharged Track)."
---

# rpg-saio-seo-agent

## Purpose
This skill provides a comprehensive 15-phase system for developing and executing SEO (Search Engine Optimization) and AEO (Answer Engine Optimization) strategies. It is designed to cater to both new businesses requiring foundational SEO/AEO and existing businesses seeking supercharged growth. The skill ensures a data-driven approach to improving online visibility and capturing relevant search traffic.

## When to Activate
*   User requests SEO strategy development.
*   User asks for AEO strategy.
*   User needs keyword research.
*   User requires competitor analysis for search engines.
*   User wants a 6-month content plan focused on SEO/AEO.
*   When optimizing online presence for search and answer engines.

## Workflow Tracks
This skill adapts its approach based on the business's current stage and the files provided:

1.  **Track 1 (Foundational - 12 Phases):** Designed for new businesses or those establishing their initial online presence. Triggered when NO Screaming Frog export is provided.
2.  **Track 2 (Supercharged - 15 Phases):** Tailored for existing businesses aiming for advanced optimization. Triggered when a Screaming Frog export (`.csv` or `.xlsx`) IS provided.

## Inputs Required
| Field | Required? | Description |
|---|---|---|
| Company Knowledge Base | Yes | A document (`.md` or `.json`) containing the client's business, mission, services, target audience, and geographic areas. |
| Screaming Frog Export | **Yes (for Track 2)** | A `.csv` or `.xlsx` export from a Screaming Frog crawl. Required to trigger the Supercharged Track (Phases 13-15). |
| Brand Guidelines | No | PDF or MD detailing brand voice and messaging. |
| Existing Sitemap | No | Current site structure to prevent duplicate content recommendations. |
| Known Competitors | No | A list of known competitor URLs. |

## The 15-Phase Methodology

Follow this exact methodology in sequence. Phases 13-15 are only for clients with existing websites (Track 2).

### PHASE 1-12: Standard Research (For All Clients)
1.  **Business Context Analysis:** Deeply understand the business, value props, target markets, and competitive positioning using the provided Knowledge Base.
2.  **Keyword Research:** Identify 100+ high-value keywords (transactional, informational, local, long-tail) using browser search tools.
3.  **AEO Research:** Research Answer Engine Optimization best practices and identify 50+ question-based opportunities.
4.  **Competitive Intelligence:** Analyze 4-6 top competitors to identify their strategies, strengths, and weaknesses. Use `similarweb-analytics` skill if available.
5.  **Strategic Recommendations:** Synthesize all research into clear, actionable strategic pillars and content opportunities.
6.  **Comprehensive Strategy Document:** Create the main `[Company]_SEO_AEO_Strategy.md` document.
7.  **Keyword Database:** Create the `[Company]_Keyword_Database.md` with all organized keywords.
8.  **AEO Question Database:** Create the `[Company]_AEO_Question_Database.md` with 50+ questions.
9.  **Executive Summary:** Create the quick-reference `[Company]_SEO_Executive_Summary.md`.
10. **Actionable Content Plan Spreadsheet:** Generate the core deliverable `[Company]_Content_Plan.xlsx` using the provided Python script (see Bundled Resources).
11. **Content Plan User Guide:** Create the `[Company]_Content_Plan_User_Guide.md`.
12. **Final Delivery:** Package and deliver all initial assets.

### PHASE 13-15: Supercharged Track (For Existing Websites)
*Triggered only if a Screaming Frog export is provided.*

13. **Technical SEO Analysis:** Analyze the Screaming Frog crawl export to identify and prioritize all technical SEO issues. 
    *   **CRITICAL:** You MUST read `references/Technical_SEO_Analysis_Framework.md` before executing this phase.
    *   Generate the `[Company]_Technical_SEO_Audit_and_Fixes.xlsx` using the provided Python script.
14. **Competitor Content Analysis:** Analyze competitor content to determine publishing frequency, identify content gaps, and establish an outpacing strategy.
    *   **CRITICAL:** You MUST read `references/Competitor_Content_Analysis_Methodology.md` before executing this phase.
    *   Create the `[Company]_Competitor_Content_Analysis.md` report.
15. **Final Supercharged Delivery:** Update the Content Plan with gap analysis findings and deliver all 15 phases of assets to the user.

## Bundled Resources

### Scripts
You MUST use these scripts to generate the required Excel deliverables. Do not attempt to build complex Excel files from scratch.

*   `scripts/generate_enhanced_content_plan.py`: Run this to generate the `Enhanced_Content_Plan_Template.xlsx`. Once generated, populate it with your research findings.
*   `scripts/generate_technical_seo_spreadsheet.py`: Run this to generate the `Technical_SEO_Audit_Template.xlsx`. Once generated, populate it with your technical audit findings (Track 2 only).

### References
Load these into context only when executing their specific phases:
*   `references/Technical_SEO_Analysis_Framework.md`: Read before Phase 13.
*   `references/Competitor_Content_Analysis_Methodology.md`: Read before Phase 14.
*   `references/Recommended_Project_Files_Guide_v2.md`: Reference for understanding required inputs.

### Templates
*   `templates/Supercharged_SEO_AEO_Master_Prompt.md`: The original master prompt this skill is based on.
*   `templates/Technical_SEO_Audit_Template.xlsx`: Blank template (can be generated via script).
*   `templates/Enhanced_Content_Plan_Template.xlsx`: Blank template (can be generated via script).

## Guardrails
*   MUST NOT implement any SEO/AEO tactics that violate search engine guidelines (e.g., black-hat SEO).
*   MUST prioritize user experience and content quality over purely technical optimization.
*   MUST NOT make direct changes to the user's website without explicit approval for each change. Instead, provide recommendations and actionable steps.
*   MUST save findings frequently to text files during research phases to prevent context loss.
*   MUST prioritize all technical issues as P1/P2/P3/P4 as defined in the Technical SEO Framework.

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
