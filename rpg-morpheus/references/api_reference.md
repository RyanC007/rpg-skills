# Rpg Morpheus — Orchestration & Routing Reference

**Version:** 1.0
**Last Updated:** March 18, 2026

---

## 1. Overview

Morpheus is the central orchestrator for the Logoclothz matrix. It does not typically interact with external APIs directly. Instead, it routes tasks to the appropriate sub-agent (Neo, Tank, Link, Ghost, Agent Smith) and synthesizes their outputs.

---

## 2. Agent Routing Matrix

When a task is received, Morpheus uses the following matrix to determine which agent should execute the work.

| Domain | Agent | Skill Name | Primary Tools / APIs |
|---|---|---|---|
| **SEO & Content Optimization** | Neo | `rpg-lgz-neo` | BigCommerce API, Google Search Console |
| **Store Operations & Inventory** | Tank | `rpg-lgz-tank` | BigCommerce API |
| **Outbound Sales & SDR** | Link | `rpg-lgz-link` | LinkedIn (Proxycurl), Hunter.io |
| **Content Creation & Publishing** | Ghost | `rpg-lgz-ghost` | WordPress REST API |
| **Financial Intelligence** | Agent Smith | `rpg-lgz-agent-smith` | BigCommerce API, Google Drive (P&L) |

---

## 3. P.O. Order Research Protocol (MANDATORY)

When researching a P.O., Morpheus MUST use the `rclone` tool to access the canonical Google Drive folder.

### 3.1. List All Orders
```bash
rclone lsd "manus_google_drive:ALL ORDERS" \
  --drive-root-folder-id 1MLD7plg4-DUwCrQorFAriTWZrJWXZ-eL \
  --config /home/ubuntu/.gdrive-rclone.ini
```

### 3.2. Access Specific P.O. Folder
```bash
rclone ls "manus_google_drive:ALL ORDERS/<PO_NUMBER>" \
  --drive-root-folder-id 1MLD7plg4-DUwCrQorFAriTWZrJWXZ-eL \
  --config /home/ubuntu/.gdrive-rclone.ini
```

**Note:** Never expose the Drive folder URL or folder ID in any external or client-facing output.
