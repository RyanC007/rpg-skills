# SDR Lead Scraper Agent - Recovery Guide

**Disaster recovery procedures for the Manus Agent Skill.**

## Re-clone Repository

If the agent directory is deleted or corrupted:

```bash
cd /home/ubuntu/knowledge_bases
git clone https://github.com/RyanC007/rpg-skills.git
```

## Verify Google Drive

Ensure Google Drive is configured via rclone:
```bash
rclone lsf manus_google_drive: --config /home/ubuntu/.gdrive-rclone.ini
```

If this fails, the Google Drive integration needs to be re-authorized.

## Re-run Test

Invoke the skill with a small test search:

```
Run sdr-lead-scraper-agent to find 5 architects in Raleigh, NC
```

This will verify that the browser automation and Google Drive export are working correctly.
