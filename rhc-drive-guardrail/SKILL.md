---
name: rhc-drive-guardrail
description: Enforces Google Drive guardrails for Red Horse Construction (RHC) projects. Use this skill for any file I/O operation related to RHC to ensure data is always read from and written to the correct shared Google Drive folder.
---

# Red Horse Construction Drive Guardrail

This skill enforces critical data handling policies for all Red Horse Construction (RHC) projects. Adherence to these rules is mandatory to prevent data loss and maintain the integrity of the project's file structure.

## Core Principle: Shared Drive is the Source of Truth

All file operations for Red Horse Construction MUST be performed on the designated shared Google Drive folder. This folder is the single source of truth for all project files.

-   **NEVER** use the personal Google Drive root (`manus_google_drive:`).
-   **ALWAYS** target the `RedHorse-Ai` folder within the shared Drive.

## `rclone` Command Guardrail

To enforce the use of the shared Drive, every `rclone` command executed for an RHC project **MUST** include the `--drive-root-folder-id` flag with the correct ID.

-   **Shared Drive Folder ID:** `0AMo6XJqwjJ1zUk9PVA`
-   **Required Flag:** `--drive-root-folder-id 0AMo6XJqwjJ1zUk9PVA`

### Example `rclone` Commands

**Copying a file to the shared drive:**

```bash
rclone copy /path/to/local/file.txt manus_google_drive:RedHorse-Ai/Content_Plan --drive-root-folder-id 0AMo6XJqwjJ1zUk9PVA
```

**Listing files in the shared drive:**

```bash
rclone ls manus_google_drive:RedHorse-Ai/RHC_Reports --drive-root-folder-id 0AMo6XJqwjJ1zUk9PVA
```

## Drive Configuration Reference

For a complete reference of all folder paths and configuration details, consult the `drive_config.json` file. A copy of this file is included in the skill's `references` directory.

To read the configuration:

```bash
cat /home/ubuntu/skills/rhc-drive-guardrail/references/drive_config.json
```

## Summary of Rules

| Rule | Description |
| :--- | :--- |
| **Source of Truth** | All file I/O MUST go to the `RedHorse-Ai` folder on the shared Google Drive. |
| **`rclone` Flag** | Every `rclone` command MUST use the `--drive-root-folder-id 0AMo6XJqwjJ1zUk9PVA` flag. |
| **No Personal Drive** | NEVER write to the personal Google Drive root (`manus_google_drive:`). |
| **GitHub is Backup** | The GitHub repository is for backup purposes only. The shared Drive is the live working environment. |
