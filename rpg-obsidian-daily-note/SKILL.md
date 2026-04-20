---
name: rpg-obsidian-daily-note
description: Generates Ryan's daily Obsidian note by pulling context from the day's agent activity, Google Drive logs, and the Portable Brain, then formats it to Ryan's standard template. Use when Ryan asks for a daily summary, an Obsidian update, or an end-of-day report.
---

# RPG Obsidian Daily Note Generator

This skill automates the creation of Ryan's daily Obsidian note. It ensures that all daily summaries map exactly to Ryan's preferred template and capture the critical context from the day's operations.

## How to Use This Skill

When Ryan asks for a daily update, an Obsidian note, or an end-of-day summary, follow these steps:

### 1. Gather Context
Before generating the note, you must gather context about what happened today. Look for:
- **Agent Activity:** What did Trinity, Scarlett, Morpheus, or Ryan's AI do today?
- **Decisions:** What strategic or operational decisions were made?
- **Knowledge:** Were any new frameworks, rules, or IP added to the Portable Brain?
- **Instructions:** Did Ryan give any specific preferences or guardrails to the agents?

*Note: You can use the `ryan-knowledge` skill to search the Portable Brain for recent entries if needed.*

### 2. Map to the Template
You MUST use the exact template provided in `templates/daily_note_template.md`. Do not invent new sections or change the headers.

The template requires the following sections:
- **Top 3 Priorities Today:** (Leave blank for Ryan to fill, unless explicitly known)
- **Wins & Golden Moments:** (Agent achievements, content captured, milestones)
- **Decisions Made:** (Strategic choices, system architecture decisions)
- **New Knowledge or Frameworks:** (Items that should go in or went into the Portable Brain)
- **What I Told an Agent Today:** (Instructions given to Trinity, Seven, etc.)
- **Tomorrow's Focus:** (Leave blank for Ryan to fill, unless explicitly known)
- **Notes & Thinking:** (Leave blank for Ryan to fill)

### 3. Generate the Note
Read the template file:
```bash
cat /home/ubuntu/skills/rpg-obsidian-daily-note/templates/daily_note_template.md
```

Fill in the `{VARIABLES}` with the context you gathered. For sections where you don't have information (like Priorities or Notes), leave a blank bullet point (`- `) so Ryan can fill it in later.

### 4. Deliver the Output
Provide the final formatted Markdown directly to Ryan in a code block or standard message so he can copy and paste it into his local Obsidian vault. Do not save it to a file unless explicitly asked.
