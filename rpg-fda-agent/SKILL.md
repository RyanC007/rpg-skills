---
name: rpg-fda-agent
version: 1.0
description: Manages all content, SEO, strategy, and business development tasks for Foodesign Associates. Use this skill for any task involving Foodesign Associates, including content creation, SEO strategy, proposal generation, or business development.
author: Trinity (Manus AI) for Ready Plan Grow
created: 2026-02-24
agents: Scarlett
---

# RPG FDA Agent — Foodesign Associates

This skill provides the necessary context and guidelines for any agent working on deliverables for Foodesign Associates (FDA), a client of Ready Plan Grow (RPG). It ensures all work—spanning content, SEO, strategy, and business development—is accurate, on-brand, and aligned with FDA's growth objectives.

## Purpose
To activate the full Foodesign Associates client context, including brand identity, strategic positioning, SEO priorities, target audience, and content voice. This ensures all outputs are consistent, high-quality, and directly support the client's business goals.

## When to Activate
Activate this skill for any task related to Foodesign Associates. Examples include:
- Generating content (blog posts, social media, proposals, case studies) for Foodesign.
- Developing or executing SEO strategies for Foodesign's website.
- Crafting business development materials or proposals for Foodesign.
- Updating or referencing the Foodesign Associates knowledge base.

## Client Profile

| Field | Detail |
| :--- | :--- |
| **Company** | Foodesign Associates |
| **Tagline** | The Food Service Design Agency |
| **Established** | 1977 (50 years of experience) |
| **Location** | Charlotte, NC |
| **Phone** | 704-545-6151 |
| **Website** | https://foodesignassociates.com |
| **Certifications** | WOSB, EDWOSB |
| **Projects Completed** | 4,500+ |
| **Primary Audience** | Architects and the architectural community nationwide |
| **Secondary Audience** | Foodservice operators, developers, government agencies |

## Brand Positioning
Foodesign's core differentiator is its **"Architectural Partnership"** positioning. They operate as an independent, design-only firm, partnering with architects without equipment sales or supplier affiliations. This ensures unbiased recommendations always prioritize the client's best interests.

**Key differentiators to always emphasize:**
- 50 years of experience and 4,500+ completed projects.
- Independent design-only firm; no equipment sales.
- Direct principal access from project inception to completion.
- Proven record of outstanding budget accuracy.
- Personable team with extensive large agency capabilities.

## SEO Priorities
- **Primary keyword opportunity:** "Commercial Laundry" vertical (zero competition, high relevance).
- **High-value targets:** "restaurant floor plan", "commercial kitchen layout", "foodservice design".
- **Strategic goal:** Transition from a "trusted" to a "trusted and visible" entity, making the website a primary growth engine.

## Content Voice
- **Tone:** Confident, warm, and authoritative.
- **Style:** Professional yet approachable, expertise-led, focusing on experience and project outcomes.
- **Language:** Avoid jargon; write for intelligent architects who may not be foodservice specialists.
- **Emphasis:** Partnership, reliability, and precision.

## Workflow

### For Content Tasks
1. Load the FDA Master Knowledge Base from `foodesign-associates-client/knowledge-base/FDA_Master_Knowledge_Base.md`.
2. Confirm the specific content type (e.g., blog, social media post, proposal, case study).
3. Identify the target keyword or topic for the content.
4. Draft content in the FDA voice, emphasizing expertise and an architect-focused perspective.
5. Include a clear Call to Action (CTA) directing to `foodesignassociates.com`.

### For SEO Tasks
1. Reference the 60-day blogging plan located in `foodesign-associates-client/strategy/`.
2. Prioritize content creation around the commercial laundry and kitchen layout keyword verticals.
3. Structure content for optimal featured snippet capture (e.g., using clear headers, lists, and definitions).
4. Ensure all new pages target a primary keyword and 2–3 supporting keywords.

### For Strategy Tasks
1. Consult the full knowledge base and the strategy folder for comprehensive context.
2. Frame all recommendations to reinforce the "Architectural Partnership" positioning.
3. Identify opportunities to increase inbound leads from the architectural community.
4. Benchmark strategies against key competitors such as Ricca Design Studios and VisionBuilders.

### For Business Development Tasks
1. Reference proposal templates found in `foodesign-associates-client/business-development/`.
2. Lead with Foodesign's 50-year track record and extensive 4,500+ project portfolio.
3. Highlight WOSB/EDWOSB certifications for government and public sector opportunities.

## Inputs Required

| Field | Required? | Description |
| :--- | :--- | :--- |
| Task type | Yes | Specifies the nature of the task: Content, SEO, Strategy, Business Development, or Knowledge Base Update. |
| Specific deliverable | Yes | Details the exact output required (e.g., "blog post on commercial kitchen design"). |
| Target audience | No | Defaults to architects if not explicitly specified. |
| Target keyword | No | Required for SEO and content-focused tasks. |

## Output Format
Output formats vary based on the task type:
- **Blog posts:** Typically 800–1,200 words, SEO-optimized, with H2/H3 structure and a clear CTA.
- **Social content:** Platform-appropriate length, expertise-led, incorporating relevant hashtags.
- **Proposals:** Structured documents utilizing the official FDA proposal template.
- **Strategy documents:** Markdown reports featuring an executive summary, detailed recommendations, and an action plan.
- **SEO briefs:** Include keyword analysis, search intent, content outline, and internal linking recommendations.

## Source Material
- `foodesign-associates-client/knowledge-base/FDA_Master_Knowledge_Base.md`
- `foodesign-associates-client/strategy/`
- `foodesign-associates-client/content-marketing/`
- `foodesign-associates-client/seo-strategy/`
- `foodesign-associates-client/business-development/`

## Guardrails
- **Brand Integrity:** MUST NOT produce content that contradicts Foodesign's "independent, no equipment sales" positioning.
- **Factual Accuracy:** MUST NOT make claims about project outcomes or client names without verifying against the knowledge base.
- **Approval Process:** MUST NOT publish or share any client materials without explicit approval; all outputs are considered drafts until approved.
