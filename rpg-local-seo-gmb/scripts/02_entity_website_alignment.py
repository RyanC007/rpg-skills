#!/usr/bin/env python3
"""
RPG Local SEO GMB — Step 2: Entity & Website Alignment
Crawls the client's website, extracts entities (services, locations, keywords),
then cross-references against competitor GBP categories to find gaps and
alignment opportunities for local SEO.
"""

import os
import sys
import json
import re
import requests
import argparse
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from collections import Counter


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; RPG-LocalSEO-Bot/1.0; +https://readyplangrow.com)"
}


# ─── Website Crawling ────────────────────────────────────────────────────────

def fetch_page(url: str) -> BeautifulSoup | None:
    """Fetch and parse a single page."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        print(f"  [WARN] Could not fetch {url}: {e}")
        return None


def discover_internal_links(base_url: str, soup: BeautifulSoup) -> list:
    """Find all internal links from a page."""
    base_domain = urlparse(base_url).netloc
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        full = urljoin(base_url, href)
        parsed = urlparse(full)
        if parsed.netloc == base_domain and parsed.scheme in ("http", "https"):
            clean = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if clean not in links:
                links.append(clean)
    return links


def crawl_website(base_url: str, max_pages: int = 30) -> list:
    """Crawl up to max_pages of a website and return page data."""
    visited = set()
    queue = [base_url.rstrip("/")]
    pages = []

    while queue and len(visited) < max_pages:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)

        soup = fetch_page(url)
        if not soup:
            continue

        # Extract page data
        title = soup.find("title")
        h1 = soup.find("h1")
        h2s = [h.get_text(strip=True) for h in soup.find_all("h2")]
        meta_desc = soup.find("meta", attrs={"name": "description"})
        body_text = soup.get_text(separator=" ", strip=True)[:3000]

        page_data = {
            "url": url,
            "title": title.get_text(strip=True) if title else "",
            "h1": h1.get_text(strip=True) if h1 else "",
            "h2s": h2s[:10],
            "meta_description": meta_desc["content"] if meta_desc and meta_desc.get("content") else "",
            "body_preview": body_text,
            "word_count": len(body_text.split()),
            "has_nap": check_nap_presence(body_text),
            "schema_types": extract_schema_types(soup),
        }
        pages.append(page_data)
        print(f"  Crawled: {url} ({page_data['word_count']} words)")

        # Queue internal links
        new_links = discover_internal_links(url, soup)
        for link in new_links:
            if link not in visited and link not in queue:
                queue.append(link)

    return pages


def check_nap_presence(text: str) -> bool:
    """Check if page likely contains NAP (Name, Address, Phone)."""
    phone_pattern = r"\(?\d{3}\)?[\s\-\.]\d{3}[\s\-\.]\d{4}"
    address_signals = ["street", "ave", "blvd", "rd", "suite", "st.", "drive", "lane"]
    has_phone = bool(re.search(phone_pattern, text, re.IGNORECASE))
    has_address = any(sig in text.lower() for sig in address_signals)
    return has_phone and has_address


def extract_schema_types(soup: BeautifulSoup) -> list:
    """Extract schema.org types from JSON-LD or itemtype attributes."""
    schema_types = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "{}")
            if isinstance(data, dict):
                t = data.get("@type", "")
                if t:
                    schema_types.append(t if isinstance(t, str) else str(t))
            elif isinstance(data, list):
                for item in data:
                    t = item.get("@type", "")
                    if t:
                        schema_types.append(t if isinstance(t, str) else str(t))
        except Exception:
            pass
    return list(set(schema_types))


# ─── Entity Extraction ───────────────────────────────────────────────────────

# Common service/entity keywords for local businesses
SERVICE_SIGNALS = [
    "repair", "installation", "replacement", "service", "maintenance",
    "inspection", "cleaning", "remodel", "renovation", "construction",
    "emergency", "commercial", "residential", "certified", "licensed",
    "insured", "free estimate", "same day", "24/7", "consultation",
]

GEO_SIGNALS = [
    "serving", "near", "in ", "area", "county", "city", "town",
    "neighborhood", "zip", "metro", "region", "local",
]


def extract_entities_from_pages(pages: list) -> dict:
    """Extract service entities, geo signals, and keyword themes from crawled pages."""
    all_text = " ".join([
        p["title"] + " " + p["h1"] + " " + " ".join(p["h2s"]) + " " + p["meta_description"]
        for p in pages
    ]).lower()

    # Service pages detection
    service_pages = [
        p for p in pages
        if any(sig in p["url"].lower() for sig in ["service", "repair", "install", "clean", "remodel"])
        or any(sig in (p["h1"] or "").lower() for sig in SERVICE_SIGNALS)
    ]

    # Location pages detection
    location_pages = [
        p for p in pages
        if any(sig in p["url"].lower() for sig in ["location", "area", "city", "county", "serving"])
        or any(sig in (p["h1"] or "").lower() for sig in GEO_SIGNALS)
    ]

    # Word frequency analysis on headings
    heading_words = re.findall(r"\b[a-z]{4,}\b", all_text)
    word_freq = Counter(heading_words)
    # Remove common stop words
    stop_words = {"that", "this", "with", "your", "have", "from", "they", "will",
                  "been", "more", "also", "when", "what", "which", "their", "about",
                  "make", "into", "than", "then", "some", "each", "such", "over",
                  "only", "both", "very", "just", "like", "time", "year", "need"}
    top_keywords = [(w, c) for w, c in word_freq.most_common(50) if w not in stop_words]

    # Schema audit
    all_schemas = []
    for p in pages:
        all_schemas.extend(p.get("schema_types", []))
    schema_summary = dict(Counter(all_schemas))

    # NAP consistency check
    pages_with_nap = [p["url"] for p in pages if p.get("has_nap")]

    return {
        "total_pages_crawled": len(pages),
        "service_pages": [{"url": p["url"], "h1": p["h1"], "title": p["title"]} for p in service_pages],
        "location_pages": [{"url": p["url"], "h1": p["h1"], "title": p["title"]} for p in location_pages],
        "top_keywords": top_keywords[:30],
        "schema_types_found": schema_summary,
        "pages_with_nap": pages_with_nap,
        "nap_coverage_pct": round(len(pages_with_nap) / len(pages) * 100, 1) if pages else 0,
    }


# ─── Gap Analysis ────────────────────────────────────────────────────────────

def run_gap_analysis(entities: dict, competitor_data: dict, client_gbp_categories: list) -> dict:
    """
    Compare client website entities + GBP categories against competitors
    to identify ranking gaps and enhancement opportunities.
    """
    competitor_categories = competitor_data.get("category_analysis", {}).get("top_10", {})
    client_service_keywords = [kw for kw, _ in entities.get("top_keywords", [])]

    # Categories competitors use that client GBP doesn't have
    missing_categories = [
        cat for cat in competitor_categories
        if cat.lower() not in [c.lower() for c in client_gbp_categories]
    ]

    # Service topics competitors rank for that client website doesn't cover
    competitor_names = [c["name"] for c in competitor_data.get("all_competitors", [])[:5]]

    # Website gaps: service pages missing
    has_service_pages = len(entities.get("service_pages", [])) > 0
    has_location_pages = len(entities.get("location_pages", [])) > 0
    has_schema = len(entities.get("schema_types_found", {})) > 0
    has_local_business_schema = "LocalBusiness" in entities.get("schema_types_found", {}) or \
                                 any("Business" in s for s in entities.get("schema_types_found", {}).keys())

    nap_coverage = entities.get("nap_coverage_pct", 0)

    gaps = []
    opportunities = []

    # Gap: No dedicated service pages
    if not has_service_pages:
        gaps.append({
            "type": "CRITICAL",
            "area": "Website Structure",
            "issue": "No dedicated service pages detected",
            "fix": "Create individual pages for each core service with keyword-optimized titles and H1s",
        })

    # Gap: No location/city pages
    if not has_location_pages:
        gaps.append({
            "type": "HIGH",
            "area": "Geographic Targeting",
            "issue": "No city or service-area landing pages found",
            "fix": "Build city-specific landing pages for each service area (e.g., '[Service] in [City], [State]')",
        })

    # Gap: Missing schema
    if not has_schema:
        gaps.append({
            "type": "HIGH",
            "area": "Technical SEO",
            "issue": "No structured data (schema.org) detected on website",
            "fix": "Implement LocalBusiness schema with NAP, hours, service areas, and geo coordinates",
        })
    elif not has_local_business_schema:
        gaps.append({
            "type": "MEDIUM",
            "area": "Technical SEO",
            "issue": "Schema present but no LocalBusiness schema type found",
            "fix": "Add LocalBusiness (or specific subtype) JSON-LD schema to homepage and service pages",
        })

    # Gap: Poor NAP coverage
    if nap_coverage < 80:
        gaps.append({
            "type": "HIGH",
            "area": "NAP Consistency",
            "issue": f"NAP only found on {nap_coverage}% of pages",
            "fix": "Add consistent NAP to the footer of every page — name, address, and phone must match GBP exactly",
        })

    # GBP category gaps
    for cat in missing_categories[:5]:
        opportunities.append({
            "type": "GBP Enhancement",
            "area": "Category Optimization",
            "opportunity": f"Add '{cat}' as a secondary GBP category",
            "rationale": f"Used by {competitor_categories.get(cat, 0)} competitors in the local pack",
        })

    # Review gap
    review_data = competitor_data.get("review_landscape", {})
    to_beat = review_data.get("to_beat_reviews", 0)
    if to_beat > 0:
        opportunities.append({
            "type": "Reputation",
            "area": "Review Volume",
            "opportunity": f"Target {to_beat} reviews to match the local leader",
            "rationale": f"Current leader has {to_beat} reviews at {review_data.get('to_beat_rating', 0)} stars",
        })

    return {
        "critical_gaps": [g for g in gaps if g["type"] == "CRITICAL"],
        "high_priority_gaps": [g for g in gaps if g["type"] == "HIGH"],
        "medium_priority_gaps": [g for g in gaps if g["type"] == "MEDIUM"],
        "gbp_opportunities": opportunities,
        "missing_competitor_categories": missing_categories,
        "website_has_service_pages": has_service_pages,
        "website_has_location_pages": has_location_pages,
        "schema_coverage": entities.get("schema_types_found", {}),
        "nap_coverage_pct": nap_coverage,
    }


def run_entity_alignment(website_url: str, competitor_json: str,
                          client_gbp_categories: list, output_dir: str = ".") -> str:
    """Full entity alignment pipeline."""
    print(f"\n[1/3] Crawling website: {website_url}")
    pages = crawl_website(website_url, max_pages=30)
    print(f"      Crawled {len(pages)} pages.")

    print(f"[2/3] Extracting entities and signals...")
    entities = extract_entities_from_pages(pages)

    print(f"[3/3] Running gap analysis against competitor data...")
    with open(competitor_json, "r") as f:
        competitor_data = json.load(f)

    gaps = run_gap_analysis(entities, competitor_data, client_gbp_categories)

    report = {
        "meta": {
            "website_url": website_url,
            "pages_crawled": len(pages),
            "client_gbp_categories": client_gbp_categories,
        },
        "website_entities": entities,
        "page_inventory": [
            {"url": p["url"], "title": p["title"], "h1": p["h1"],
             "word_count": p["word_count"], "has_nap": p["has_nap"],
             "schema": p["schema_types"]}
            for p in pages
        ],
        "gap_analysis": gaps,
    }

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "02_entity_alignment.json")
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n✅ Entity alignment complete. Output: {out_path}")
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RPG Local SEO — Entity & Website Alignment")
    parser.add_argument("--url", required=True, help="Client website URL")
    parser.add_argument("--competitor-json", required=True, help="Path to 01_competitor_research.json")
    parser.add_argument("--gbp-categories", default="", help="Comma-separated client GBP categories")
    parser.add_argument("--output", default="./rpg_local_seo_output", help="Output directory")
    args = parser.parse_args()

    categories = [c.strip() for c in args.gbp_categories.split(",") if c.strip()]
    run_entity_alignment(args.url, args.competitor_json, categories, args.output)
