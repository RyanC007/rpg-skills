---
name: rpg-content-strategy-onboarding
description: Ingest a client's keyword research spreadsheet and auto-generate a structured content strategy document, 12-post blog calendar, and agent routing README. Deploy all files to Google Drive and GitHub. Use when onboarding a new RPG client who has a completed keyword research spreadsheet, or when a client's content strategy needs to be initialized or refreshed.
---

# RPG Content Strategy Onboarding Skill

This skill converts a standardized keyword research spreadsheet into a fully deployed content strategy — ready for all AI manager agents to consume.

## When to Use

Invoke this skill when a new RPG client has been onboarded and their keyword research spreadsheet is available, when a client's content strategy needs to be initialized for the first time, or when a content strategy refresh is requested.

## Required Inputs

Before running, confirm you have:

| Input | Description | Example |
| :--- | :--- | :--- |
| `client_name` | Full client name | `"Red Horse Construction"` |
| `spreadsheet_path` | Absolute path to `.xlsx` keyword research file in sandbox | `/home/ubuntu/Client_Keyword_Research.xlsx` |
| `gdrive_folder_id` | Google Drive root folder ID for the client | `0AMo6XJqwjJ1zUk9PVA` |
| `github_repo` | GitHub repo for the AI Manager Stack | `RyanC007/ai-manager-stack` |
| `gdrive_content_path` | Path inside Drive for the Content_Plan folder | `RedHorse-Ai/Content_Plan` |
| `github_content_path` | Path inside repo for the client's content folder | `clients/red-horse-construction/content` |

## Spreadsheet Format Requirements

The spreadsheet MUST contain these sheets (matching the RPG Master Keyword Research template):

| Sheet Name | Used For |
| :--- | :--- |
| `AEO Questions` | Primary source of blog post topics. Columns: Keyword, Volume, AEO_Opportunity (HIGH/MEDIUM/LOW), Content_Type |
| `Investor Flipping - BLUE OCEAN` | Investor-focused Blue Ocean topics. Columns: Keyword, Volume, Opportunity_Type (BLUE OCEAN/NICHE) |
| `Keyword Pool` | Primary service keywords (used for SEO tracking reference) |

If the client's spreadsheet uses different sheet names, rename the relevant sheets before running.

## Execution Steps

### Step 1 — Run the Engine Script

```bash
python3 /home/ubuntu/skills/rpg-content-strategy-onboarding/scripts/generate_strategy.py \
  --client "{client_name}" \
  --spreadsheet "{spreadsheet_path}" \
  --output /tmp/content_strategy_output \
  --start-date "{YYYY-MM-DD of first publish date, or omit for auto}" \
  --gdrive-path "{gdrive_content_path}" \
  --github-path "{github_content_path}"
```

Optional flags:
- `--brand-pillars "Pillar 1,Pillar 2,Pillar 3,Pillar 4"` — override default brand pillars
- `--audiences "Homeowner,Investor"` — override default audiences

The script outputs to `/tmp/content_strategy_output/`:
- `{client_slug}_Content_Strategy_v1.md` — the strategy document
- `README.md` — the agent routing file for the Content_Plan folder
- `onboarding_summary.json` — machine-readable summary for the calling agent

### Step 2 — Deploy to Google Drive

```bash
rclone copy /tmp/content_strategy_output/ \
  "manus_google_drive:{gdrive_content_path}/" \
  --config /home/ubuntu/.gdrive-rclone.ini \
  --drive-root-folder-id {gdrive_folder_id}
```

### Step 3 — Deploy to GitHub

```bash
cd /home/ubuntu/ai-manager-stack
git pull origin master --rebase
mkdir -p {github_content_path}
cp /tmp/content_strategy_output/*.md {github_content_path}/
git add .
git commit -m "feat: Add content strategy v1 for {client_name}"
git push origin master
```

### Step 4 — Copy to Project Shared Files

```bash
cp /tmp/content_strategy_output/{client_slug}_Content_Strategy_v1.md \
  /home/ubuntu/projects/{project_directory}/
```

This ensures the strategy document is loaded automatically in every future task for this project.

### Step 5 — Confirm and Report

Read `onboarding_summary.json` and report to the user: number of posts in the calendar, first and last publish dates, Google Drive shareable link (generate with `rclone link`), and GitHub commit URL.

## Versioning

When updating an existing strategy (e.g., when a client's updated plan arrives): re-run the engine with a new output directory, rename the output file to `v2`, update the README to point to v2, deploy using Steps 2–4, and archive v1 by moving it to an `_archive/` subfolder in Drive.

## Notes

- The engine automatically infers `Target Audience` (Homeowner vs. Investor) from keyword content.
- Brand pillar assignment uses keyword matching; override with `--brand-pillars` if the client has custom pillars.
- Publish dates alternate between the 1st and 15th of each month starting from the provided start date.
- The script handles missing sheets gracefully — if `Investor Flipping - BLUE OCEAN` is absent, it fills the calendar with AEO topics only.
