---
name: rpg-8book-framework
description: Runs the RPG Strategy Analysis Framework on any new idea, strategy, or business decision. Built from 8 essential business books. Use when Ryan or the RPG team asks to evaluate an idea, strategy, or decision before committing resources.
---

# RPG 8 Book Framework

## Purpose
This skill is the decision-making engine for Ready, Plan, Grow! It evaluates any new idea, strategy, or business decision through a structured, modular framework derived from 8 essential business books. It eliminates guesswork, surfaces blind spots, and produces a clear, scored recommendation before resources are committed.

**Source books:** Thinking in Bets (Duke), Thinking Fast and Slow (Kahneman), The Innovator's Dilemma (Christensen), Atomic Habits (Clear), So Good They Can't Ignore You (Newport), Fooled by Randomness (Taleb), Superforecasting (Tetlock), The Intelligence Trap (Robson).

## When to Activate
- "Run the framework on [idea or strategy]."
- "Evaluate this decision."
- "Should we do [X]?"
- "Score this idea."
- "Is this worth pursuing?"
- Any time a new product, campaign, hire, or operational change is being considered.

## Workflow

### Step 1: Identify the Decision Type
Based on the user's input, determine which category the decision falls into:

| Decision Type | Use When |
| :--- | :--- |
| **Product / Offer** | Launching a new service, course, or tool |
| **Marketing / Acquisition** | Planning a campaign, funnel, or content strategy |
| **Operational / Financial** | Hiring, pricing changes, or investing capital |
| **Leadership / Team** | Managing culture, conflict, or team decisions |

If the decision spans multiple types, run the primary module first, then the secondary module.

### Step 2: Select and Run the Module

#### Module 1: Product / Offer Analysis
*Core books: The Innovator's Dilemma + So Good They Can't Ignore You*

1. **The Disruption Check:** Are we attacking from below? Does this offer a simpler, cheaper, more accessible solution that big agencies are ignoring?
2. **The Career Capital Check:** Does this leverage our rare, valuable skills, or are we chasing a trend we know nothing about?
3. **The Ownership Test:** Does the client own the output? If they don't, it's an agency model, not an RPG model.
4. **The Premortem:** Imagine it's 6 months from now and this product completely failed. What went wrong?

#### Module 2: Marketing / Acquisition Analysis
*Core books: Atomic Habits + Thinking, Fast and Slow*

1. **The System Check:** Does this build a repeatable system, or just create a one-off task?
2. **The 1% Compounding Effect:** Does doing this make tomorrow slightly easier, or does it reset the clock every day?
3. **The System 1 Filter:** Is the messaging simple, direct, and emotional? Are we speaking to the client's immediate pain, or boring them with logic?
4. **The Friction Test:** What is the hardest part of executing this consistently? How do we make it obvious, attractive, easy, and satisfying?

#### Module 3: Operational / Financial Analysis
*Core books: Thinking in Bets + Fooled by Randomness + Superforecasting*

1. **The Probability Check:** Assign a real percentage. If it is under 50%, why are we doing it?
2. **The Downside Protection:** If this bet goes to zero, does it hurt the core business?
3. **The Outside View:** Who else has tried this exact thing, and what were their actual results?
4. **The Variance Check:** If this succeeds wildly, how much of that is luck vs. skill?

#### Module 4: Leadership / Team Analysis
*Core books: The Intelligence Trap + Grit*

1. **The Ego Check:** Are we doing this because it's the best move, or because it sounds cool?
2. **The Decision Pod:** Who is the one person who will tell me this is a bad idea? Have I asked them yet?
3. **The Grit Factor:** Does this require sustained effort over years? Is the team prepared for the marathon?
4. **The Intellectual Humility Test:** If new data proves our strategy wrong tomorrow, how fast can we pivot without losing face?

### Step 3: Score the Decision

| Score | Verdict | Action |
| :--- | :--- | :--- |
| 4 / 4 | Green light | Move fast. |
| 3 / 4 | Amber light | Fix the one weakness before launch. |
| 2 / 4 | Red light | Redesign the idea or kill it. |
| 1 / 4 or less | Kill it | The idea is not ready. |

### Step 4: Deliver the Output
Present the analysis clearly to the user. The output must include:
- The module(s) used and why.
- The answers to all 4 questions, written out.
- The final score (Green / Amber / Red).
- A clear, direct recommended action.

## Inputs Required

| Field | Required? | Description |
| :--- | :--- | :--- |
| Idea or Decision | Yes | A one-sentence description of what is being evaluated. |
| Context | No | Any relevant background, market data, or prior research. |
| Module Override | No | If Ryan specifies a module, use that one. Otherwise, auto-select. |

## Output Format
A structured analysis report containing:
- Decision type and module selected.
- 4 scored questions with written answers.
- Final score and verdict.
- Recommended next action.

## Guardrails
- MUST NOT guess or fabricate data. If a question requires market data, pull it.
- MUST write out all 4 answers. Thinking about it is not the same as writing it down.
- MUST NOT skip the scoring step. Every analysis ends with a clear score.
- MUST apply the Tier 3 (Internal) guardrail tier for all outputs from this skill.

## Mandatory Output Sanitization
**BEFORE delivering any file, report, post, or content to the user or saving to Google Drive, you MUST run the sanitization tool on the output file.** This is non-negotiable and applies to every agent and every output type.

```bash
python3 /home/ubuntu/knowledge_bases/rpg-branded-agents/skills/_guardrails/sanitize_output.py --input /path/to/output_file.md
```

The tool overwrites the file in place. Use `--output /path/to/clean_file.md` to save a separate sanitized copy instead.

### Sanitization Checklist
- [ ] Sanitization tool has been run on the output file
- [ ] No errors or flagged content remain in the output
- [ ] Sanitized file (not the pre-sanitization draft) is what gets delivered or saved to Drive
