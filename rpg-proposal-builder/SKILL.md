---
name: rpg-proposal-builder
description: Customizes the standard RPG Business Backpack HTML proposal template for a specific prospect. Use when a user asks to build, create, or customize a proposal for a new client or prospect. Accepts discovery call transcripts or notes as input, extracts key data, presents a Human-in-the-Loop review before generating the final HTML, produces a walkthrough presentation script, and publishes the proposal as a password-protected live URL. Handles pricing, add-ons, waivers, cover details, and layout.
license: Complete terms in LICENSE.txt
---

# RPG Proposal Builder

Transforms raw discovery notes or transcripts into a completed, client-ready RPG Business Backpack proposal HTML file — and publishes it as a password-protected live URL. Always follows the Human-in-the-Loop checkpoint before generating the final file.

## Core Workflow

```
Step 1 → Extract data from discovery notes (script)
Step 2 → Present Human-in-the-Loop review (Scarlett presents, human approves)
Step 3 → Generate final proposal HTML (script, template only — no freehand edits)
Step 4 → Generate presentation script (Markdown)
Step 5 → Deliver both files as attachments
Step 6 → Publish as password-protected live URL (webdev project)
```

---

## Step 1: Extract Data from Discovery Notes

Run the extraction script against the provided notes or transcript file:

```bash
python3 /home/ubuntu/skills/rpg-proposal-builder/scripts/extract_proposal_data.py \
  --input /path/to/notes.md > /tmp/proposal_data_draft.json
```

The script uses the OpenAI API to parse the notes and returns structured JSON.

**CRITICAL RULE:** Never include "Conversion Strategy" — it is not an RPG service.

---

## Step 2: Human-in-the-Loop Review

Before generating the proposal, present the extracted data to the user for approval. Format the review as a clear summary covering:

1. **Client Info** — Company name, first name, proposal date
2. **What We Discussed** — The 3 synthesised pain points in RPG voice
3. **Investment** — Website dev fee, knowledge base fee, content plan selection, totals
4. **Open Questions** — Any gaps flagged by the extraction script that need human confirmation (e.g. content plan not yet chosen)

Ask the user to confirm or correct before proceeding. Do NOT generate the HTML until the user approves.

If the user provides additional context (e.g. "website is $2,000, content plan TBD"), update the JSON accordingly before running Step 3.

---

## Step 3: Generate Final Proposal HTML

**CRITICAL:** The template is the source of truth. Never rewrite, restructure, or freehand-edit any part of it. Only placeholder tokens are replaced — nothing else.

First, ensure the template is available locally. Clone if needed:

```bash
gh repo clone marcela-egs/rpg-backpack-proposal-template /tmp/rpg-backpack-proposal-template
```

Then run the generation script:

```bash
python3 /home/ubuntu/skills/rpg-proposal-builder/scripts/generate_proposal.py \
  --data /tmp/proposal_data_approved.json \
  --template /tmp/rpg-backpack-proposal-template/rpg-backpack-proposal.html \
  --output /tmp/[client-slug]-proposal.html
```

The script will report any unfilled placeholders. Fix them in the JSON and re-run if needed.

### Placeholder Reference

| Placeholder | Source Field |
|---|---|
| `[Client Company Name]` | `client_company_name` |
| `[Month Year]` | `proposal_month_year` |
| `[Paraphrase 1/2/3]` | `pain_points[0/1/2]` |
| `[PLAN COLOR]` | Derived from `content_plan` |
| `[Premium / Pro] Content Plan` | `content_plan` |
| `[$250 / $650]` | Derived from `content_plan` |
| `[New build / Redesign / Audit...]` | `website_type` |
| Website `$[TBD]` (first occurrence) | `website_dev_fee` |
| `[X] weeks` | `website_timeline_weeks` |
| Add-ons description | `addons_description` |
| Add-ons `$[TBD]` (second occurrence) | `addons_fee` |
| `$[TOTAL]` | `total_upfront` |
| `$[MONTHLY]` | `monthly_ongoing` |

---

## Step 4: Generate Presentation Script

Using the approved data, generate a tailored Markdown presentation script based on the template at:

```
/home/ubuntu/skills/rpg-proposal-builder/templates/script_template.md
```

Fill in all `[bracketed]` sections with client-specific content in RPG voice. Save as:

```
/tmp/[client-slug]-presentation-script.md
```

---

## Step 5: Deliver Files

Deliver both files to the user via the `message` tool:
- `[client-slug]-proposal.html`
- `[client-slug]-presentation-script.md`

Then ask the user if they want a password-protected live URL. If yes, proceed to Step 6.

---

## Step 6: Publish as Password-Protected Live URL

This step deploys the proposal as a live, password-protected website using the existing `hoover-proposal-portal` webdev project pattern. The proposal HTML becomes the site itself — no React wrapper, no iframes, no redirects.

### Why This Approach Works

The proposal template already has a password gate (`#rpg-gate-overlay`) baked into the HTML. The correct deployment method is to serve the proposal HTML **directly as `client/index.html`** in a webdev project. The Vite + Express server reads `client/index.html` and serves it at the root URL. This is the only approach that renders correctly — CDN redirects trigger downloads, and React wrappers add unnecessary complexity.

### 6a: Get the Password from the User

Ask the user for the password to protect the proposal before proceeding. Do not use a default.

### 6b: Inject the Password into the Proposal HTML

The proposal template's gate script uses a hardcoded password check. Locate and update it:

```bash
# Find the password line in the generated proposal
grep -n "rpgCheckPassword\|input.value ===" /tmp/[client-slug]-proposal.html
```

Edit the file to replace the placeholder password with the one provided by the user:

```javascript
// In the rpgCheckPassword function, update:
if (input.value === 'USER_PROVIDED_PASSWORD') {
```

### 6c: Initialize the Webdev Project

Use `webdev_init_project` with a project name derived from the client slug (e.g., `hoover-proposal-portal`). Use the default static template — no db/server/user features needed initially.

```
Project name: [client-slug]-proposal-portal
```

**If the project fails to serve the HTML correctly after initialization**, upgrade to `web-db-user` using `webdev_add_feature`. This enables the Express backend which reliably serves the proposal HTML. This was the proven fix for the Hoover engagement.

### 6d: Replace `client/index.html` with the Proposal HTML

This is the critical step. Copy the password-injected proposal HTML directly over the project's `client/index.html`:

```bash
cp /tmp/[client-slug]-proposal.html /home/ubuntu/[client-slug]-proposal-portal/client/index.html
```

**Do NOT place the proposal HTML in `client/public/`** — files over ~500KB in `public/` cause deployment timeouts.

**Do NOT use CDN redirect** — the browser will download the file instead of rendering it.

**Do NOT wrap in React or iframe** — unnecessary complexity and the iframe approach also triggers downloads.

### 6e: Restart and Verify

```bash
# Restart the dev server
webdev_restart_server

# Then open the dev URL in the browser and:
# 1. Confirm the password gate renders
# 2. Enter the correct password
# 3. Confirm the full proposal renders in-page (not a download, not a blank page)
```

### 6f: Save Checkpoint and Publish

Once verified in the browser:

1. Run `webdev_save_checkpoint` with a descriptive message
2. Instruct the user to click **Publish** in the top-right of the Management UI to get the permanent public URL
3. Deliver the checkpoint attachment and the password to the user

### Delivery Message Template

```
The proposal is live and password-protected.

Password: [USER_PROVIDED_PASSWORD]

Hit Publish in the top-right to get the permanent public URL to share with [Client First Name].
```

---

## Important Constraints

- **Backpack is always $1,500 flat.** Do not change scope or pricing of core Backpack deliverables unless explicitly instructed.
- **Template is sacred.** Copy it, replace placeholders only. No freehand HTML edits.
- **Content plan is a client choice.** If not confirmed, leave as "client to confirm" in the proposal — never assume.
- **No Conversion Strategy.** Ever.
- **Brand voice:** Direct, conversational, anti-BS, no jargon, no em dashes.
- **Publishing:** The proposal HTML IS the site. Replace `client/index.html` directly. No wrappers, no CDN redirects.
