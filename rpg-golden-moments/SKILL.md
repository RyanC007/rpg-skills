---
name: rpg-golden-moments
description: Captures, synthesizes, and converts daily wins, breakthroughs, and insights into content for LinkedIn, Substack, and X. Use when logging a golden moment, running the daily synthesis, or generating content from captured moments. Assigned to Scarlett, Trinity, Thor, and Ryan AI. Already scheduled - do not modify the schedule without Ryan approval.
---

# RPG Golden Moments Skill

OUTPUT_TIER: 1 (Public Outbound) for published content
OUTPUT_TIER: 3 (Internal) for raw moment logs and synthesis drafts

## Guardrails (Tier 1 for published content)
- Never mention clients by name in published content
- No internal repo URLs, file paths, or agent infrastructure details in published content
- No unprovable claims or hyperbole
- No em dashes

## Purpose
Capture daily wins, breakthroughs, and insights before they get lost. Synthesize them into content for LinkedIn, Substack, and X. This is the system that turns the work into the story.

## Agent Assignment
- Scarlett: Yes
- Trinity: Yes
- Thor: Yes
- Ryan AI: Yes
- Morpheus: No

## Schedule
Already configured. Do not modify without Ryan approval.

## Workflow

### Mode 1: Log a Moment
When a significant win, insight, or breakthrough happens, log it immediately.
Format: date, type (breakthrough/insight/tactical/win), description, context.
Append to raw-moments.csv in the golden-moments folder.

Moment types:
- breakthrough: A significant capability unlocked or problem solved
- insight: A realization that changes how something is done
- tactical: A specific technique or approach that worked well
- win: A measurable result or client/business outcome

### Mode 2: Daily Synthesis
Run at the scheduled time. Pull all moments logged in the last 24 hours and synthesize into:
1. A daily log entry (internal, Tier 3)
2. Content drafts for LinkedIn, Substack, and X (Tier 1)

Run: python3 daily_synthesis.py (from the golden-moments scripts directory)

### Mode 3: Generate Content from Moments

LinkedIn Post:
- Hook in first line (the moment or result, not the process)
- 3-5 short paragraphs
- Anonymize any client references (Tier 1 guardrail)
- CTA at end
- 3-5 relevant hashtags

Substack Article:
- Use the weekly build log template
- Synthesize the week moments into a narrative
- Educational angle: what can the reader learn from this?
- 500-800 words

X Post:
- Single insight, under 280 characters
- Punchy, direct, no fluff

### Mode 4: Save and Notify
Save all generated content drafts to the content-drafts folder organized by platform.
Notify Ryan or Marcela that drafts are ready for review.

## Templates
- templates/daily-summary-template.md - Internal daily log format
- templates/linkedin-post-template.md - LinkedIn post structure
- templates/substack-article-template.md - Substack article structure

## Voice Reminders for Published Content
- First person, personal and direct
- Specific details and numbers (anonymized where needed)
- No corporate jargon
- No em dashes
- The story is the work, not the tool

## Mandatory Final Step: Content Sanitization
Before saving any generated content drafts to a file or publishing them, you MUST run the universal content sanitizer CLI tool on the output file to ensure all RPG slop words are removed.
```bash
python3 /home/ubuntu/knowledge_bases/rpg-branded-agents/skills/_guardrails/sanitize_output.py --input /path/to/your/output.md
```
Do not skip this step.
