---
name: scarlett-drive-guardrail
description: Enforces Google Drive guardrails for all Scarlett tasks. Use this skill for any file I/O operation to ensure data is always read from and written to the correct RPG Shared Drive folder.
---

# Scarlett Drive Guardrail

This skill enforces critical data handling policies for Scarlett. Adherence to these rules is mandatory to prevent data loss, maintain the integrity of the project's file structure, and ensure the `Scarlett-AI` Shared Drive remains the single source of truth.

## Core Principle: The RPG Shared Drive is the Source of Truth

All file operations MUST be performed on the designated RPG Shared Drive. This drive is the single source of truth for all knowledge, protocols, client files, and context.

-   **NEVER** use the personal Google Drive root (`manus_google_drive:`).
-   **ALWAYS** target the `0AK8dAs_XgfnNUk9PVA` Shared Drive.
-   **NEVER** permanently delete any file. Always move files to the trash.

## `rclone` Command Guardrail

To enforce the use of the shared Drive, every `rclone` command executed by Scarlett **MUST** include the `--drive-root-folder-id` flag with the correct ID.

-   **Shared Drive Folder ID:** `0AK8dAs_XgfnNUk9PVA`
-   **Required Flag:** `--drive-root-folder-id 0AK8dAs_XgfnNUk9PVA`

### Example `rclone` Commands

**Copying a file to the shared drive (e.g., saving a report):**

```bash
rclone copy /path/to/local/report.md manus_google_drive:Scarlett/Reports/ --drive-root-folder-id 0AK8dAs_XgfnNUk9PVA
```

**Listing files in the shared drive:**

```bash
rclone lsf manus_google_drive:Scarlett-System-Files/ --drive-root-folder-id 0AK8dAs_XgfnNUk9PVA
```

## `gws` Command Guardrail

When using the `gws` CLI tool, you MUST specify the `driveId` and include the necessary flags to support shared drives.

-   **Required Parameters:** `"driveId": "0AK8dAs_XgfnNUk9PVA", "supportsAllDrives": true`
-   **For Search (`q`):** Also include `"includeItemsFromAllDrives": true, "corpora": "drive"`

### Example `gws` Commands

**Listing files in a specific folder:**

```bash
gws drive files list --params '{"driveId": "0AK8dAs_XgfnNUk9PVA", "includeItemsFromAllDrives": true, "supportsAllDrives": true, "corpora": "drive", "q": "\"1X4opx6gIGUNnOjTvGcE6WlXCHRukdhQy\" in parents"}'
```

## Drive Configuration Reference

For a complete reference of all folder paths and configuration details, consult the `drive_config.json` file. A copy of this file is included in the skill's `references` directory.

To read the configuration:

```bash
cat /home/ubuntu/skills/scarlett-drive-guardrail/references/drive_config.json
```

## Summary of Rules

| Rule | Description |
| :--- | :--- |
| **Source of Truth** | All file I/O MUST go to the RPG Shared Drive (`0AK8dAs_XgfnNUk9PVA`). |
| **`rclone` Flag** | Every `rclone` command MUST use the `--drive-root-folder-id 0AK8dAs_XgfnNUk9PVA` flag. |
| **`gws` Params** | Every `gws` command MUST use `"driveId": "0AK8dAs_XgfnNUk9PVA"` and `"supportsAllDrives": true`. |
| **No Personal Drive** | NEVER write to the personal Google Drive root. |
| **No Deletion** | NEVER permanently delete files. |
