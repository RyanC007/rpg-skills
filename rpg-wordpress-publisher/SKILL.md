---
name: rpg-wordpress-publisher
description: Publishes content to a client's WordPress website via the WordPress REST API. Use when content has been approved and needs to be posted to a WordPress site. Requires the site URL and an application password. Always defaults to draft status unless explicitly instructed to publish live.
---

# Rpg Wordpress Publisher

OUTPUT_TIER: 2 (Client-Facing)

## Guardrails (Tier 2 - Mandatory)
- Never publish live without explicit instruction. Default is always draft.
- Never expose WordPress application passwords in logs or outputs
- No internal repo references in post content

## Purpose
Publish approved content to a client's WordPress site via the REST API. No plugin required. Uses WordPress Application Passwords for authentication.

## Prerequisites
- WordPress site URL
- WordPress Application Password (created in WP Admin > Users > Profile > Application Passwords)
- WordPress username
- Approved content ready to post

## Workflow

### Step 1: Load Credentials
Retrieve the client's WordPress credentials from their knowledge base in Google Drive. Never hardcode credentials.

### Step 2: Prepare the Post Payload
```python
post_data = {
    "title": "Post Title Here",
    "content": "Full post content in HTML or markdown",
    "status": "draft",
    "categories": [],
    "tags": [],
    "meta": {
        "_yoast_wpseo_title": "SEO Meta Title",
        "_yoast_wpseo_metadesc": "SEO Meta Description"
    }
}
```

### Step 3: Post via REST API
```python
import requests
from requests.auth import HTTPBasicAuth

response = requests.post(
    f"{site_url}/wp-json/wp/v2/posts",
    json=post_data,
    auth=HTTPBasicAuth(username, application_password)
)

if response.status_code == 201:
    post_id = response.json()["id"]
    post_url = response.json()["link"]
    print(f"Post created: {post_url}")
else:
    print(f"Error: {response.status_code} - {response.text}")
```

### Step 4: Confirm and Report
- Log the post ID and URL to the client's context entry in Google Drive
- Notify Ryan or Marcela that the post is live or in draft
- If draft: include the WordPress admin edit URL for review

## Default Behavior
- Status: draft unless explicitly instructed to set publish
- Never delete or modify existing posts without explicit instruction
- If the API returns an error, stop and report. Do not retry without checking credentials.

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
