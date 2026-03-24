# Client Customization Variables

These are the only values that change per client. Locate and replace all occurrences in the template files.

## Required Substitutions

| Variable | Where Used | Example |
|---|---|---|
| `{{COMPANY_NAME}}` | Home.tsx, index.html | `LogoClothz` |
| `{{WEBSITE_URL}}` | Home.tsx (CTA href) | `https://logoclothz.com` |
| `{{DOMAIN}}` | Home.tsx (fine print, footer) | `logoclothz.com` |
| `{{DISCOUNT_PERCENT}}` | Home.tsx (headline, CTA) | `18` |
| `{{COUPON_CODE}}` | Home.tsx, ScratchCard.tsx | `LOGO18` |
| `{{PRODUCT_LINE}}` | Home.tsx (subheadline) | `custom logo tablecloths — cut, sewn & printed in the USA` |
| `{{BG_IMAGE_URL}}` | Home.tsx (BG_IMAGE const) | CDN URL from generate_image |
| `{{PAGE_TITLE}}` | index.html `<title>` | `LogoClothz — Scratch & Save 18% Off` |
| `{{META_DESCRIPTION}}` | index.html meta | One-line description of the offer |

## Optional Substitutions (Design)

| Variable | Where Used | Default |
|---|---|---|
| `{{PRIMARY_COLOR}}` | index.css `--background` | Deep crimson `oklch(0.22 0.08 22)` |
| `{{ACCENT_COLOR}}` | index.css `--primary` | Aged gold `oklch(0.72 0.14 75)` |
| `{{TRUST_BADGE_1}}` | Home.tsx trust signals | `🇺🇸 Cut, Sewn & Printed in the USA` |
| `{{TRUST_BADGE_2}}` | Home.tsx trust signals | `🎨 Full Custom Logo Print` |
| `{{TRUST_BADGE_3}}` | Home.tsx trust signals | `🚚 Fast Turnaround` |
| `{{FINE_PRINT}}` | Home.tsx fine print | `One-time use · Valid on [domain] · While supplies last` |

## Design Theme Options

The default theme is **Retro Carnival / Lottery Ticket** (crimson + gold).

For other brand personalities, swap the CSS variables in `index.css`:

| Theme | `--background` | `--primary` (accent) | Font Pair |
|---|---|---|---|
| Carnival (default) | `oklch(0.22 0.08 22)` crimson | `oklch(0.72 0.14 75)` gold | Playfair Display + Source Sans 3 |
| Corporate Navy | `oklch(0.18 0.06 250)` navy | `oklch(0.65 0.15 200)` electric blue | DM Sans Bold + DM Sans |
| Luxury Black | `oklch(0.12 0.01 0)` near-black | `oklch(0.68 0.12 80)` champagne gold | Cormorant Garamond + Jost |
| Forest Green | `oklch(0.20 0.07 145)` dark green | `oklch(0.75 0.12 85)` warm gold | Raleway + Open Sans |
