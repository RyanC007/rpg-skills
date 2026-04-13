---
name: rpg-marcela-linkedin
description: Generates Marcela's weekly LinkedIn content for Ready, Plan, Grow!. Produces 5 posts (Mon-Fri), 1 image per post using the 5-template rotation (Whiteboard, Newspaper, Chalkboard, Open Book, Billboard), and compiles everything into a Google Doc Posting Guide saved to RPG Shared Drive. Use when generating Marcela's LinkedIn content, running the weekly content pipeline, or building a posting guide for Marcela.
---

# RPG Marcela LinkedIn Content Pipeline

**Mode:** Human-in-the-loop. No automation. No Blotato. No scheduling.
**Output Tier:** 1 (Public Outbound — strictest guardrails apply)
**Owner:** Scarlett

---

## Pipeline Steps

| Step | Scarlett Does | Marcela Does |
| :--- | :--- | :--- |
| 1 | Generate 5 posts using Marcela's voice brief and content pillars | Reviews posts |
| 2 | Generate 1 image per post using the template rotation | Approves or requests changes |
| 3 | Compile into a Google Doc Posting Guide | Posts manually to LinkedIn at 7 AM EST each day |
| 4 | Deliver the Google Doc link to Ryan | Done |

Scarlett stops at the Google Doc. Marcela does the posting.

---

## Approved Tools

Manus, Claude, ChatGPT, GitHub, Python, VS Code, Google Drive, Google Sheets, Excel.

**Banned (hard failure if used):** Zapier, Airtable, HubSpot, Mailchimp, Notion, Confluence, QuickBooks, Float, Slack, Blotato.

---

## Weekly Posting Schedule

5 posts per week. One per day. Marcela posts manually at 7 AM EST.

| Day | Content Pillar | Tone |
| :--- | :--- | :--- |
| Monday | Strategy and Opportunity Cost | Direct, empowering, slightly challenging |
| Tuesday | Marketing Operations and GTM | Practical, operator-first, no fluff |
| Wednesday | Know Your Numbers | Clear, confident, non-condescending |
| Thursday | Leadership and Founder Mindset | Warm, honest, reflective |
| Friday | Small Business News and Market Reality | Grounded, informed, calm. Not political. |

---

## Content Pillars

**Monday — Strategy and Opportunity Cost:** The $25/Hour vs. $500/Hour Work Test. Prioritization, delegation, leverage, cutting low-value work, building systems that scale without the founder.

**Tuesday — Marketing Operations and GTM:** Go-to-market clarity, campaign structure, positioning, and the mechanics of getting customers. Marcela's 20+ years of operator experience lives here.

**Wednesday — Know Your Numbers:** CAC, LTV, margins, cash flow timing, pricing strategy, reading a P&L. Financial literacy for founders, not accounting theory.

**Thursday — Leadership and Founder Mindset:** The human side of running a company. Founder loneliness, confidence through systems, operating with clarity, the emotional reality of leadership.

**Friday — Small Business News and Market Reality:** Tariffs, interest rates, supply chain shifts, policy changes, economic signals. Translate the noise into practical implications for the small business owner. Always anchor in "here is what this means for your business and here is what you can do about it."

---

## Marcela's Voice Rules (Non-Negotiable)

- Supportive but direct. She does not coddle. She respects her audience enough to tell the truth.
- Practical over theoretical. Every post must have something the reader can do today.
- Low fluff. No corporate jargon. No empty motivational speak. No hyperbole.
- Human-first. The human experience of running a business is always the anchor.
- No em dashes. Full stop.
- No "unprecedented," "game-changing," or unprovable superlatives. Ever.
- No "Founders Flywheel." That is Ryan's framework, not Marcela's.
- Short paragraphs. Line breaks between every paragraph.
- First person. "I," "we," "you." Never third person about herself.
- No client names. Use "a business owner I worked with" or "a founder."

**Signature phrases (use where natural):**
- "Let's cut through the noise..."
- "What actually moves the needle..."
- "Your time has a price tag."
- "Letting go isn't weakness. It's leadership."

---

## Post Format

```
[HOOK — 1 line. Bold statement, question, or pattern interrupt. No em dashes.]

[BODY — 3-5 short paragraphs. 2-3 sentences each. Line break between every paragraph.]

[ENGAGEMENT — Direct question to the reader. Always ends with a ?]

[HASHTAGS — 3-5 max. Relevant only.]
```

---

## Image Template Rotation

One image per post. Generate using AI image generation with the corresponding reference image loaded.

Reference images: `/home/ubuntu/repos/ai-manager-stack/assets/linkedin-images/marcela-w1-w2/`

| Day | Template | Reference File | Visual Style |
| :--- | :--- | :--- | :--- |
| Monday | T1: Whiteboard | `post-01-whiteboard.png` | Modern office, aluminum-framed whiteboard on wheels, marker-written headline, flow diagram below. Bright, professional. |
| Tuesday | T2: Newspaper | `post-02-newspaper.png` | B&W photo of folded newspaper on wooden desk, glasses and coffee beside it. Bold serif headline, subheadline, bullet list in a box. |
| Wednesday | T3: Chalkboard | `post-03-chalkboard.png` | Wooden-framed green classroom chalkboard, natural window light, student desks visible. White chalk handwriting. Headline at top, two-column comparison below. |
| Thursday | T4: Open Book | `post-04-openbook.png` | Open book on worn wooden table, coffee and glasses nearby. Typewriter font on cream pages. Left page = quote. Right page = numbered list of 5 items. |
| Friday | T5: Billboard | `post-05-billboard.png` | Highway billboard at dusk, traffic below, industrial skyline. All-caps bold white sans-serif, very large. Small italic subtext below. Bold, cinematic. |

**Image spec:** 16:9 landscape aspect ratio. All text legible at thumbnail size.

**Generation method:** Load the reference PNG as a visual reference in the image generation tool. Swap in the current post's headline and key content. Match the scene, lighting, and text style exactly.

---

## Virality Check (Run on Every Post Before Compiling)

Every post must pass at least one test:

1. **Scroll-Stop Test:** Does the first line make someone stop scrolling? If not, rewrite the hook.
2. **"I Needed This" Test:** Would a small business owner feel this was written for them?
3. **Share Test:** Would someone tag another founder in the comments?
4. **Save Test:** Would someone save this to come back to later?
5. **Comment Trigger:** Does the closing question make someone want to answer?

---

## Google Doc Posting Guide

**Drive folder:** `System-Wide-Context-Pool/content-drafts/marcela-weekly-digests/`
**Shared Drive ID:** `0AK8dAs_XgfnNUk9PVA`
**Naming convention:** `Marcela_PostingGuide_Week{N}_{YYYY-MM-DD}`

Every gws command must include `"driveId": "0AK8dAs_XgfnNUk9PVA"` and `"supportsAllDrives": true`.

Each post entry in the Doc includes:
1. Day and date
2. Pillar and theme
3. Full post text (ready to copy-paste)
4. Image (embedded or linked)
5. Virality note (one sentence on why this post has engagement potential)
6. Hashtags

After creating the Doc, deliver the link to Ryan. Task ends there.

---

## Pre-Delivery Guardrails Checklist

Before delivering the Google Doc, confirm every item:

- No em dashes anywhere in any post
- No "Founders Flywheel" reference
- No client names
- No internal Drive links or repo URLs in post copy
- No technical AI jargon
- No unprovable superlatives
- Every post ends with a question
- Every post has 3-5 hashtags
- Every image is 16:9 landscape
- Google Doc saved to the correct Drive folder
- Google Doc link delivered to Ryan

---

## Context to Load at Start of Every Run

Run the daily context pull first:

```bash
bash /home/ubuntu/skills/scarlett-context-pull/scripts/scarlett_context_pull.sh
```

Also read before generating if not already in context:
- `/home/ubuntu/skills/rpg-social-engine/SCARLETT_MARCELA_INSTRUCTIONS.md`
- `/home/ubuntu/skills/scarlett-drive-guardrail/SKILL.md`
