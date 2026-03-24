---
name: scratchoff-coupon-page
description: Build an interactive scratch-off coupon landing page for any client or brand. The page mimics a lottery scratch ticket — users scratch a silver coating with finger (mobile) or mouse (desktop) to reveal a discount code. On full reveal, confetti bursts and a claim CTA link appears. Use when a client needs a promotional discount landing page, a scratch-to-reveal coupon, or an interactive coupon experience for any product or service.
---

# Scratch-Off Coupon Landing Page Skill

Builds a fully functional, mobile-first scratch-off coupon page using React + Tailwind (web-static scaffold). Delivered as a hosted Manus web project. Turnaround per client: ~30–60 minutes.

## Workflow

### 1. Gather Client Variables

Collect these before building (read `references/client-variables.md` for full list):

- **Company name** and **website URL**
- **Discount percent** (e.g. `18`) and **coupon code** (e.g. `LOGO18`)
- **One-line product description** (e.g. "custom logo tablecloths — cut, sewn & printed in the USA")
- **Brand color preference** (or use default carnival theme)
- **3 trust badges** relevant to their product/service

### 2. Initialize the Web Project

```
webdev_init_project  scaffold=web-static  name="{client-slug}-scratchoff"
```

### 3. Generate Background Image

Use `generate_image` to create a textured background matching the client's brand color. Prompt template:

> "A rich, deep [COLOR] background with subtle vintage texture. Faint diagonal crosshatch pattern like aged paper or fabric weave. Scattered tiny gold star shapes barely visible. Warm dramatic lighting from center. Vignette edges darker. No text, no people. Photorealistic texture quality."

Store the CDN URL as `BG_IMAGE` in `Home.tsx`.

### 4. Install Template Files

Copy these files from `templates/` into the project, then substitute all `{{VARIABLE}}` placeholders (see `references/client-variables.md`):

| Template File | Project Destination |
|---|---|
| `ScratchCard.tsx` | `client/src/components/ScratchCard.tsx` |
| `Confetti.tsx` | `client/src/components/Confetti.tsx` |
| `Home.tsx` | `client/src/pages/Home.tsx` |
| `index.css` | `client/src/index.css` |
| `index.html` | `client/index.html` |

Add Google Fonts to `index.html` (default: Playfair Display + Source Sans 3). For alternate themes, see `references/client-variables.md`.

Update `App.tsx` to use `defaultTheme="dark"` (the dark background requires dark theme).

### 5. Key Customization Points

**Coupon code** — update in two places:
- `ScratchCard.tsx` in the revealed layer (text displaying the code)
- `Home.tsx` in the post-reveal section

**Discount percent** — update in `Home.tsx` headline and CTA button text.

**Trust badges** — update the 3-item array in `Home.tsx` near the bottom.

**Colors** — edit CSS variables in `index.css` under `:root`. Use OKLCH format. See theme options in `references/client-variables.md`.

### 6. Scratch Mechanic — How It Works

- Canvas element sits on top of the revealed code layer (z-index: 2)
- `destination-out` composite operation erases coating as user drags
- Pixel sampling every stroke calculates scratch percentage
- At **60% scratched**, canvas clears fully and `onRevealed()` fires
- `Confetti.tsx` spawns 180 canvas particles in brand colors, auto-clears after 4.5s
- CTA animates in with `animate-slide-up` CSS keyframe

**Do not change** the `globalCompositeOperation` logic or the pixel sampling loop — these are fragile.

### 7. Validate & Deliver

```
webdev_save_checkpoint
```

Send the `manus-webdev://` URL to the client. Instruct them to click **Publish** in the Management UI to go live, or bind their custom domain in Settings → Domains.

## Upsell Options (mention to client)

- **Email capture before reveal** — gate the code behind an email field for list building
- **Countdown timer** — "Expires in 24 hours" urgency element above the card
- **Product image strip** — 3–4 product photos below the trust badges
- **Analytics** — Manus built-in UV/PV analytics available after publish

## Pricing Guidance (for RPG client delivery)

| Tier | Includes | Price Range |
|---|---|---|
| Basic | Page built + published, standard carnival theme | $300–$500 |
| Branded | Custom colors, custom bg image, trust badges | $500–$800 |
| Full Package | + Email capture + countdown timer + product strip | $800–$1,200 |
