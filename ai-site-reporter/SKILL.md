---
name: ai-site-reporter
description: Perform deep technical analysis of any website URL to identify its AI builder or CMS, determine site age, extract the full tech stack, and examine code patterns. Delivers a structured Markdown report. Use when asked to analyze, audit, or investigate any website, or when asked "what was this built with", "how old is this site", or "what tech stack does this use".
---

# AI Site Reporter

This skill conducts a comprehensive technical analysis of a given website URL, providing insights into its construction, age, and underlying technologies. It generates a detailed Markdown report covering builder detection, domain age, full tech stack, code patterns, SEO elements, and third-party integrations.

## Purpose

The primary purpose of the `ai-site-reporter` skill is to automate the in-depth technical reconnaissance of websites. It provides a structured and evidence-based report that helps in understanding a website's digital footprint, from its foundational technology to its integrated services.

## Key Features

-   **Builder/CMS Identification**: Detects the underlying AI builder or Content Management System (CMS) using various fingerprinting techniques.
-   **Site Age Determination**: Estimates the website's age by analyzing domain registration, SSL certificate dates, and Wayback Machine archives.
-   **Comprehensive Tech Stack Analysis**: Identifies frameworks, hosting providers, CDNs, fonts, analytics tools, and other integrations.
-   **Code Pattern Examination**: Scans HTML, CSS, JavaScript, meta tags, JSON-LD, `robots.txt`, and `sitemap.xml` for critical information.
-   **Structured Reporting**: Generates a well-organized Markdown report with an executive summary, detailed findings, and recommendations.
-   **Automated Archiving**: Automatically saves all generated reports to a designated Google Drive folder for permanent record-keeping.

## Workflow

The `ai-site-reporter` skill executes a multi-step process to gather and analyze website data:

### Step 1: Fetch Raw Data

Collect essential raw data from the target URL using `curl` and `openssl` commands. This includes:

-   **Full HTML** of the homepage (and optionally key sub-pages).
-   **HTTP response headers** to reveal server, CDN, and framework information.
-   **WHOIS / RDAP data** for domain registration details.
-   **SSL certificate** dates and issuer information.
-   **Wayback Machine CDX API** for historical snapshots.
-   **`robots.txt`** and **`sitemap.xml`** for SEO and site structure insights.

```bash
TARGET="https://DOMAIN.com"
DOMAIN="DOMAIN.com"

# HTML
curl -s -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  "$TARGET/" -o /tmp/site_homepage.html

# Headers
curl -s -I -L "$TARGET/" > /tmp/site_headers.txt

# RDAP domain info (works for .com/.net - adjust for other TLDs)
curl -s "https://rdap.verisign.com/com/v1/domain/$DOMAIN" > /tmp/site_rdap.json

# SSL cert
echo | timeout 10 openssl s_client -connect $DOMAIN:443 2>/dev/null | \
  openssl x509 -noout -dates -issuer -subject > /tmp/site_ssl.txt

# Wayback Machine
curl -s "http://web.archive.org/cdx/search/cdx?url=$DOMAIN&output=json&limit=5&fl=timestamp,original,statuscode" \
  > /tmp/site_wayback.json

# robots.txt and sitemap
curl -s "$TARGET/robots.txt" -o /tmp/site_robots.txt
curl -s "$TARGET/sitemap.xml" -o /tmp/site_sitemap.xml
```

### Step 2: Parse HTML for Fingerprints

Utilize the bundled Python script `analyze_site.py` to extract key signals from the collected HTML. This script identifies:

-   Generator meta tags.
-   HTML build comments.
-   Script source patterns.
-   CSS class patterns.
-   Font file references.
-   Analytics and tracking IDs.
-   External domains and integrations.
-   JSON-LD structured data.
-   Open Graph and Twitter card tags.

```bash
python3.11 /home/ubuntu/rpg-branded-agents/skills/ai-site-reporter/scripts/analyze_site.py /tmp/site_homepage.html
```

### Step 3: Identify the Builder / CMS

Cross-reference the extracted fingerprints with the lookup table in `references/builder_fingerprints.md` to identify the website's builder or CMS. Prioritize identification based on reliability:

1.  `meta name="generator"` tag.
2.  HTML comments (e.g., Vercel, Wix, Squarespace build IDs).
3.  Script source patterns (e.g., `/wp-content/`, `/_next/`).
4.  CSS class patterns (e.g., Tailwind, Bootstrap, Webflow).
5.  HTTP headers (e.g., `x-powered-by`, `x-wix-request-id`).
6.  Font combinations (e.g., Geist + Inter for Vercel/v0 stack).
7.  Deployment ID patterns (e.g., `dpl_` for Vercel).

```bash
cat /home/ubuntu/rpg-branded-agents/skills/ai-site-reporter/references/builder_fingerprints.md
```

### Step 4: Determine Site Age

Synthesize information from multiple sources to accurately determine the site's age:

| Source                      | Information Provided                               |
| :-------------------------- | :------------------------------------------------- |
| RDAP registration date      | When the domain was initially purchased            |
| SSL cert `notBefore` date   | When the site first went live with HTTPS           |
| Wayback Machine snapshot    | Earliest public archive capture                    |
| Sitemap `lastmod` dates     | Most recent content updates                        |

### Step 5: Compile the Report

Generate a comprehensive Markdown report using the `templates/report_template.md` as a base. The report must include the following sections:

1.  **Executive Summary**: A table summarizing key findings.
2.  **AI Builder / CMS Identification**: Detailed evidence for the identified builder/CMS.
3.  **Site Age and History**: A breakdown of how the site's age was determined.
4.  **Technology Stack Deep Dive**: A table listing all identified technologies.
5.  **Code and SEO Examination**: Analysis of code patterns and SEO elements.
6.  **Third-Party Integrations**: List of integrated external services.
7.  **Recommendations**: Actionable suggestions based on the analysis.

Save the final report to `/tmp/site_analysis_DOMAIN.md`.

### Step 6: File the Report to Google Drive

**Mandatory Step**: Upload the generated report to the designated Google Drive folder `Scarlett-System-Files/Reports/` for permanent archiving. This ensures all web analysis reports are centrally stored.

```bash
# Save report locally first
REPORT_FILE="/tmp/site_analysis_${DOMAIN}.md"

# Upload to Google Drive
rclone copy "$REPORT_FILE" \
  "manus_google_drive:Scarlett-System-Files/Reports" \
  --config /home/ubuntu/.gdrive-rclone.ini

# Confirm it landed
rclone ls "manus_google_drive:Scarlett-System-Files/Reports" \
  --config /home/ubuntu/.gdrive-rclone.ini | grep "$DOMAIN"
```

### Step 7: Deliver

Attach the Markdown report file to the final message to the user. Include a brief inline summary of the top 3 findings and confirm that the report has been successfully filed to Google Drive.

## Quick Fingerprint Reference

| Signal                                    | Builder / Platform                 |
| :---------------------------------------- | :--------------------------------- |
| `meta generator="v0.app"` + `dpl_` IDs    | Vercel v0.app (AI builder)         |
| `meta generator="Webflow"`                | Webflow                            |
| `meta generator="Framer"`                 | Framer                             |
| `wp-content/` in script paths             | WordPress                          |
| `_gatsby/` paths                          | Gatsby                             |
| `/_nuxt/` paths                           | Nuxt.js                            |
| `x-wix-request-id` header                 | Wix                                |
| `x-squarespace-*` headers                 | Squarespace                        |
| `shopify.com` in scripts                  | Shopify                            |
| `__NEXT_DATA__` script tag                | Next.js                            |
| `turbopack-*.js`                          | Next.js + Turbopack (Vercel)       |
| Geist + Inter fonts                       | Vercel ecosystem                   |
| Radix UI CSS vars + shadcn vars           | shadcn/ui component library        |
| `lucide lucide-*` classes                 | Lucide React icons                 |
| `<!--[A-Z0-9]{20}-->` HTML comment         | v0.app (Vercel) build ID           |
| `server: Vercel` HTTP header              | Hosted on Vercel                   |

## Notes

-   Always run `analyze_site.py` before drawing conclusions. Do not guess based on visual appearance alone.
-   If the site uses a custom domain on Vercel, the `server: Vercel` header is the most reliable hosting indicator.
-   IDPixel (`cdn.idpixel.app`) is a B2B visitor identification tool, common in outbound-focused sales sites.
-   Termly (`app.termly.io`) is an automated privacy policy generator, common in sites built quickly with AI tools.
-   Cal.com links indicate the site owner uses Cal.com for meeting scheduling rather than Calendly.
-   The Wayback Machine CDX API returns an empty array for very new sites (under 2-3 months old). This itself is a signal of recency.
-   Font identification: download woff2 files and use `fonttools` (`sudo pip3 install fonttools`) to extract the font family name from the binary.
