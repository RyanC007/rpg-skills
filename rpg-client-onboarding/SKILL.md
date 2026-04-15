---
name: rpg-client-onboarding
description: "Full RPG client onboarding workflow — creates the Client Mission Control Portal, Master Client Profile (MCP), and Agent Briefing for a new client. Use when Marcela says 'onboard [client name]' or 'set up the portal for [client]'. Requires client name, website URL, and their RPG Shared Drive folder link. Outputs a live password-protected portal on Manus, MCP in Drive, and Agent Briefing ready for the Client AI project instructions."
---

# RPG Client Onboarding

## Overview

This skill executes the full RPG client onboarding sequence. It transforms a client name + URL + Drive folder into a live Mission Control Portal, a Master Client Profile, and a Client Agent Briefing — all synced to GitHub (`marcela-egs/rpg-client-portal-template`) and the RPG Shared Drive.

**Trigger:** "Scarlett, onboard [client name]" or "set up the portal for [client]"

**Required inputs:**
- Client name
- Client website URL (or "none" if no site exists)
- Client Drive folder link or ID (Marcela creates this before triggering)

**Outputs:**
- Live password-protected portal at a Manus URL
- `[CLIENT]_Master_Client_Profile.md` in Drive + GitHub
- `[CLIENT]_Agent_Briefing.md` in Drive + GitHub (attach for Ryan to paste into Client AI)
- Client JSON data file committed to `marcela-egs/rpg-client-portal-template/clients/[slug]/`

---

## Pre-flight Check

Confirm Ryan has already created the Client AI project in Manus. If not, flag to Ryan before proceeding — the Agent Briefing cannot be finalized without the project existing.

---

## Step 1 — Ingest Client Data

### 1a. Read the Drive Folder

List all files in the client's Drive folder. Read every document present — proposal, invoice, brand guide, discovery notes, social strategy, website playbook. Extract: business name, services purchased, brand colors/fonts, ICP descriptions, 90-day goals, and all known contact email addresses.

### 1b. Crawl the Website

Use `ai-site-reporter` and `rpg-seo-audit` to extract: platform/CMS, hosting provider, SSL status, marketing tags (GA4, GSC, Meta Pixel), social links, and ICP signals from existing copy.

If no website exists, mark all tech stack fields as "Not applicable — new build."

---

## Step 2 — Build the Master Client Profile (MCP)

Create `/home/ubuntu/[slug]/[CLIENT]_Master_Client_Profile.md` using `references/mcp_template.md`.

Mark auto-populated fields as `[AUTO]` and fields needing kickoff confirmation as `[PENDING — confirm at kickoff]`.

Upload to Drive (`00_Knowledge Base` folder) and commit to GitHub under `clients/[slug]/`.

---

## Step 3 — Create the Client Uploads Folder

Create `06_Client Uploads` subfolder inside the client's Drive root folder. Record the folder ID. This is where the client drops assets — it must be empty by end of every week.

---

## Step 4 — Generate the Portal

### 4a. Create the Client JSON

Create `client/src/data/[slug].json` using `references/client_data_template.json`. Populate from the MCP.

Key fields:
- `client.password` → generate as `[slug][year]` (e.g., `tutu2026`)
- `client.driveUrl` → link to their shared Drive folder
- `client.uploadsFolder` → link to `06_Client Uploads` subfolder
- `client.authorizedEmails` → all known contact emails
- `phase3.type` → `new_build`, `updates`, or `none` (see Phase 3 Branch Logic below)

### 4b. Initialize the Webdev Project

Use `webdev_init_project` with `project_name: "[slug]-client-portal"`. Copy the master portal template from `marcela-egs/rpg-client-portal-template`. Update `App.tsx` to import the new client JSON. Build and verify zero TypeScript errors. Save checkpoint.

---

## Step 5 — Write the Agent Briefing

Create `/home/ubuntu/[slug]/[CLIENT]_Agent_Briefing.md` using `references/agent_briefing_template.md`.

Populate with: portal URL + password, MCP path in Drive, client JSON path in GitHub, authorized email list, full Drive folder structure with folder IDs, and escalation path.

Upload to Drive and commit to GitHub.

---

## Step 6 — Final GitHub Commit

```bash
cd /home/ubuntu/rpg-client-portal-template
git add clients/[slug]/
git commit -m "[CLIENT]: Complete onboarding — MCP, Agent Briefing, portal data"
git push origin main
```

Verify `clients/[slug]/` contains both the MCP and Agent Briefing.

---

## Step 7 — Deliver to Marcela

Report with:
1. Portal URL and password
2. Agent Briefing file (attach) — Ryan pastes this into the Client AI project instructions
3. MCP summary — auto-populated fields vs. pending kickoff confirmation
4. Authorized emails confirmed
5. Flag: "Next step for Ryan — paste Agent Briefing into the Client AI project instructions"

---

## Phase 3 Branch Logic

| Condition | `phase3.type` | Phase Label |
| :--- | :--- | :--- |
| No existing website | `new_build` | Phase 3 · Website Build |
| Existing site needing updates | `updates` | Phase 3 · Website Updates |
| Not a website client | `none` | Phase 3 hidden |

---

## File Guardrail (Non-Negotiable)

No files are stored locally permanently. Every file MUST be:
1. Committed to `marcela-egs/rpg-client-portal-template` under `clients/[slug]/`
2. Mirrored to the client's RPG Shared Drive folder

Local files in `/home/ubuntu/[slug]/` are working copies only.

---

## Skills Used During Onboarding

| Step | Skill |
| :--- | :--- |
| Website crawl | `ai-site-reporter`, `rpg-seo-audit` |
| ICP extraction | `rpg-mit-icp-reverse-engineer` |
| Drive operations | `scarlett-drive-guardrail`, `gws-best-practices` |
| Portal build | `webdev_init_project` + this skill's templates |

---

## Reference Files

- `references/mcp_template.md` — Master Client Profile template
- `references/agent_briefing_template.md` — Agent Briefing template
- `references/client_data_template.json` — Portal JSON data template
