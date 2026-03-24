---
name: edg-data-storage
description: Mandatory data storage rules for Elite Design Group (EDG) tasks. Use whenever performing ANY file creation, output delivery, or data storage action for EDG. The EDG Shared Google Drive is the single source of truth. All EDG data, reports, and content must be stored there. The RPG Shared Drive is Scarlett's own brain — EDG data must NOT be stored there. GitHub (RyanC007/ai-manager-stack) is for code and versioned config only.
---

# EDG Data Storage — Single Source of Truth

## The Golden Rule

> **The EDG Shared Drive (`0ALUwTQXVI3lDUk9PVA`) is the single source of truth for ALL EDG data. No exceptions.**

**Drive URL:** https://drive.google.com/drive/folders/0ALUwTQXVI3lDUk9PVA

---

## EDG Shared Drive Folder Structure

| Folder | Purpose |
| :--- | :--- |
| `AI_Coordination/` | **Default target.** All AI agent outputs: reports, analysis, scripts, data files, client profile |
| `AI_Coordination/01_Project_Setup/` | Agent instructions, Scarlett context snapshot, project setup docs |
| `AI_Coordination/03_Knowledge_Base/` | Knowledge entries (JSON, MD, XLSX) |
| `AI_Coordination/04_Keyword_Research/` | Keyword CSVs and XLSX files |
| `AI_Coordination/05_Master_Synthesis/` | Master knowledge base, version changelog |
| `AI_Coordination/06_Extended_Knowledge_Package/` | Extended content strategy, completed content |
| `AI_Coordination/Scarlett_Oversight/` | Scarlett review queue, access package, feedback logs |
| `AI_Coordination/Reports/` | Monthly and weekly reports |
| `C_Elite Design Group/` | Client-facing deliverables |
| `C_Elite Design Group/2026_Content/` | Published and in-progress blog posts |
| `Knowledge Base Repo/` | Brand knowledge, strategy docs, keyword research |
| `product-data/` | WooCommerce product exports |

**Default upload target for all AI outputs:** `AI_Coordination/` folder.

---

## rclone Upload Command (Required Format)

```bash
rclone copy /path/to/file \
  "manus_google_drive:AI_Coordination/" \
  --drive-root-folder-id 0ALUwTQXVI3lDUk9PVA \
  --config /home/ubuntu/.gdrive-rclone.ini
```

## gws Upload Command (Required Format)

Always include `"supportsAllDrives": true`:

```bash
gws drive files create \
  --params '{"fields": "id,name,webViewLink", "supportsAllDrives": true}' \
  --json '{"name": "FILENAME", "parents": ["FOLDER_ID"]}' \
  --upload /path/to/file \
  --upload-content-type MIME_TYPE
```

---

## Scarlett Cross-Sync Protocol

Scarlett is the RPG AI orchestrator and provides quality oversight on EDG work. She needs EDG context to do her job.

**How Scarlett gets EDG context:**

Scarlett reads **directly from the EDG Shared Drive**. She does NOT store EDG data in her own RPG Shared Drive. The correct pattern is:

1. **EDG data lives in the EDG Shared Drive** — always, without exception.
2. **Scarlett reads from the EDG Shared Drive** — her access package and context snapshot are stored in `AI_Coordination/01_Project_Setup/` on the EDG drive.
3. **The RPG Shared Drive (`0AK8dAs_XgfnNUk9PVA`) is Scarlett's own brain** — EDG data must NOT be written there.

### When the EDG client profile is updated

Push the updated `edg_client_profile.md` to the EDG Shared Drive (not the RPG drive):

```bash
rclone copy /path/to/edg_client_profile.md \
  "manus_google_drive:AI_Coordination/" \
  --drive-root-folder-id 0ALUwTQXVI3lDUk9PVA \
  --config /home/ubuntu/.gdrive-rclone.ini
```

Also update the Scarlett Context Snapshot:

```bash
rclone copy /path/to/Scarlett_Context_Snapshot_EDG.md \
  "manus_google_drive:AI_Coordination/01_Project_Setup/" \
  --drive-root-folder-id 0ALUwTQXVI3lDUk9PVA \
  --config /home/ubuntu/.gdrive-rclone.ini
```

---

## GitHub Backup

The only permitted secondary storage is:

> **Repo:** `RyanC007/ai-manager-stack`

Use GitHub for: code, scripts, versioned config files, agent instruction files.
Use the EDG Shared Drive for: reports, data files, deliverables, knowledge base documents.

---

## Prohibited Locations

- **RPG Shared Drive (`0AK8dAs_XgfnNUk9PVA`)** — This is Scarlett's brain. EDG data must NOT be stored here.
- Personal Google Drive folders — including `1ln47wxV2tyAmjIeg-FGQLYPKpUyeuqC0` (legacy, do not use)
- Sandbox local storage as the only copy
- Any other cloud storage, S3, or external service

---

## Pre-Completion Checklist

Before marking any EDG task complete:

- [ ] All output files uploaded to `AI_Coordination/` in the **EDG Shared Drive** (`0ALUwTQXVI3lDUk9PVA`)
- [ ] No EDG files written to the RPG Shared Drive (`0AK8dAs_XgfnNUk9PVA`)
- [ ] No files left only in personal Drive or local sandbox
- [ ] Code/scripts backed up to `RyanC007/ai-manager-stack` if applicable
- [ ] If `edg_client_profile.md` was updated: pushed to `AI_Coordination/` on the EDG Shared Drive
- [ ] If Scarlett context changed: `Scarlett_Context_Snapshot_EDG.md` updated in `AI_Coordination/01_Project_Setup/`
