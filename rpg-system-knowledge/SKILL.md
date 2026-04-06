---
name: rpg-system-knowledge
description: Mandatory system-wide knowledge storage and retrieval directive. Use this skill whenever Ryan provides new facts, preferences, corrections, or workflows that need to be remembered permanently. Also use when an agent surfaces new knowledge about RPG, Ryan, or Marcela that should eventually update the core knowledge bases after human review. Ensures no knowledge is trapped in a local sandbox and all agents share the same brain.
---

# RPG System Knowledge Directive

**CRITICAL DIRECTIVE:** No knowledge should ever be stored locally in a sandbox. All new knowledge MUST be stored in Google Drive and committed to GitHub. Nothing stays local.

---

## Storage Architecture

**CANONICAL SOURCE: GitHub is the single source of truth for all entity knowledge. Drive mirrors are read-only copies for agent runtime access. All updates go to GitHub first, then sync to Drive.**

### System Knowledge (workflow rules, preferences, routing)

| Layer | Location | Purpose |
|---|---|---|
| Live read source | Google Drive `System-Wide-Context-Pool/system-knowledge` (ID: `1xYW5dA14c_jPIZ3XXOcc7qz0fddjt61h`) | Agents pull from here at runtime |
| Versioned backup | GitHub `RyanC007/rpg-system-knowledge` (private) | Full history, diffs, and rollback |
| Staging (pending review) | Google Drive `System-Wide-Context-Pool/knowledge-pending` (ID: `1ZxlDrK8sxbvtuLp3e4jIgSTvWXYB1XAI`) | New RPG/Ryan/Marcela knowledge awaiting Ryan's approval before committing to core KBs |

### Entity Knowledge (Ryan, Marcela, RPG)

| Entity | Canonical GitHub Repo | Drive Mirror Folder ID |
|---|---|---|
| Ryan | `RyanC007/ryan-knowledge-base` | `1Py0oT1LbYw4nA8CTVZN48OhDXekB4Sui` |
| Marcela | `RyanC007/marcela-knowledge-base` | `1K7BWFFTOWHe9ezYj4TjwTTzSS5nazT8Y` |
| RPG | `RyanC007/rpg-master-knowledge-base` | `1yhOgADaYIStRmdkt8uRxCkvt1ta6w37m` |

**Archived (do not use):** `RyanC007/marcela-knowledge-base-rpg` — duplicate of `marcela-knowledge-base`, archived on 2026-03-25.

All Drive mirror folders live inside `System-Wide-Context-Pool` (ID: `1S0tTXrNmhAusCSs7ta0s7obRa2mTIeXw`).

---

## Two Types of Knowledge

### Type 1: System Knowledge (store immediately, no review needed)
Applies to: workflow rules, pipeline changes, routing rules, Ryan's stated preferences, agent boundaries.

These go directly to `system-knowledge` in Drive and to the `rpg-system-knowledge` GitHub repo. No human review required.

### Type 2: Entity Knowledge (stage for review first)
Applies to: new facts about **Ryan**, **Marcela**, or **RPG** as a business (e.g., new skills, new strategic direction, new brand positioning, personal updates, business wins).

These go to `knowledge-pending` in Drive first. Ryan reviews and approves before the agent commits them to the core knowledge base repos.

---

## When to Use This Skill

You MUST use this skill when:
1. Ryan corrects a workflow or provides a new preference.
2. You design a new pipeline or system architecture that future agents will need.
3. Ryan explicitly says "remember this", "store this", or "add this to your knowledge".
4. During any task, you learn something new about Ryan, Marcela, or RPG that is not already in the knowledge bases.
5. A conversation reveals a new skill, tool, strategy, win, or positioning update for Ryan or Marcela.

---

## How to Store Type 1 Knowledge (System Knowledge)

**Step 1: Create the knowledge file**
Name it `[topic_slug]_knowledge.md`. Use this format:
```markdown
# [Topic Name]
**Date Added:** YYYY-MM-DD
**Applies To:** [Trinity / Scarlett / All Agents]

## Core Directive
[A concise summary of the rule, preference, or fact]

## Details
[Any technical details, folder IDs, or specific commands required]
```

**Step 2: Upload to Drive (live read source)**
```bash
gws drive +upload /path/to/file.md --parent 1xYW5dA14c_jPIZ3XXOcc7qz0fddjt61h
```

**Step 3: Commit to GitHub (versioned backup)**
```bash
gh repo clone RyanC007/rpg-system-knowledge /tmp/rpg-system-knowledge
cp /path/to/file.md /tmp/rpg-system-knowledge/[subfolder]/
cd /tmp/rpg-system-knowledge
git add . && git commit -m "knowledge: [brief description]" && git push
```

Subfolders: `pipelines/` `routing/` `preferences/` `agents/`

---

## How to Store Type 2 Knowledge (Entity Knowledge - Requires Human Review)

**Step 1: Create the staging file**
Name it `[date]_[entity]_[topic]_pending.md` (e.g., `2026-03-25_ryan_new_skill_pending.md`). Use this format:
```markdown
# Knowledge Update Pending Review
**Date Surfaced:** YYYY-MM-DD
**Surfaced By:** [Trinity / Scarlett]
**Entity:** [Ryan / Marcela / RPG]
**Target Repo:** [ryan-knowledge-base / marcela-knowledge-base / rpg-master-knowledge-base]
**Target File:** [e.g., identity/ryan-identity.md or voice/ryan-voice.md]

## What Was Learned
[Clear, concise description of the new knowledge]

## Suggested Update
[The exact text or section that should be added or changed in the target file]

## Source
[Brief note on where this came from - e.g., "Ryan mentioned during task on 2026-03-25"]
```

**Step 2: Upload to the knowledge-pending staging folder**
```bash
gws drive +upload /path/to/pending_file.md --parent 1ZxlDrK8sxbvtuLp3e4jIgSTvWXYB1XAI
```

**Step 3: Flag Ryan for review**
At the end of the task, include a note in your response:

> "I also captured a knowledge update for [Ryan/Marcela/RPG] and staged it for your review in the `knowledge-pending` folder. Say 'review pending knowledge' when you are ready and I will walk you through it."

**Step 4: After Ryan approves**
Once Ryan confirms, commit the update to the correct repo:

| Entity | Repo | Key Files |
|---|---|---|
| Ryan | `RyanC007/ryan-knowledge-base` | `identity/`, `voice/`, `preferences/`, `business/` |
| Marcela | `RyanC007/marcela-knowledge-base` | `identity/`, `voice/`, `expertise/` |
| RPG | `RyanC007/rpg-master-knowledge-base` | `brand/`, `ops/`, `team/`, `clients/` |

```bash
gh repo clone RyanC007/[target-repo] /tmp/[target-repo]
# Edit the relevant file
cd /tmp/[target-repo]
git add . && git commit -m "knowledge: [brief description] (approved by Ryan [date])" && git push
```

Then delete the staging file from Drive:
```bash
gws drive files delete [PENDING_FILE_ID]
```

---

## How to Retrieve Knowledge

List all current system knowledge:
```bash
gws drive files list --params '{"q": "\"1xYW5dA14c_jPIZ3XXOcc7qz0fddjt61h\" in parents", "includeItemsFromAllDrives": true, "supportsAllDrives": true}'
```

List all pending knowledge awaiting review:
```bash
gws drive files list --params '{"q": "\"1ZxlDrK8sxbvtuLp3e4jIgSTvWXYB1XAI\" in parents", "includeItemsFromAllDrives": true, "supportsAllDrives": true}'
```

Read a specific file:
```bash
gws drive files get [FILE_ID] --alt media
```
