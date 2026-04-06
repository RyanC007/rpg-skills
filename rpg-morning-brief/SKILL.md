---
name: rpg-morning-brief
description: >-
  Runs the daily Scarlett morning brief, a 15-minute system health check with Ryan (Mon-Fri).
  Two modes - PREP runs nightly and builds the brief from Drive context, ready by 8 AM EST.
  DELIVER is triggered by Ryan saying "good morning scarlett", "run morning brief", or "let's do the brief".
  Walks through blockers one at a time as text. Replaces all scheduled EOD reports.
  This is the only daily reporting process for Scarlett.
---

# RPG Morning Brief Skill

OUTPUT_TIER: 3 (Internal)

## Two Modes

| Mode | When | Trigger |
| :--- | :--- | :--- |
| **PREP** | Nightly, Mon-Fri, completes by 8 AM EST | Scheduled automatically |
| **DELIVER** | Morning, when Ryan is ready | Ryan says a trigger phrase |

---

## PREP Mode

Runs by the Manus scheduler every weekday morning. Builds the brief silently and saves it to Drive. Ryan never sees this -- it just happens in the background.

```bash
python3 /home/ubuntu/skills/rpg-morning-brief/scripts/prep_brief.py
```

The script:
1. Pulls the last 48 hours of context from `Scarlett/Daily_Updates/Context_Pool`
2. Reads the 5 most recent context files
3. Builds a dated brief markdown file
4. Saves it locally to `/home/ubuntu/scarlett_agent_context/briefs/morning_brief_YYYY-MM-DD.md`
5. Uploads it back to the Drive context pool

**Do not deliver or mention the brief until Ryan triggers it.**

---

## DELIVER Mode

Triggered when Ryan says any of:
- "good morning scarlett"
- "run morning brief"
- "let's do the brief"
- "morning brief"
- "scarlett brief"

### Delivery Steps

**1. Load the brief**
Read the most recent file from `/home/ubuntu/scarlett_agent_context/briefs/` or pull it fresh from Drive if not cached.

**2. Open the session**
Greet Ryan and state how many items are in the queue:
> "Good morning Ryan. I've pulled the latest context. I have [N] items for you today. Ready when you are."

**3. Go through the blocker queue -- one item at a time**

Build the queue from the brief context: open blockers, overdue items, pending follow-ups flagged for the morning brief, new Trinity/Thor flags.

For each item, present it as text and wait for Ryan's response before moving on:
> "Item [N]: [description]. [Question]."

**4. Log Ryan's updates**
Append each update to the brief file as it happens under `## Session Log`.

**5. Upload the completed brief to Drive**
```bash
rclone copy /home/ubuntu/scarlett_agent_context/briefs/morning_brief_YYYY-MM-DD.md \
  "manus_google_drive:Scarlett/Daily_Updates/Context_Pool" \
  --drive-root-folder-id 0AK8dAs_XgfnNUk9PVA \
  --config /home/ubuntu/.gdrive-rclone.ini
```

**6. Close the brief**
> "That's everything for today. I've logged your updates. Have a good one Ryan."

---

## Rules

- Do NOT deliver the brief until Ryan triggers it
- Do NOT dump all blockers at once -- one at a time only
- Do NOT generate a full written report unless Ryan explicitly asks
- Do NOT run any other scheduled processes -- this IS the daily reporting
- Brief prep runs Mon-Fri only. No weekends.

---

## Drive Guardrail

All rclone commands MUST include:
- `--drive-root-folder-id 0AK8dAs_XgfnNUk9PVA`
- `--config /home/ubuntu/.gdrive-rclone.ini`

See `scarlett-drive-guardrail` skill for full rules.
