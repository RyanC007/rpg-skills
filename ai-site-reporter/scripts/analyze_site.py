#!/usr/bin/env python3.11
"""
analyze_site.py - Core HTML analysis script for the ai-site-reporter skill.
Usage: python3.11 analyze_site.py <path_to_homepage.html>
"""

import sys
import re
import json
from bs4 import BeautifulSoup


def analyze(html_path):
    with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    print("=" * 60)
    print("AI SITE REPORTER - HTML ANALYSIS")
    print("=" * 60)

    # --- TITLE ---
    title = soup.title.string.strip() if soup.title else "No title"
    print(f"\n[TITLE]\n{title}")

    # --- META TAGS ---
    metas = {m.get('name', m.get('property', '')): m.get('content', '') for m in soup.find_all('meta') if m.get('content')}
    print(f"\n[META DESCRIPTION]\n{metas.get('description', 'Not found')}")
    print(f"\n[GENERATOR META]\n{metas.get('generator', 'Not found')}")

    # --- HTML COMMENT (build ID) ---
    comments = re.findall(r'<!--([^-]{5,50})-->', html)
    print(f"\n[HTML COMMENTS (build IDs)]\n{comments[:5]}")

    # --- OPEN GRAPH ---
    og = {k: v for k, v in metas.items() if k.startswith('og:') or k.startswith('twitter:')}
    print(f"\n[OPEN GRAPH / TWITTER CARDS]\n{'Present: ' + str(list(og.keys())) if og else 'MISSING - no og: or twitter: tags found'}")

    # --- SCRIPT SRCS ---
    script_srcs = [s.get('src', '') for s in soup.find_all('script') if s.get('src')]
    print(f"\n[SCRIPT SOURCES ({len(script_srcs)} total)]\n" + '\n'.join(script_srcs[:20]))

    # --- CSS LINKS ---
    css_links = [l.get('href', '') for l in soup.find_all('link') if 'stylesheet' in l.get('rel', [])]
    print(f"\n[CSS LINKS]\n" + '\n'.join(css_links[:10]))

    # --- FONT PRELOADS ---
    font_preloads = [l.get('href', '') for l in soup.find_all('link') if l.get('as') == 'font']
    print(f"\n[FONT PRELOADS]\n" + '\n'.join(font_preloads[:10]))

    # --- TECHNOLOGY FINGERPRINTS ---
    patterns = {
        'Next.js': r'__next|_next/static|next\.js|__NEXT_DATA__',
        'React': r'react|ReactDOM|__reactFiber',
        'Tailwind CSS': r'tailwind|tw-|className.*flex.*gap',
        'shadcn/ui': r'--background:|--foreground:|--primary:|--destructive:',
        'Radix UI': r'--radix-[a-z]',
        'Framer Motion': r'framer-motion|motion\.div',
        'Vercel': r'server.*Vercel|x-vercel|dpl=dpl_',
        'Turbopack': r'turbopack',
        'v0.app': r'v0\.app|v0\.dev',
        'WordPress': r'wp-content|wp-includes|wordpress',
        'Webflow': r'webflow\.com|wf-',
        'Framer': r'framer\.com|framer-web',
        'Wix': r'wix\.com|wixsite',
        'Squarespace': r'squarespace\.com|squarespace-cdn',
        'Shopify': r'shopify\.com|shopify-cdn',
        'Gatsby': r'_gatsby|gatsby-',
        'Nuxt.js': r'_nuxt|nuxt\.js',
        'Bootstrap': r'bootstrap\.min|col-md-|container-fluid',
        'Lucide Icons': r'lucide lucide-',
        'Heroicons': r'heroicon',
        'Font Awesome': r'font-awesome|fa-',
    }
    print("\n[TECHNOLOGY FINGERPRINTS]")
    for name, pattern in patterns.items():
        matches = re.findall(pattern, html, re.IGNORECASE)
        if matches:
            print(f"  FOUND: {name} ({len(matches)} matches)")

    # --- ANALYTICS & TRACKING ---
    print("\n[ANALYTICS & TRACKING]")
    analytics_patterns = {
        'Google Analytics 4': r'G-[A-Z0-9]{8,12}',
        'Google Tag Manager': r'GTM-[A-Z0-9]+',
        'Meta Pixel': r'fbq\(|facebook\.net/en_US/fbevents',
        'HubSpot': r'_hsq|hs-scripts\.com',
        'Hotjar': r'hotjar\.com|hjSiteSettings',
        'Mixpanel': r'mixpanel\.com|mixpanel\.init',
        'Segment': r'analytics\.js|segment\.com',
        'Plausible': r'plausible\.io',
        'PostHog': r'posthog\.com|posthog\.init',
        'Microsoft Clarity': r'clarity\.ms|clarityInit',
        'IDPixel': r'idpixel\.app',
        'Intercom': r'intercom\.io|intercomSettings',
        'Crisp': r'crisp\.chat|CRISP_WEBSITE_ID',
    }
    for name, pattern in analytics_patterns.items():
        found = re.findall(pattern, html, re.IGNORECASE)
        if found:
            ids = list(set(found))[:3]
            print(f"  FOUND: {name} - {ids}")

    # --- INTEGRATIONS ---
    print("\n[THIRD-PARTY INTEGRATIONS]")
    integration_patterns = {
        'Cal.com': r'cal\.com',
        'Calendly': r'calendly\.com',
        'Stripe': r'stripe\.com|js\.stripe\.com',
        'Paddle': r'paddle\.com',
        'HubSpot CRM': r'hubspot\.com',
        'Salesforce': r'salesforce\.com',
        'Typeform': r'typeform\.com',
        'Termly (Privacy Policy)': r'termly\.io',
        'Cloudflare': r'cloudflare\.com|__cf_bm',
        'AWS CloudFront': r'cloudfront\.net',
        'Zendesk': r'zendesk\.com',
    }
    for name, pattern in integration_patterns.items():
        found = re.findall(pattern, html, re.IGNORECASE)
        if found:
            print(f"  FOUND: {name}")

    # --- EXTERNAL DOMAINS ---
    ext_domains = list(set(re.findall(r'https?://([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', html)))
    print(f"\n[EXTERNAL DOMAINS ({len(ext_domains)} unique)]")
    for d in sorted(ext_domains)[:30]:
        print(f"  {d}")

    # --- JSON-LD STRUCTURED DATA ---
    jsonld_scripts = soup.find_all('script', type='application/ld+json')
    print(f"\n[JSON-LD STRUCTURED DATA]\n{len(jsonld_scripts)} block(s) found")
    for s in jsonld_scripts[:3]:
        try:
            data = json.loads(s.string)
            print(f"  Type: {data.get('@type', 'unknown')}")
        except Exception:
            pass

    # --- SITEMAP PAGES ---
    print("\n[NOTE] Run separately: curl sitemap.xml and robots.txt for page inventory")
    print("\n" + "=" * 60)
    print("Analysis complete.")
    print("=" * 60)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3.11 analyze_site.py <path_to_homepage.html>")
        sys.exit(1)
    analyze(sys.argv[1])
