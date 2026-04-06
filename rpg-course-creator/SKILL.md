---
name: rpg-course-creator
description: Creates structured online course content for RPG. Use when building course modules, lesson scripts, workbooks, or full course outlines for the RPG course catalog. Applies RPG educational voice, structures content for adult learners, and outputs ready-to-use course materials.
---

# Rpg Course Creator

OUTPUT_TIER: 1 (Public Outbound) for published course content
OUTPUT_TIER: 3 (Internal) for outlines and planning docs

## Purpose
Build structured online course content for RPG. Covers full course architecture, individual module outlines, lesson scripts, and student workbooks.

## Course Architecture Standard

### Course Structure
- 4-6 modules per course
- 3-5 lessons per module
- Each lesson: 10-15 minutes of content
- Each module: one clear transformation or skill gained
- Course: one clear outcome the student achieves

### Lesson Structure
1. Hook (30 seconds) - Why this lesson matters
2. Concept (3-5 minutes) - The core idea, plain language
3. Example (2-3 minutes) - Real-world application
4. Action step (1-2 minutes) - What the student does now
5. Summary (30 seconds) - One sentence takeaway

## Workflow

### Step 1: Define Course Outcome
What can the student DO after completing this course? One clear, specific outcome.

### Step 2: Build Module Outline
Map the journey from where the student starts to the course outcome. Each module is one step in that journey.

### Step 3: Write Lesson Scripts
For each lesson, write a full script following the lesson structure above. RPG voice: direct, no jargon, practical.

### Step 4: Create Workbook
For each module, create a student workbook page with:
- Key concept summary
- Reflection questions
- Action steps with checkboxes
- Space for notes

### Step 5: Quality Check
- [ ] Each lesson has a clear action step
- [ ] No corporate jargon
- [ ] Examples relevant to small business owners
- [ ] Workbook aligns with lesson content

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
