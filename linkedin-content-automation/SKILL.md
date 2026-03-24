---
name: linkedin-content-automation
description: Automate LinkedIn content creation by analyzing Ryan's profile and generating daily draft posts. Use when the user requests LinkedIn content automation, daily post generation, or scheduling LinkedIn content check-ins. This skill scrapes LinkedIn profiles, learns writing style, generates posts using a knowledge base, tracks posting cadence, and delivers daily drafts at 8 AM EST.
license: MIT
---

# LinkedIn Content Automation

Automate LinkedIn content creation for Ryan Cunningham by analyzing his writing style and generating daily draft posts based on his knowledge base.

## Overview

This skill provides a complete workflow for LinkedIn content automation:

1. Analyze Ryan's LinkedIn profile to learn his writing style
2. Load knowledge base from project's `/knowledge/` directory
3. Generate daily LinkedIn post drafts
4. Track posting cadence (minimum 3 posts per week)
5. Deliver daily check-ins at 8:00 AM EST with draft posts

## Configuration

**LinkedIn Profile**: https://www.linkedin.com/in/constructmedia/

**Knowledge Base Location**: `./knowledge/` (relative to project root)

**Posting Schedule**: Daily check-in at 8:00 AM EST

**Minimum Cadence**: 3 posts per week

**Post Specifications**:
- Length: Medium (150-250 words)
- Style: Direct, conversational, strategic, practical
- Structure: Hook → Value → Engagement Question
- Topics: AI automation, brand building, neural nets, marketing for founders, Founders Flywheel
- Always end with an engaging question
- Include 3-5 relevant hashtags
- Occasionally suggest infographic ideas

## Workflow

### Initial Setup (First Time Only)

When the skill is first used, complete these setup steps:

**Step 1: Scrape LinkedIn Profile**

Run the profile scraper to analyze Ryan's writing style:

```bash
python /home/ubuntu/skills/linkedin-content-automation/scripts/scrape_linkedin_profile.py \
  "https://www.linkedin.com/in/constructmedia/" \
  "./linkedin_data/ryan_profile_analysis.json"
```

This script provides instructions for browser automation. Navigate to the profile, extract recent posts (aim for 20-30 posts), and analyze:
- Average post length
- Common topics and themes
- Tone and voice patterns
- Structure patterns (hooks, conclusions)
- Engagement techniques
- Hashtag usage

Save the analysis to `./linkedin_data/ryan_profile_analysis.json`.

**Step 2: Verify Knowledge Base**

Check that the knowledge base exists at `./knowledge/`. If not, ask the user to provide knowledge base files or create placeholder files.

**Step 3: Initialize Post History**

Create the post tracking file:

```bash
mkdir -p ./linkedin_data
echo '{"posts": []}' > ./linkedin_data/post_history.json
```

**Step 4: Schedule Daily Check-in**

Use the schedule tool to set up daily 8:00 AM EST check-ins:

```
Type: cron
Cron: 0 0 8 * * *
Timezone: America/New_York (EST)
Repeat: true
Prompt: "Generate today's LinkedIn post draft using the linkedin-content-automation skill"
```

### Daily Workflow (Automated)

When triggered at 8:00 AM EST or manually invoked:

**Step 1: Check Posting Cadence**

```bash
python /home/ubuntu/skills/linkedin-content-automation/scripts/track_posts.py \
  recommend ./linkedin_data/post_history.json
```

This returns:
- Posts published this week
- Posts needed to meet minimum (3/week)
- Urgency level
- Recommendation message

**Step 2: Select Topic and Post Type**

Based on the cadence recommendation and recent post history:
- Review `references/content_topics.md` for topic ideas
- Rotate through topic areas (don't repeat topics from previous day)
- Vary post types (educational, story-based, tactical, thought leadership)
- Every 5-7 posts, suggest an infographic post

**Step 3: Generate Post Draft**

```bash
python /home/ubuntu/skills/linkedin-content-automation/scripts/generate_linkedin_post.py \
  "./knowledge" \
  "./linkedin_data/ryan_profile_analysis.json" \
  "[optional: specific topic]" \
  "[optional: post_type]"
```

Post types:
- `standard` - Regular text post
- `infographic` - Suggest infographic with post copy
- `story` - Story-based post
- `tactical` - How-to or step-by-step post

The script outputs a JSON object with the generated post content.

**Step 4: Review and Format**

Review the generated post for:
- Matches Ryan's authentic voice
- Provides genuine value
- Ends with an engaging question
- Includes 3-5 relevant hashtags
- Appropriate length (150-250 words)
- No corporate jargon, hyperbole, or em dashes

Use `templates/post_templates.md` as a reference for structure.

**Step 5: Deliver to User**

Send a message to the user with:
- Greeting and date
- Posting cadence status
- Generated post draft (formatted and ready to copy)
- Topic and post type used
- Optional: Infographic suggestion if applicable
- Call to action: "Ready to post? Let me know when it's published so I can track it!"

### Logging Published Posts

When the user confirms a post has been published:

```bash
python /home/ubuntu/skills/linkedin-content-automation/scripts/track_posts.py \
  log ./linkedin_data/post_history.json \
  "[first 100 characters of post content]"
```

This updates the posting cadence tracker.

## Writing Style Guidelines

**Ryan's Voice** (from RPG Brand Voice):
- Direct and conversational
- Anti-BS attitude (call out industry nonsense)
- Sarcastic but respectful
- Empathetic and human
- Educational but not preachy

**Ryan's Narrative**:
- Gen X founder, victim of corporate culling 2023/2024
- Delivers what corporate never does: real results without vendor lock-in
- Focus on small business founders and practical application

**Content Constraints**:
- No corporate jargon or buzzwords
- No hyperbole or flowery language
- No em dashes (use periods or commas)
- No unprovable claims
- Always focus on practical value

**Engagement Strategy**:
- Always end with a question
- Ask about their experience, challenges, or opinions
- Make questions specific and relevant to the post topic
- Encourage comments, not just likes

## Content Topics

Refer to `references/content_topics.md` for:
- Detailed topic breakdowns
- Post angle templates
- Seasonal/timely angles
- Infographic ideas
- Content mix guidelines

Core topics:
1. AI Automation
2. Brand Building
3. Knowledge Building
4. Neural Nets for AI
5. Marketing Power for Small Business Founders
6. The Founders Flywheel (Ryan's framework)

## Post Templates

Refer to `templates/post_templates.md` for:
- Standard post template
- Story-based post template
- Tactical/how-to post template
- Thought leadership post template
- Infographic post template
- Question/engagement post template

## Troubleshooting

**Issue**: Knowledge base directory not found
**Solution**: Ask user to provide knowledge base files or confirm the project structure

**Issue**: Writing style analysis file missing
**Solution**: Re-run the LinkedIn profile scraper (Step 1 of Initial Setup)

**Issue**: Generated posts don't match Ryan's voice
**Solution**: Review more LinkedIn posts to improve the style analysis, or manually adjust the system prompt in `generate_linkedin_post.py`

**Issue**: Posting cadence not tracking correctly
**Solution**: Verify `post_history.json` format and manually add missing posts if needed

## Files and Directories

```
linkedin-content-automation/
├── SKILL.md (this file)
├── scripts/
│   ├── scrape_linkedin_profile.py    - Scrape and analyze LinkedIn profile
│   ├── generate_linkedin_post.py     - Generate post drafts using AI
│   └── track_posts.py                - Track posting cadence
├── references/
│   └── content_topics.md             - Topic ideas and angles
└── templates/
    └── post_templates.md             - Post structure templates
```

**Project Files** (created during use):
```
./linkedin_data/
├── ryan_profile_analysis.json        - Writing style analysis
└── post_history.json                 - Posting cadence tracker
```

## Notes

- The skill uses OpenAI's API (gpt-4.1-mini) for post generation
- Browser automation is required for LinkedIn profile scraping
- Schedule tool is required for daily 8 AM EST check-ins
- Knowledge base should be maintained and updated by the user
- Post drafts are suggestions; user has final editorial control

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
