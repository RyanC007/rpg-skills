---
name: scarlett-context-pull
description: Drive-first context and knowledge recording system for Scarlett. Runs at the start of every task to check the RPG Shared Drive context pool, flag pending knowledge updates, and open a dated session log on Drive. Also provides mid-session activity logging, knowledge update writing, and session closing — all directly to Drive. NEVER stores artifacts, knowledge, or context locally. Use at the start of every Scarlett task.
---

# Skill: scarlett-context-pull (v2.0 — Drive-First Protocol)

## PRIME DIRECTIVE

**NEVER store artifacts, knowledge, context logs, or session data locally.**
Everything goes to the Scarlett-AI / RPG Shared Drive (`0AK8dAs_XgfnNUk9PVA`).
The only local footprint allowed is the transient work directory `~/.scarlett_session_work/` used for file staging before upload — files are deleted immediately after each Drive write.

---

## When to Use

Run the startup script at the start of **every** Scarlett task, before doing anything else. The other scripts are called throughout and at the end of each task.

---

## Drive Architecture

| Folder | Drive ID | Purpose |
|:---|:---|:---|
| Scarlett-AI (root) | `0AK8dAs_XgfnNUk9PVA` | Single source of truth |
| System-Wide-Context-Pool | `1S0tTXrNmhAusCSs7ta0s7obRa2mTIeXw` | All Scarlett knowledge |
| `system-knowledge` | `1xYW5dA14c_jPIZ3XXOcc7qz0fddjt61h` | Live system knowledge (Type 1) |
| `system-knowledge/scarlett-context-logs` | `1qI_vetE2cKzy8jcY_ivVefZezcrsGZeK` | Dated session logs |
| `knowledge-pending` | `1ZxlDrK8sxbvtuLp3e4jIgSTvWXYB1XAI` | Entity knowledge awaiting Ryan review (Type 2) |

---

## Four Scripts — One Pipeline

### 1. Startup Check (run at task start — MANDATORY)
```bash
bash /home/ubuntu/skills/scarlett-context-pull/scripts/scarlett_startup_check.sh
```
**What it does:**
- Reads `system-knowledge` from Drive (count + latest file)
- Checks `knowledge-pending` for unreviewed updates — flags them if found
- Reads the most recent session log from `scarlett-context-logs` on Drive
- Creates a new dated session log on Drive for this session
- Stores session file ID in `~/.scarlett_session_work/` for use by other scripts

**No Thor. No Trinity. RPG Shared Drive only.**

---

### 2. Activity Logger (call mid-task as needed)
```bash
bash /home/ubuntu/skills/scarlett-context-pull/scripts/scarlett_log_activity.sh "Description of what happened"
```
**What it does:** Appends a timestamped entry to the current session log on Drive. Use to record key decisions, discoveries, or task milestones.

---

### 3. Knowledge Update (call when new knowledge surfaces)
```bash
bash /home/ubuntu/skills/scarlett-context-pull/scripts/scarlett_knowledge_update.sh \
  --type 1 \
  --title "short-slug-title" \
  --content "Full markdown content"
```
- `--type 1` = System Knowledge → writes live to `system-knowledge`
- `--type 2` = Entity Knowledge → stages in `knowledge-pending` for Ryan review

**When to use:** Ryan corrects a workflow, states a preference, says "remember this", or new facts about Ryan/Marcela/RPG surface. Also use for any new pipeline, routing rule, or system design.

**After writing Type 2:** Always flag Ryan with:
> "I captured a knowledge update for [Ryan / Marcela / RPG] and staged it for your review in `knowledge-pending`. Say 'review pending knowledge' when ready."

---

### 4. Session Closer (run before delivering results — MANDATORY)
```bash
bash /home/ubuntu/skills/scarlett-context-pull/scripts/scarlett_session_close.sh "Summary of what was accomplished"
```
**What it does:** Writes a closing summary to the Drive session log, then clears `~/.scarlett_session_work/`. No local data survives session close.

---

## Knowledge Types Reference

| Type | What It Is | Destination | Review Required |
|:---|:---|:---|:---|
| **Type 1 — System** | Workflow rules, pipeline changes, routing rules, Ryan's stated preferences | `system-knowledge` (live) | No |
| **Type 2 — Entity** | New facts about Ryan, Marcela, or RPG — skills, strategy, wins, positioning | `knowledge-pending` | Yes — Ryan must approve |

---

## Mandatory Startup Output Check

After running the startup script, if `knowledge-pending` has files, surface them immediately:

> "Ryan, there are [N] knowledge updates staged for your review in `knowledge-pending` from [dates]. Say 'review pending knowledge' when ready."

Do not proceed silently past pending knowledge.

---

## What Is Forbidden

- Writing `.md`, `.json`, `.txt`, or any knowledge/context file to `/home/ubuntu/` or any local path as a final destination
- Using `rclone` to pull Thor or Trinity context (both decommissioned or out of scope)
- Storing session logs, knowledge updates, or artifacts anywhere except the Scarlett-AI Drive
- Leaving any files in `~/.scarlett_session_work/` after session close

---

## Protocol Version
Scarlett Drive-First Protocol v2.0 — Updated April 2026
Supersedes: scarlett-context-pull v4.1 (February 2026)
