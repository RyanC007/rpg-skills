---
name: rpg-youtube-thumbnail
description: Creates YouTube thumbnail images for RPG video content. Use when generating thumbnail images for YouTube videos. Takes the video title and topic as input, generates a branded thumbnail following RPG visual guidelines, and outputs a 1280x720 image ready for upload.
---

# Rpg Youtube Thumbnail

OUTPUT_TIER: 1 (Public Outbound)

## Guardrails (Tier 1)
- No client names on thumbnails
- No internal URLs or file paths in image metadata

## Thumbnail Specifications
- Size: 1280x720 pixels (16:9)
- File format: JPG or PNG
- Max file size: 2MB
- Text must be legible at 320x180 (small preview size)

## RPG Thumbnail Design Standards
- Background: Bold color (RPG yellow #F5C518, orange #FF6B35, or dark #1a1a1a)
- Primary text: Large, bold, Poppins or system sans-serif
- Max 6 words of text on the thumbnail
- Include RPG logo or brand mark in corner
- High contrast between text and background

## Workflow

### Step 1: Get Input
Required:
- Video title
- Video topic/theme
- Tone (educational, provocative, story-based)
- Any specific visual elements requested

### Step 2: Generate Thumbnail
Use the generate tool to create the image. Prompt should specify:
- Dimensions: 1280x720
- Style: Bold, clean, professional
- RPG brand colors
- Text overlay content
- Background treatment

### Step 3: Quality Check
- [ ] Text legible at small size
- [ ] RPG brand colors used
- [ ] No more than 6 words of text
- [ ] High contrast
- [ ] Logo/brand mark present

### Step 4: Deliver
Save to the video's project folder and deliver to Ryan or Marcela for upload.

## Mandatory Output Sanitization

**BEFORE delivering any file, report, post, or content to the user or saving to Google Drive, you MUST run the sanitization tool on the output file.** This is non-negotiable and applies to every agent and every output type.

### Standard RPG Sanitization (All Agents)

```bash
python3 /home/ubuntu/knowledge_bases/rpg-skills/skills/_guardrails/sanitize_output.py --input /path/to/output_file.md
```

The tool overwrites the file in place. Use `--output /path/to/clean_file.md` to save a separate sanitized copy instead.

### Logoclothz Agents (Additional Rules)

```bash
python3 /home/ubuntu/knowledge_bases/rpg-skills/skills/_guardrails/sanitize_output.py --input /path/to/output_file.md --logoclothz
```

### Sanitization Checklist

- [ ] Sanitization tool has been run on the output file
- [ ] No errors or flagged content remain in the output
- [ ] Sanitized file (not the pre-sanitization draft) is what gets delivered or saved to Drive
