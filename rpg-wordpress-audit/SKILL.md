---
name: rpg-wordpress-audit
description: "Performs a comprehensive, automated audit of a WordPress installation via SSH. Use when a user wants to diagnose a poorly functioning WordPress site, investigate broken cron jobs, check security, review plugin/theme health, or get a full site health report. Collects SSH and database credentials, then runs a multi-stage audit and produces a structured report."
---

# RPG WordPress Audit

## Overview

This skill connects to a remote WordPress installation via SSH and runs a structured, multi-stage audit covering core file integrity, plugins, themes, database health, security, cron jobs, and performance. The output is a comprehensive Markdown report with findings and prioritised recommendations.

## Audit Workflow

1. **Collect Credentials** — Ask the user for SSH and database details
2. **Verify Connectivity** — Confirm SSH access and WP-CLI availability
3. **Run Audit Scripts** — Execute the six audit modules in sequence
4. **Generate Report** — Populate the report template and deliver to the user

---

## Step 1: Collect Credentials

Use the `message` tool (`ask` type) to request the following from the user in a single message. Store all values as shell environment variables for the session. **Never write credentials to disk.**

| Variable | Description | Default |
| :--- | :--- | :--- |
| `SSH_HOST` | Hostname or IP of the server | — |
| `SSH_USER` | SSH username | — |
| `SSH_PORT` | SSH port | `22` |
| `SSH_KEY_PATH` | Path to private key file (if not password auth) | — |
| `WP_PATH` | Absolute path to WordPress root on the server | `/var/www/html` |
| `DB_HOST` | Database host | `localhost` |
| `DB_NAME` | WordPress database name | — |
| `DB_USER` | Database username | — |
| `DB_PASSWORD` | Database password | — |

If the user provides an SSH private key, ask them to paste it and save it temporarily to `/tmp/wp_audit_key` with `chmod 600`.

---

## Step 2: Verify Connectivity

Before running the audit, confirm the connection works and that WP-CLI is available:

```bash
# Test SSH connection
ssh -p $SSH_PORT -i $SSH_KEY_PATH $SSH_USER@$SSH_HOST "echo 'SSH OK'"

# Confirm WP-CLI is installed
ssh -p $SSH_PORT -i $SSH_KEY_PATH $SSH_USER@$SSH_HOST "wp --info --path=$WP_PATH"
```

If WP-CLI is not installed, install it on the remote server:

```bash
ssh -p $SSH_PORT -i $SSH_KEY_PATH $SSH_USER@$SSH_HOST "
  curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar &&
  chmod +x wp-cli.phar &&
  sudo mv wp-cli.phar /usr/local/bin/wp
"
```

---

## Step 3: Run Audit Scripts

Execute each script via SSH. Capture the output of each into a variable or temp file for use in the report. The scripts are located at `/home/ubuntu/skills/rpg-wordpress-audit/scripts/`.

```bash
# Helper alias for running remote WP-CLI commands
WP_SSH="ssh -p $SSH_PORT -i $SSH_KEY_PATH $SSH_USER@$SSH_HOST wp --path=$WP_PATH"

bash /home/ubuntu/skills/rpg-wordpress-audit/scripts/01_core_check.sh
bash /home/ubuntu/skills/rpg-wordpress-audit/scripts/02_plugin_theme_check.sh
bash /home/ubuntu/skills/rpg-wordpress-audit/scripts/03_database_check.sh
bash /home/ubuntu/skills/rpg-wordpress-audit/scripts/04_security_check.sh
bash /home/ubuntu/skills/rpg-wordpress-audit/scripts/05_cron_check.sh
bash /home/ubuntu/skills/rpg-wordpress-audit/scripts/06_performance_check.sh
```

Each script uses the environment variables set in Step 1. Collect all output and note any errors or warnings.

---

## Step 4: Generate Report

1. Read the report template: `/home/ubuntu/skills/rpg-wordpress-audit/templates/audit_report.md`
2. Populate every section with findings from the audit scripts.
3. For each finding, assign a severity: `CRITICAL`, `WARNING`, or `OK`.
4. Include a prioritised **Recommendations** section at the end.
5. Save the completed report to `/tmp/wp_audit_report_<SITE_NAME>.md`.
6. Deliver the report to the user via the `message` tool (`result` type) with the file attached.

---

## Severity Guide

| Severity | Meaning |
| :--- | :--- |
| **CRITICAL** | Immediate action required — security risk, data loss risk, or site-breaking issue |
| **WARNING** | Should be addressed soon — performance, outdated software, or misconfiguration |
| **OK** | No action required |

---

## Notes

- All scripts assume WP-CLI is available on the remote server at `/usr/local/bin/wp`.
- Scripts use `--allow-root` flag only if the SSH user is `root`.
- If the site uses a managed host (e.g., WP Engine, Kinsta) that restricts SSH, note this to the user and fall back to REST API-based checks where possible.
- Clean up the temporary SSH key after the audit: `rm -f /tmp/wp_audit_key`

## Mandatory Output Sanitization

**BEFORE delivering any file, report, post, or content to the user or saving to Google Drive, you MUST run the sanitization tool on the output file.** This is non-negotiable and applies to every agent and every output type.

### Standard RPG Sanitization (All Agents)

```bash
python3 /home/ubuntu/knowledge_bases/rpg-branded-agents/skills/_guardrails/sanitize_output.py --input /path/to/output_file.md
```

The tool overwrites the file in place. Use `--output /path/to/clean_file.md` to save a separate sanitized copy instead.

### Logoclothz Agents (Additional Rules)

```bash
python3 /home/ubuntu/knowledge_bases/rpg-branded-agents/skills/_guardrails/sanitize_output.py --input /path/to/output_file.md --logoclothz
```

### Sanitization Checklist

- [ ] Sanitization tool has been run on the output file
- [ ] No errors or flagged content remain in the output
- [ ] Sanitized file (not the pre-sanitization draft) is what gets delivered or saved to Drive
