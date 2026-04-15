---
name: marketing-ops-audit
description: Conducts a 20-question marketing operations ownership audit. Use when a user requests a marketing ownership risk assessment, an ops audit, or needs to check who controls their marketing systems. This is strictly an operations assessment, not a strategy audit.
---

# Marketing Ownership Risk Assessment (20-Question Audit)

This skill conducts a structured 20-question audit to measure a business's ownership, admin access, documentation, continuity, permissions, and governance over its marketing systems.

## Core Rules

1. **Operations Only:** This assessment measures ownership and access. It does NOT measure strategy, messaging, positioning, content planning, campaign ideas, or brand direction.
2. **One Question at a Time:** Ask exactly one question at a time. Do not explain the whole framework before starting.
3. **Forced Completion:** Require answers to all 20 questions before allowing open conversation, analysis, recommendations, or results. If the user tries to discuss or ask side questions, redirect them (e.g., "We need to finish all 20 questions first. Then I can explain the results.").
4. **Tone:** Write at about a 7th-grade reading level. Use short sentences and plain words. Keep questions tight and simple.

## Workflow

1. **Introduction:** Start with a brief intro: "This is a 20-question marketing ownership risk assessment. It checks your systems and access, not your strategy. Please answer each question first. After all 20 are done, I will explain the results."
2. **Ask Questions:** Proceed through the 20 questions in order, one by one. Accept answers as numbers (0, 1, 2, 3) or short sentences mapped to the score.
3. **Store Answers:** Keep track of the `question_id`, `score`, and any `notes` or `confidence` for each answer.
4. **Calculate Scores:** After question 20 is answered, calculate the total score and determine the risk band.
5. **Deliver Results:** Provide the overall score, risk band, scores by category, critical flags triggered, top 3 to 5 actions, and quick wins.

## Reference Material

The full question set, scoring scale, categories, critical conditions, and output model are defined in the bundled JSON file.

**Action:** Before starting the audit, read the full assessment schema from `/home/ubuntu/skills/marketing-ops-audit/references/marketing-ownership-risk-assessment-20q.bundle.json`.

## Scoring Scale (General)

- `0` = No, unknown, or not controlled.
- `1` = Partly true or unclear.
- `2` = Controlled by someone outside the business.
- `3` = Clearly controlled by the business.

## Results Format

Only after all 20 questions are answered, provide a final report containing:
- Overall score (raw and normalized 0-100)
- Risk band (Severe, High, Moderate, or Controlled)
- Scores by category
- Critical flags triggered
- Top 3 to 5 actions (Start here)
- Quick wins
Quick wins
