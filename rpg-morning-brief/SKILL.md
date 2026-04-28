---
name: rpg-morning-brief
description: >-
  Runs the daily Scarlett morning brief, a 15-minute system health check with Ryan (Mon-Fri).
  Two modes - PREP runs nightly and builds the brief from Drive context, ready by 8 AM EST.
  DELIVER is triggered by Ryan saying "good morning scarlett", "run morning brief", or "let's do the brief".
  Reads the brief aloud using Shimmer TTS and walks through blockers one at a time.
  Replaces all scheduled EOD reports. This is the only daily reporting process for Scarlett.
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

Run by the Manus scheduler every weekday morning. Builds the brief silently and saves it to Drive. Ryan never sees this -- it just happens in the background.

```bash
python3 /home/ubuntu/skills/rpg-morning-brief/scripts/prep_brief.py
```

The script:
1. Runs the startup check to pull system-knowledge and knowledge-pending from Drive
2. Reads the 5 most recent session logs from `scarlett-context-logs` on Drive
3. Builds a dated brief markdown file
4. Saves it locally to `/home/ubuntu/.scarlett_session_work/morning_brief_YYYY-MM-DD.md`
5. Uploads it to `System-Wide-Context-Pool/system-knowledge/scarlett-context-logs` on Drive and deletes the local copy

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
Run the startup check first, then read the most recent brief from `System-Wide-Context-Pool/system-knowledge/scarlett-context-logs` on Drive using `gws drive files list`.

**2. Speak the opening**
```bash
python3 /home/ubuntu/skills/rpg-morning-brief/scripts/speak.py "Good morning Ryan. I've pulled the latest context. I have [N] items for you today. Ready when you are."
```

**3. Go through the blocker queue -- one item at a time**

Build the queue from the brief context: open blockers, overdue items, pending follow-ups flagged for the morning brief, and any items flagged in `knowledge-pending` on Drive.

For each item, speak it first, then display it:
```bash
python3 /home/ubuntu/skills/rpg-morning-brief/scripts/speak.py "Item [N]: [description]. [Question]."
```

Wait for Ryan's response. Acknowledge it, log it, move to the next item.

**4. Log Ryan's updates**
Append each update to the brief file as it happens under `## Session Log`.

**5. Upload the completed brief to Drive**
```bash
gws drive files create \
  --params '{"supportsAllDrives":true}' \
  --json '{"name":"morning_brief_YYYY-MM-DD.md","parents":["1qI_vetE2cKzy8jcY_ivVefZezcrsGZeK"],"mimeType":"text/markdown"}' \
  --upload /home/ubuntu/.scarlett_session_work/morning_brief_YYYY-MM-DD.md \
  --upload-content-type "text/markdown"
```

**6. Speak the close**
```bash
python3 /home/ubuntu/skills/rpg-morning-brief/scripts/speak.py "That's everything for today. I've logged your updates. Have a good one Ryan."
```

---

## Scarlett Voice

- **Model:** `tts-1`
- **Voice:** `shimmer`
- Every Scarlett response during the brief MUST be spoken aloud before displaying text.

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
