---
name: edg-social-media-gen
description: Generates standardized 4:5 (1080x1350) social media posts for Elite Design Group (EDG) house plans. Use when creating IG content from elitedesigngroup.com plan links.
---

# EDG Social Media Generation Skill

This skill automates the creation of 4:5 aspect ratio Instagram posts for EDG house plans, ensuring brand consistency and perfect viewport rendering.

## Workflow

### 1. Information Gathering
- Navigate to the provided `elitedesigngroup.com` house plan URL.
- Extract: Plan Number, Plan Name, Style (Main & Accent), Square Feet, Beds, Baths, Garages, Footprint, and Starting Price.
- Extract the primary house plan image URL.

### 2. Image Processing
- Download the primary image.
- Use `scripts/process_image.py` to create a 1080x1350 JPG version for the IG background/hero.
- Upload processed images using `manus-upload-file` to get public URLs for the HTML templates.

### 3. Template Rendering
- Use `templates/cover_template.html`.
- Replace placeholders (e.g., `{{PLAN_NAME}}`, `{{IMAGE_URL}}`) with extracted data.
- **CRITICAL**: The template is pre-optimized to fill the 1080x1350 viewport exactly. Do NOT add body padding or centering.
- Render to PNG using Puppeteer at exactly 1080x1350 resolution.

### 4. Final Conversion & Storage
- Convert the rendered PNG to JPG format.
- Name the file: `Elite Design Group_House_Plan[Number]_Cover.jpg`
- Upload to the EDG Shared Drive (`1nC94j49lj2GSXRG6udkTTYRvHpmz1Tiw`) inside the `Social Media/House Plan IG` folder structure.

## Resource Paths
- **Cover Template**: `templates/cover_template.html`
- **Image Script**: `scripts/process_image.py`

## Storage Protocol
- **Shared Drive ID**: `0ALUwTQXVI3lDUk9PVA`
- **Parent Folder ID (AI_Coordination)**: `1nC94j49lj2GSXRG6udkTTYRvHpmz1Tiw`
- **Target Subfolders**: `Social Media` > `House Plan IG`
- **Mandatory**: Use `"supportsAllDrives": true` in all `gws` commands.
