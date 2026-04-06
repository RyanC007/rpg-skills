#!/usr/bin/env python3
"""
RPG llms.txt Generator
Usage: python crawl_and_generate.py <domain> [output_dir]
Example: python crawl_and_generate.py fitnessfloors.com ./output

Crawls a website's key pages via sitemap, extracts clean content,
and generates a spec-compliant llms.txt + supporting .md files.
"""

import sys
import os
import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; LLMBot/1.0)'}
MAX_PAGES = 40
MAX_TEXT_CHARS = 5000

# Page types to prioritise (matched against URL path)
PRIORITY_PATTERNS = [
    '/$', '/about', '/faq', '/contact', '/products', '/services',
    '/blog', '/case-stud', '/resources', '/pricing'
]


def fetch(url, timeout=12):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        return r
    except Exception as e:
        print(f"  FAIL {url}: {e}")
        return None


def clean_text(soup):
    for tag in soup(['nav', 'footer', 'script', 'style', 'header']):
        tag.decompose()
    text = soup.get_text(separator=' ', strip=True)
    return re.sub(r'\s+', ' ', text)[:MAX_TEXT_CHARS]


def get_sitemap_urls(domain):
    """Pull all page URLs from sitemap.xml, handling sitemap indexes."""
    urls = []
    sitemap_url = f"https://{domain}/sitemap.xml"
    r = fetch(sitemap_url)
    if not r or r.status_code != 200:
        print(f"  No sitemap found at {sitemap_url}")
        return urls

    def parse_sitemap(xml_text):
        found = []
        try:
            root = ET.fromstring(xml_text)
            ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            # Sitemap index
            for sitemap in root.findall('sm:sitemap', ns):
                loc = sitemap.find('sm:loc', ns)
                if loc is not None:
                    sub = fetch(loc.text)
                    if sub and sub.status_code == 200:
                        found.extend(parse_sitemap(sub.text))
            # Regular sitemap
            for url_el in root.findall('sm:url', ns):
                loc = url_el.find('sm:loc', ns)
                if loc is not None:
                    found.append(loc.text.strip())
        except Exception as e:
            print(f"  Sitemap parse error: {e}")
        return found

    urls = parse_sitemap(r.text)
    print(f"  Found {len(urls)} URLs in sitemap")
    return urls


def prioritise_urls(urls, domain):
    """Score and sort URLs by priority, return top MAX_PAGES."""
    base = f"https://{domain}"
    scored = []
    for url in urls:
        if not url.startswith(base):
            continue
        path = urlparse(url).path.rstrip('/')
        score = 0
        for pat in PRIORITY_PATTERNS:
            if re.search(pat, path):
                score += 1
        # Prefer shorter paths (top-level pages)
        depth = path.count('/')
        score -= depth * 0.1
        scored.append((score, url))
    scored.sort(key=lambda x: -x[0])
    return [u for _, u in scored[:MAX_PAGES]]


def scrape_page(url):
    """Scrape a single page and return structured data."""
    r = fetch(url)
    if not r or r.status_code != 200:
        return None
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find('title')
    h1 = soup.find('h1')
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    h2s = [h.get_text(strip=True) for h in soup.find_all('h2')][:8]
    return {
        'url': r.url,
        'title': title.text.strip() if title else '',
        'h1': h1.get_text(strip=True) if h1 else '',
        'h2s': h2s,
        'meta_desc': meta_desc.get('content', '') if meta_desc else '',
        'text': clean_text(soup),
    }


def url_to_md_filename(url, domain):
    """Convert a URL to a clean .md filename."""
    path = urlparse(url).path.strip('/')
    if not path:
        return 'index.md'
    slug = path.replace('/', '-').replace('_', '-')
    return f"{slug}.md"


def generate_llms_txt(domain, pages, output_dir):
    """Generate the root llms.txt index file."""
    # Separate pages into sections
    product_pages = []
    info_pages = []
    for p in pages:
        path = urlparse(p['url']).path.lower()
        filename = url_to_md_filename(p['url'], domain)
        title = p.get('h1') or p.get('title') or filename
        desc = p.get('meta_desc', '')
        entry = f"- [{title}]({filename})"
        if desc:
            # Truncate description to 100 chars
            short_desc = desc[:100].rstrip() + ('...' if len(desc) > 100 else '')
            entry += f": {short_desc}"
        if any(kw in path for kw in ['/product', '/service', '/floor', '/court', '/carpet', '/rubber', '/vinyl', '/wood']):
            product_pages.append(entry)
        else:
            info_pages.append(entry)

    # Build the file
    homepage = next((p for p in pages if urlparse(p['url']).path in ['', '/']), None)
    site_desc = homepage.get('meta_desc', '') if homepage else ''
    site_title = homepage.get('title', domain) if homepage else domain

    lines = [f"# {site_title}\n"]
    if site_desc:
        lines.append(f"> {site_desc}\n")
    lines.append(f"This file provides structured content for AI language models to understand {domain}.\n")

    if product_pages:
        lines.append("## Products & Services\n")
        lines.extend(product_pages)
        lines.append("")

    if info_pages:
        lines.append("## Company Information\n")
        lines.extend(info_pages)
        lines.append("")

    lines.append("## Optional\n")
    lines.append(f"- [Sitemap](https://{domain}/sitemap.xml): Full list of all indexed pages\n")

    content = "\n".join(lines)
    out_path = os.path.join(output_dir, 'llms.txt')
    with open(out_path, 'w') as f:
        f.write(content)
    print(f"  Written: {out_path}")


def generate_md_files(pages, domain, output_dir):
    """Generate one .md file per page."""
    for page in pages:
        filename = url_to_md_filename(page['url'], domain)
        title = page.get('h1') or page.get('title') or filename
        desc = page.get('meta_desc', '')
        h2s = page.get('h2s', [])
        text = page.get('text', '')

        lines = [f"# {title}\n"]
        if desc:
            lines.append(f"> {desc}\n")
        if h2s:
            lines.append("**Sections:** " + " | ".join(h2s) + "\n")
        lines.append(f"**Source:** {page['url']}\n")
        lines.append("---\n")
        lines.append(text + "\n")

        out_path = os.path.join(output_dir, filename)
        with open(out_path, 'w') as f:
            f.write("\n".join(lines))
    print(f"  Written {len(pages)} .md files")


def main():
    if len(sys.argv) < 2:
        print("Usage: python crawl_and_generate.py <domain> [output_dir]")
        sys.exit(1)

    domain = sys.argv[1].replace('https://', '').replace('http://', '').rstrip('/')
    output_dir = sys.argv[2] if len(sys.argv) > 2 else f"./{domain.replace('.', '_')}_llms"
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n=== RPG llms.txt Generator ===")
    print(f"Domain: {domain}")
    print(f"Output: {output_dir}\n")

    print("Step 1: Fetching sitemap URLs...")
    all_urls = get_sitemap_urls(domain)

    if not all_urls:
        print("  No sitemap URLs found. Falling back to homepage only.")
        all_urls = [f"https://{domain}/"]

    print(f"Step 2: Prioritising top {MAX_PAGES} pages...")
    priority_urls = prioritise_urls(all_urls, domain)
    print(f"  Selected {len(priority_urls)} pages")

    print("Step 3: Scraping pages...")
    pages = []
    for url in priority_urls:
        print(f"  Scraping: {url}")
        data = scrape_page(url)
        if data:
            pages.append(data)

    # Save raw data for debugging
    with open(os.path.join(output_dir, '_raw_data.json'), 'w') as f:
        json.dump(pages, f, indent=2)

    print(f"\nStep 4: Generating llms.txt...")
    generate_llms_txt(domain, pages, output_dir)

    print(f"Step 5: Generating .md files...")
    generate_md_files(pages, domain, output_dir)

    print(f"\n=== Done ===")
    print(f"Files saved to: {output_dir}")
    print(f"Upload llms.txt to: https://{domain}/llms.txt")
    print(f"Upload each .md file to mirror its source URL with .md appended.")


if __name__ == '__main__':
    main()
