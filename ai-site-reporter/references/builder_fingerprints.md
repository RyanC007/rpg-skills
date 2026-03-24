# Builder & CMS Fingerprint Reference

A comprehensive lookup table for identifying website builders, CMS platforms, and hosting environments from code signals.

## AI-Powered Builders

| Builder | Primary Signal | Secondary Signals |
| :--- | :--- | :--- |
| **v0.app (Vercel)** | `meta generator="v0.app"` | `<!--[A-Z0-9]{20}-->` HTML comment, `dpl_` deployment IDs, Geist + Inter fonts, Next.js + Turbopack |
| **Framer** | `meta generator="Framer"` | `framer.com` in scripts, `framer-web` class patterns |
| **Durable** | `meta generator="Durable"` | `durable.co` in scripts |
| **Wix ADI** | `x-wix-request-id` header | `wix.com` in scripts, `wixsite.com` domain |
| **Squarespace** | `x-squarespace-*` headers | `squarespace-cdn.com` in scripts |

## Traditional CMS Platforms

| CMS | Primary Signal | Secondary Signals |
| :--- | :--- | :--- |
| **WordPress** | `/wp-content/` or `/wp-includes/` in scripts | `meta generator="WordPress"`, `wp-json` API endpoint |
| **Shopify** | `shopify.com` or `shopify-cdn.com` in scripts | `Shopify.theme` in JS, `myshopify.com` references |
| **Wix** | `x-wix-request-id` HTTP header | `wix.com` CDN, `wixstatic.com` images |
| **Squarespace** | `x-squarespace-*` HTTP headers | `squarespace-cdn.com` assets |
| **Webflow** | `meta generator="Webflow"` | `webflow.com` in scripts, `wf-` CSS classes |
| **Ghost** | `meta generator="Ghost"` | `ghost.io` in scripts, `content/themes/` paths |
| **Drupal** | `meta generator="Drupal"` | `/sites/default/files/` paths |
| **Joomla** | `meta generator="Joomla"` | `/components/com_` paths |

## JavaScript Frameworks

| Framework | Primary Signal | Secondary Signals |
| :--- | :--- | :--- |
| **Next.js** | `__NEXT_DATA__` script tag | `/_next/static/` paths, `x-nextjs-*` headers |
| **Nuxt.js** | `/_nuxt/` paths | `__NUXT__` global variable |
| **Gatsby** | `/_gatsby/` paths | `gatsby-*` class names |
| **Remix** | `__remixContext` | `_data` query params |
| **SvelteKit** | `__sveltekit_*` | `/_app/` paths |
| **Astro** | `astro-*` attributes | `/_astro/` paths |
| **Angular** | `ng-version` attribute | `main.*.js` with Angular patterns |
| **Vue.js** | `__vue_*` | `v-bind`, `v-if` attributes |

## Hosting & CDN

| Platform | Primary Signal |
| :--- | :--- |
| **Vercel** | `server: Vercel` HTTP header, `x-vercel-cache` header |
| **Netlify** | `server: Netlify` header, `x-nf-request-id` header |
| **Cloudflare Pages** | `cf-cache-status` header, `__cf_bm` cookie |
| **AWS Amplify** | `x-amz-*` headers, `amplifyapp.com` domain |
| **GitHub Pages** | `server: GitHub.com` header |
| **Render** | `x-render-origin-server` header |
| **Railway** | `railway.app` domain |
| **Fly.io** | `fly-request-id` header |

## UI Component Libraries

| Library | Signal |
| :--- | :--- |
| **shadcn/ui** | CSS vars: `--background`, `--foreground`, `--primary`, `--destructive`, `--muted` |
| **Radix UI** | CSS vars: `--radix-accordion-content-height`, `--radix-select-trigger-width`, etc. |
| **Material UI** | `MuiButton`, `MuiTypography` class prefixes |
| **Chakra UI** | `chakra-*` class prefixes |
| **Ant Design** | `ant-*` class prefixes |
| **Bootstrap** | `col-md-`, `container-fluid`, `btn-primary` class patterns |
| **Tailwind CSS** | Utility classes: `flex`, `grid`, `text-neutral-*`, `bg-amber-*`, `rounded-*` |

## Icon Libraries

| Library | Signal |
| :--- | :--- |
| **Lucide React** | `lucide lucide-[icon-name]` CSS classes |
| **Heroicons** | `heroicon-*` classes |
| **Font Awesome** | `fa-*` classes, `font-awesome` in scripts |
| **Feather Icons** | `feather feather-*` classes |
| **Phosphor Icons** | `ph-*` classes |

## Font Combinations as Stack Indicators

| Font Combination | Likely Stack |
| :--- | :--- |
| Geist + Inter | Vercel ecosystem (v0.app, Next.js) |
| Inter + Geist Mono | Vercel ecosystem |
| DM Sans + DM Mono | Modern SaaS (often Framer or custom) |
| Satoshi + Cabinet Grotesk | Webflow or custom |
| Poppins + Roboto | WordPress or Webflow |
| Helvetica Neue + system-ui | Squarespace |

## Analytics & Tracking Quick Reference

| Tool | Signal |
| :--- | :--- |
| Google Analytics 4 | `G-XXXXXXXXXX` ID |
| Google Tag Manager | `GTM-XXXXXXX` ID |
| Meta Pixel | `fbq(` or `facebook.net/en_US/fbevents.js` |
| HubSpot | `_hsq` or `hs-scripts.com` |
| Hotjar | `hjSiteSettings` or `hotjar.com` |
| Mixpanel | `mixpanel.init` |
| Segment | `analytics.js` |
| Plausible | `plausible.io` |
| PostHog | `posthog.init` |
| Microsoft Clarity | `clarity.ms` |
| IDPixel | `cdn.idpixel.app` (B2B visitor ID, common in sales-focused sites) |
| Intercom | `intercomSettings` or `intercom.io` |
| Crisp | `CRISP_WEBSITE_ID` or `crisp.chat` |
