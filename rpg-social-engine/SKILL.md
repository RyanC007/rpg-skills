---
name: rpg-social-engine
description: Operate the RPG Social Engine pipeline for Ryan and Marcela. Use this skill when asked to generate content, check pipeline status, run the weekly approval flow, force-post a day, or troubleshoot the Social Engine. This skill covers the full pipeline from Google Drive content ingestion to Blotato scheduling across 6 platforms.
---

# RPG Social Engine Skill

## What This Skill Does

This skill gives Trinity the operational knowledge to run the Social Engine pipeline end-to-end for Ryan (`--client ryan`) and Marcela (`--client marcela`). The engine lives at:

```
/home/ubuntu/ai-manager-stack/tools/social-engine/
```

---

## Weekly Automated Flow

The engine runs on a fully automated weekly cycle. Trinity does not need to trigger this manually unless something fails.

| Time | Action |
|---|---|
| Sunday 18:00 UTC | Generate 7 days of content via Gemini + send preview email to client |
| Sunday 18:05 UTC | Weekly approval email sent to client |
| Hourly (all week) | Poll Gmail for `APPROVE ALL` reply |
| On approval | Bulk-schedule all approved days into Blotato at 9:00 AM EST per day |

The single command that handles all of this is:

```bash
cd /home/ubuntu/ai-manager-stack/tools/social-engine
python3 cloud_daily_run.py --client ryan --run
```

Run this hourly via the schedule tool. The script is time-aware: it generates on Sunday at 18:xx UTC and polls Gmail at all other times.

---

## Core Commands Trinity Uses

### Check Pipeline Status
```bash
cd /home/ubuntu/ai-manager-stack/tools/social-engine
python3 cloud_daily_run.py --client ryan --status
```
Shows: current week, pipeline generation time, approval status, scheduled days.

### Manually Trigger Content Generation
Only needed if Sunday generation failed or Ryan requests a regeneration.
```bash
cd /home/ubuntu/ai-manager-stack/tools/social-engine
python3 content_pipeline/pipeline_runner.py --client ryan
```

### Poll for Approval Reply
Only needed outside the hourly schedule if Ryan says he replied.
```bash
cd /home/ubuntu/ai-manager-stack/tools/social-engine
python3 weekly_approval.py --client ryan --poll
```

### Emergency Force Post (Bypass Schedule)
Use only when Ryan explicitly requests an immediate post.
```bash
cd /home/ubuntu/ai-manager-stack/tools/social-engine
python3 cloud_daily_run.py --client ryan --force-post --day 1
```

### Dry Run Preview (No Publishing)
Use to preview what would be published without sending anything to Blotato.
```bash
cd /home/ubuntu/ai-manager-stack/tools/social-engine
python3 main.py --client ryan --week "Week-1" --dry-run
```

---

## Approval Reply Formats

When polling Gmail, the engine looks for these exact phrases in the client's reply to the `[Ryan Social Engine]` subject thread:

- `APPROVE ALL` — Schedule all 7 days
- `APPROVE ALL SKIP 3 5` — Schedule all days except Day 3 and Day 5
- `SKIP ALL` — Discard the week entirely

---

## Client Configurations

| Client | Config File | Email | Blotato Key Env Var |
|---|---|---|---|
| Ryan | `clients/ryan.json` | rc@logoclothz.com | `BLOTATO_API_KEY` |
| Marcela | `clients/marcela.json` | PLACEHOLDER (needs filling) | `MARCELA_BLOTATO_API_KEY` |

**Marcela's pipeline is not yet active.** Her `clients/marcela.json` contains `PLACEHOLDER_` values that must be replaced with real Blotato account IDs and Google Drive folder IDs before her pipeline can run.

---

## Content File Format

If Trinity is ever asked to write or edit a content file directly, it MUST follow this exact format. Files go into the client's Google Drive content folder.

```markdown
---
type: post
day: 1
topic: [Full topic sentence]
client: ryan
platforms: linkedin, x, instagram, youtube_shorts, tiktok, facebook
hashtags: AI, AIAgents, BusinessAutomation, AIForBusiness, Entrepreneur
---

## Hook
[1-3 lines. Bold statement or pattern interrupt. No em dashes.]

## Body
[150-300 words. Short paragraphs. No em dashes. No generic CTAs.]

## Engagement
[Ends with a question mark. Always.]
```

For `type: article`, also include:
```markdown
## YouTube Short Script

HOOK:
[One punchy line]

INSIGHT:
[2-3 sentences of value]

ENGAGEMENT:
[Ends with a question mark]
```

**Non-negotiable rules:**
- No em dashes anywhere (`—`)
- `## Engagement` MUST end with `?`
- No "follow me", "click here", "link in bio" (except Instagram/TikTok where "link in bio" is allowed)
- No unprovable claims ("the only", "unprecedented", "game-changing")

---

## Visual Assets (Auto-Generated)

Trinity does not need to manage visual generation. The engine handles this automatically during publishing:

- **LinkedIn:** Rotates through Whiteboard, Newspaper, Chalkboard, Billboard, Classified Document, Cyberpunk templates. The post hook is injected as the image headline.
- **Facebook:** Rotates through Billboard, TV Wall, Classroom Chalkboard, Open Book, Cinema Screen, Constellation Night Sky.
- **Instagram:** Extracts 3-5 short sentences from the body to create a multi-slide quote card.
- **TikTok + YouTube Shorts:** Generates one shared AI avatar video using the content file's YouTube Short Script. Voice: Brian (Ryan), Sarah (Marcela).

---

## Troubleshooting

| Symptom | Action |
|---|---|
| Pipeline failed on Sunday | Run `pipeline_runner.py --client ryan` manually |
| No approval reply detected | Run `weekly_approval.py --client ryan --poll` manually |
| Blotato API error | Check `BLOTATO_API_KEY` in `.env` file |
| Google Drive error | Re-run `setup_oauth.py --client ryan` to refresh OAuth token |
| Visual generation timeout | Engine skips and publishes text-only. No action needed. |
| Marcela pipeline not running | Fill in all `PLACEHOLDER_` values in `clients/marcela.json` first |

If an error cannot be resolved after 3 retries, halt the engine and include the full error in the 8:00 AM EST Executive Briefing to Ryan.

---

## Reference Files

For deeper technical detail, read these files as needed:
- `references/content_pillars.md` — Ryan's 7 topic pillars and weekly rotation schedule
- Full operations manual: `tools/social-engine/docs/TRINITY_OPERATIONS_MANUAL.md`
