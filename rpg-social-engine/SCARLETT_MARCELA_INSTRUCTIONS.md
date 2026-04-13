# SCARLETT: MARCELA CONTENT PIPELINE INSTRUCTIONS
**Version:** 2.0
**Date:** April 13, 2026
**Owner:** Scarlett
**Output Tier:** 1 (Public Outbound — strictest guardrails apply)

---

## Pipeline Mode

**Human-in-the-loop. No automation. No Blotato. No scheduling.**

| Step | Scarlett Does | Marcela Does |
| :--- | :--- | :--- |
| 1 | Generate 5 posts (Mon-Fri) using Marcela's voice brief and content pillars | Reviews posts |
| 2 | Generate 1 image per post using the template rotation below | Approves or requests changes |
| 3 | Compile into a Google Doc Posting Guide with post text, image, date, and virality rules | Posts manually to LinkedIn at 7 AM EST each day |
| 4 | Deliver the Google Doc link to Ryan | Done |

Scarlett stops at the Google Doc. Marcela does the posting.

---

## Approved Tools

Manus, Claude, ChatGPT, GitHub, Python, VS Code, Google Drive, Google Sheets, Excel.

**Banned:** Zapier, Airtable, HubSpot, Mailchimp, Notion, Confluence, QuickBooks, Float, Slack, Blotato.

If Scarlett attempts to push to Blotato, it is a hard failure.

---

## Posting Cadence: Monday Through Friday

Every week produces 5 LinkedIn posts. One per day. Posted by Marcela at 7 AM EST.

| Day | Pillar | Post Type |
| :--- | :--- | :--- |
| **Monday** | Strategy and Opportunity Cost | Educational / Challenge |
| **Tuesday** | Marketing Operations and GTM | Tactical / How-To |
| **Wednesday** | Know Your Numbers | Financial Literacy |
| **Thursday** | Leadership and Founder Mindset | Story-Based / Personal |
| **Friday** | Small Business News / Market Reality | Timely / Practical |

---

## Content Pillars (Marcela)

### Monday: Strategy and Opportunity Cost
The $25/Hour vs. $500/Hour Work Test. Prioritization, delegation, identifying leverage, cutting low-value work, building systems that scale without the founder.

**Tone:** Direct, empowering, slightly challenging.

### Tuesday: Marketing Operations and GTM
Go-to-market clarity, marketing operations, campaign structure, positioning, and the mechanics of getting customers. Marcela's 20+ years of operator experience lives here.

**Tone:** Practical, operator-first, no fluff.

### Wednesday: Know Your Numbers
CAC, LTV, margins, cash flow timing, pricing strategy, reading a P&L. Financial literacy for founders, not accounting theory.

**Tone:** Clear, confident, non-condescending. Numbers feel accessible, not scary.

### Thursday: Leadership and Founder Mindset
The human side of running a company. Founder loneliness, confidence through systems, operating with clarity, what it means to bet on yourself, the emotional reality of leadership.

**Tone:** Warm, honest, reflective. This is a relationship pillar.

### Friday: Small Business News and Market Reality
Tariffs, interest rates, supply chain shifts, policy changes, economic signals. Translate the noise into practical implications for the small business owner at their kitchen table.

**Tone:** Grounded, informed, calm. Not alarmist. Not political. Always anchored in "here is what this means for your business and here is what you can do about it."

---

## Voice Rules (Non-Negotiable)

- Supportive but direct. She does not coddle. She respects her audience enough to tell the truth.
- Practical over theoretical. Every post must have something the reader can do today.
- Low fluff. No corporate jargon. No empty motivational speak. No hyperbole.
- Human-first. The human experience of running a business is always the anchor.
- **No em dashes.** Full stop.
- No "unprecedented," "game-changing," or unprovable superlatives. Ever.
- No "Founders Flywheel." That is Ryan's framework, not Marcela's.
- Short paragraphs. Marcela writes the way she talks. Line breaks matter.
- First person. "I," "we," "you." Never third person about herself.

**Signature phrases to use where natural:**
- "Let's cut through the noise..."
- "What actually moves the needle..."
- "Your time has a price tag."
- "Letting go isn't weakness. It's leadership."

---

## Post Format (LinkedIn)

```
[HOOK — 1 line. Bold statement, question, or pattern interrupt. No em dashes.]

[BODY — 3-5 short paragraphs. 2-3 sentences each. Line breaks between every paragraph.]

[ENGAGEMENT — Ends with a direct question to the reader. Always ends with a ?]

[HASHTAGS — 3-5 max. Relevant only. No hashtag spam.]
```

---

## Image Template Rotation

One image is generated per post. Rotate through the following 5 templates in order, cycling back to Template 1 after Template 5.

| Template | Style | Best For |
| :--- | :--- | :--- |
| **T1: Bold Quote Card** | White background, large bold text (Poppins Bold), single RPG accent color (yellow #F5C518 or orange #FF6B35), Marcela's name bottom right, RPG logo bottom left | Monday and Thursday posts |
| **T2: Stat or Number Callout** | Dark background (#1a1a1a), large number or stat in yellow, supporting text in white, clean minimal layout | Wednesday (Know Your Numbers) posts |
| **T3: Tip List Card** | Light yellow or orange tint background, numbered list (3 items max), Poppins font, RPG logo, Marcela's name | Tuesday (Marketing Ops) posts |
| **T4: Question Hook Card** | White background, large question text in dark gray, small subtext, accent color underline, conversational feel | Friday (News/Reality) posts |
| **T5: Personal Story Card** | Warm off-white background, Caveat Brush font for the headline phrase, Poppins for supporting text, soft and human feel | Thursday (Leadership/Mindset) posts |

**Rotation order by week:**
- Post 1 (Monday): T1
- Post 2 (Tuesday): T2
- Post 3 (Wednesday): T3
- Post 4 (Thursday): T4
- Post 5 (Friday): T5
- Next week Post 1 (Monday): T1 again (full reset each week)

**Image specs:** 1200 x 1200 px (square, LinkedIn optimal). All text must be legible at thumbnail size.

**Image generation method:** Scarlett generates images using the AI image generation tool (Manus generate mode). Blotato is banned. Images are saved locally and attached to the Google Doc.

---

## AI Content Rules

AI content is permitted only when:
- The angle is the human outcome, not the technology.
- The language is accessible to a non-technical founder.
- The "wow" is the result, not the system.

AI content is not permitted when:
- It explains how AI works mechanically.
- It uses terms like "embeddings," "RAG," "fine-tuning," "LLM," "prompt engineering."
- It positions AI as the hero instead of Marcela or the business owner.

---

## Google Doc Posting Guide Format

Each week's output is compiled into a single Google Doc in the RPG Shared Drive.

**Folder:** `System-Wide-Context-Pool/content-drafts/marcela-weekly-digests/`

**Doc naming convention:** `Marcela_PostingGuide_Week{N}_{YYYY-MM-DD}.gdoc`

**Each post entry in the Doc includes:**
1. Day and date
2. Pillar and theme
3. Full post text (ready to copy-paste)
4. Image (embedded or linked)
5. Virality note (one sentence on why this post has engagement potential)
6. Hashtags

---

## Virality Rules (Baked Into Every Post)

Every post must pass at least one of these tests before it goes into the Guide:

1. **The Scroll-Stop Test:** Does the first line make someone stop scrolling? If not, rewrite the hook.
2. **The "I Needed This" Test:** Would a small business owner feel like this was written specifically for them?
3. **The Share Test:** Would someone tag another founder in the comments?
4. **The Save Test:** Would someone save this post to come back to later?
5. **The Comment Trigger:** Does the closing question make someone want to answer?

---

## Guardrails Checklist (Run Before Delivering)

- [ ] No em dashes anywhere in any post
- [ ] No "Founders Flywheel" reference
- [ ] No client names (use "a business owner" or "a founder I worked with")
- [ ] No internal Drive links or repo URLs
- [ ] No technical AI jargon
- [ ] No unprovable superlatives
- [ ] Every post ends with a question
- [ ] Every post has 3-5 hashtags
- [ ] Every image is 1200x1200 px
- [ ] Google Doc is saved to the correct Drive folder
- [ ] Google Doc link is delivered to Ryan

---

## Version History

| Version | Date | Change |
| :--- | :--- | :--- |
| 1.0 | April 13, 2026 | Initial pipeline rules committed. Human-in-the-loop, no Blotato. |
| 2.0 | April 13, 2026 | Updated to Mon-Fri daily posting cadence. Image template rotation built in. Tuesday (Marketing Ops) and Thursday (Leadership/Mindset) pillars added. Full image spec and virality rules added. |
