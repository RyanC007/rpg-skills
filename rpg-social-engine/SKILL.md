---
name: rpg-social-engine
description: Operate the RPG Social Engine pipeline for Ryan and Marcela. Use this skill when asked to generate content, check pipeline status, force-post a day, or troubleshoot the Social Engine. CRITICAL ROUTING: Use this skill (not linkedin-series-creator or linkedin-content-automation) when Ryan asks about the "Blotato pipeline" or content that Scarlett dropped in the shared drive (e.g., Golden Moments). This skill covers the full pipeline from Google Drive content ingestion to Blotato scheduling across 6 platforms.
---

# RPG Social Engine Skill

## What This Skill Does

This skill gives Trinity the operational knowledge to run the Social Engine pipeline end-to-end for Ryan (`--client ryan`) and Marcela (`--client marcela`). The engine lives at:

```
/home/ubuntu/ai-manager-stack/tools/social-engine/
```

### Canonical Generation Script

The **sole** content generation engine is:

```
ai-manager-stack/tools/social-engine/content_pipeline/pipeline_runner.py
```

Do NOT use `generate_linkedin_post.py` from `rpg-skills/linkedin-content-automation/` or `rpg-skills/linkedin-series-creator/`. Those scripts are **deprecated** as of 2026-04-08 and retained for reference only.

---

## Agent Boundaries

| Agent | Role | Boundary |
|---|---|---|
| **Scarlett** | Content generation ONLY | Generates content via `pipeline_runner.py`, writes drafts DIRECTLY to Trinity's Drive pickup folder. Never publishes. |
| **Trinity** | Publishing ONLY | Picks up content from Drive, reviews, and publishes to Blotato. Never generates content. |

This is Ryan's personal pipeline. Marcela's pipeline will be separate and run by Scarlett later.

---

## Weekly Workflow

The pipeline runs on a two-step weekly cycle. No polling, no approval email. On-demand only.

| Time | Who | Action |
|---|---|---|
| Sunday 18:00 UTC | Scarlett | Generates 7 days of content via `pipeline_runner.py` and writes DIRECTLY to Trinity's Drive pickup folder |
| On-demand (when Ryan instructs) | Trinity | Ryan tells Trinity to pick up content and push to Blotato |

**Gmail polling and approval emails are permanently removed.** The weekly_approval.py script has been deleted. The system is on-demand only -- Ryan tells Trinity when to publish.

### On-Demand Handoff (Trinity's job)

When Ryan says anything like "run the pipeline", "push this week's content", "pick up the Golden Moments", or "push to Blotato", run these two commands in order:

**Step 1: Run the Golden Moments handoff (converts Drive content to Social Engine format)**
```bash
cd /home/ubuntu/ai-manager-stack/tools/social-engine
python3 golden_moments_handoff.py --client ryan
```

**Step 2: Publish each day to Blotato**
```bash
cd /home/ubuntu/ai-manager-stack/tools/social-engine
python3 cloud_daily_run.py --client ryan --force-post --day 1
```
Repeat for each day (--day 2, --day 3, etc.) or confirm with Ryan how many days to schedule.

---

## Core Commands Trinity Uses

### Check Pipeline Status
```bash
cd /home/ubuntu/ai-manager-stack/tools/social-engine
python3 cloud_daily_run.py --client ryan --status
```
Shows: current week, pipeline generation time, scheduled days.

### Manually Trigger Content Generation
Only needed if Sunday generation failed or Ryan requests a regeneration.
```bash
cd /home/ubuntu/ai-manager-stack/tools/social-engine
python3 content_pipeline/pipeline_runner.py --client ryan
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

## Content Storage

### Scarlett writes DIRECTLY to Trinity's Drive

**Trinity-AI Drive ID:** `0AMzg3SxgIv0-Uk9PVA`
**Pickup Folder:** `07_Personal/Ryan_Content_Drops/`
**Folder ID:** `1K7xeoQZBKr46j1zcB7DQjStdqBTiSqFP`

Each week's content goes into a subfolder named `{year}-W{week_number}`, e.g. `2026-W15`, with subfolders for `LinkedIn/` and `Substack/`.

There is no intermediate storage on Scarlett's drive. Scarlett writes directly to Trinity's pickup folder to eliminate double storage.

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
- No em dashes anywhere
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

## Blotato API Integration

The publishing engine uses the Blotato REST API (`https://backend.blotato.com/v2`):
- **Auth:** `blotato-api-key` header
- **Endpoints:** POST `/posts` for scheduling, GET `/posts/scheduled` for dedup checks
- **Visual generation:** POST `/videos/from-templates` for images/videos
- **Asset polling:** GET `/videos/creations/{id}` with `wait_for_asset()` utility
- **Dedup:** Per-platform dedup checks prevent double-posting on the same calendar day
- **Retry:** Automatic retry with backoff on 429/5xx errors

---

## Troubleshooting

| Symptom | Action |
|---|---|
| Pipeline failed on Sunday | Run `pipeline_runner.py --client ryan` manually |
| Blotato API error | Check `BLOTATO_API_KEY` in `.env` file or Drive secrets |
| Google Drive error | Re-run `setup_oauth.py --client ryan` to refresh OAuth token |
| Visual generation timeout | Engine skips and publishes text-only. No action needed. |
| Marcela pipeline not running | Fill in all `PLACEHOLDER_` values in `clients/marcela.json` first |

If an error cannot be resolved after 3 retries, halt the engine and include the full error in the 8:00 AM EST Executive Briefing to Ryan.

---

## Reference Files

For deeper technical detail, read these files as needed:
- `references/content_pillars.md` -- Ryan's 7 topic pillars and weekly rotation schedule
- Full operations manual: `tools/social-engine/docs/TRINITY_OPERATIONS_MANUAL.md`
