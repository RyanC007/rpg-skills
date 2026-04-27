#!/usr/bin/env python3
"""
RPG Brand 360 Audit — SERP Data Collection Script
Collects real-time keyword rankings, local pack presence, competitor domains,
and Knowledge Panel presence for a target brand.

Usage:
    export SERP_API_KEY="your_key_here"
    python3 serp_audit.py --brand "Brand Name" --domain "example.com" \
        --keywords "keyword one, keyword two, keyword three"

Output:
    Prints a JSON summary to stdout.
    Saves full results to /tmp/serp_audit_results.json
"""

import argparse
import json
import os
import sys
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print("Error: 'requests' library not installed. Run: pip install requests")
    sys.exit(1)

SERPAPI_BASE = "https://serpapi.com/search.json"


def get_api_key():
    key = os.environ.get("SERP_API_KEY")
    if not key:
        print("ERROR: SERP_API_KEY environment variable is not set.")
        print("Set it with: export SERP_API_KEY='your_key_here'")
        sys.exit(1)
    return key


def extract_domain(url):
    """Extract the root domain from a URL."""
    try:
        parsed = urlparse(url if url.startswith("http") else "https://" + url)
        domain = parsed.netloc.replace("www.", "")
        return domain
    except Exception:
        return url


def search_google(query, api_key, num=20):
    """Run a standard Google SERP query and return the full result dict."""
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": num,
        "hl": "en",
        "gl": "us",
    }
    try:
        resp = requests.get(SERPAPI_BASE, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"  [WARN] SERP request failed for '{query}': {e}")
        return {}


def check_knowledge_panel(brand_name, api_key):
    """Check if a brand has a Google Knowledge Panel."""
    data = search_google(brand_name, api_key, num=10)
    kp = data.get("knowledge_graph", {})
    if kp:
        return {
            "present": True,
            "title": kp.get("title", ""),
            "type": kp.get("type", ""),
            "website": kp.get("website", ""),
        }
    return {"present": False}


def check_local_pack(keyword, brand_name, api_key):
    """Check if the brand appears in the Local Pack for a keyword."""
    data = search_google(keyword, api_key, num=10)
    local_results = data.get("local_results", [])
    for item in local_results:
        title = item.get("title", "")
        if brand_name.lower() in title.lower():
            return {
                "present": True,
                "position": item.get("position", "unknown"),
                "rating": item.get("rating"),
                "reviews": item.get("reviews"),
            }
    return {"present": False, "local_results_count": len(local_results)}


def run_keyword_audit(keywords, target_domain, api_key):
    """
    For each keyword, find the target domain's organic rank and
    collect competitor domains from the top 10 results.
    """
    rankings = {}
    competitor_frequency = {}

    for kw in keywords:
        kw = kw.strip()
        if not kw:
            continue

        print(f"  Checking keyword: '{kw}'")
        data = search_google(kw, api_key, num=20)
        organic = data.get("organic_results", [])

        rank = None
        for item in organic:
            link = item.get("link", "")
            item_domain = extract_domain(link)
            position = item.get("position", 0)

            # Check if this is the target domain
            if target_domain.lower() in item_domain.lower():
                rank = position
            else:
                # Count competitor frequency
                if item_domain and not item_domain.startswith("google"):
                    competitor_frequency[item_domain] = (
                        competitor_frequency.get(item_domain, 0) + 1
                    )

        rankings[kw] = {
            "position": rank if rank else "Not in top 20",
            "ranked": rank is not None,
        }

    # Sort competitors by frequency
    top_competitors = sorted(
        competitor_frequency.items(), key=lambda x: x[1], reverse=True
    )[:5]

    return rankings, [{"domain": d, "appearances": c} for d, c in top_competitors]


def main():
    parser = argparse.ArgumentParser(
        description="RPG Brand 360 Audit — SERP Data Collection"
    )
    parser.add_argument("--brand", required=True, help="The client brand name")
    parser.add_argument(
        "--domain",
        required=True,
        help="The client's primary domain (e.g., example.com)",
    )
    parser.add_argument(
        "--keywords",
        required=True,
        help="Comma-separated list of target keywords (3-5 recommended)",
    )
    parser.add_argument(
        "--output",
        default="/tmp/serp_audit_results.json",
        help="Path to save the full JSON output (default: /tmp/serp_audit_results.json)",
    )

    args = parser.parse_args()
    api_key = get_api_key()

    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    target_domain = extract_domain(args.domain)

    print(f"\nRPG Brand 360 Audit — SERP Collection")
    print(f"Brand:   {args.brand}")
    print(f"Domain:  {target_domain}")
    print(f"Keywords: {keywords}")
    print("-" * 50)

    # 1. Keyword rankings and competitor surfacing
    print("\n[1/3] Running keyword rank checks...")
    rankings, top_competitors = run_keyword_audit(keywords, target_domain, api_key)

    # 2. Local pack check (using first keyword)
    print("\n[2/3] Checking Local Pack presence...")
    local_pack = check_local_pack(keywords[0], args.brand, api_key)

    # 3. Knowledge Panel check
    print("\n[3/3] Checking Knowledge Panel...")
    knowledge_panel = check_knowledge_panel(args.brand, api_key)

    # Compile results
    results = {
        "brand": args.brand,
        "domain": target_domain,
        "keywords_audited": keywords,
        "keyword_rankings": rankings,
        "local_pack": local_pack,
        "knowledge_panel": knowledge_panel,
        "top_competitors_from_serp": top_competitors,
        "summary": {
            "keywords_ranking_in_top_20": sum(
                1 for v in rankings.values() if v["ranked"]
            ),
            "total_keywords_checked": len(keywords),
            "local_pack_present": local_pack.get("present", False),
            "knowledge_panel_present": knowledge_panel.get("present", False),
        },
    }

    # Save to file
    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)

    # Print summary
    print("\n" + "=" * 50)
    print("SERP AUDIT COMPLETE")
    print("=" * 50)
    print(f"\nKeyword Rankings:")
    for kw, data in rankings.items():
        pos = data["position"]
        status = f"Position {pos}" if data["ranked"] else "Not in top 20"
        print(f"  '{kw}': {status}")

    print(f"\nLocal Pack: {'YES' if local_pack.get('present') else 'NO'}")
    print(f"Knowledge Panel: {'YES' if knowledge_panel.get('present') else 'NO'}")

    print(f"\nTop Competitors Found in SERP:")
    for comp in top_competitors:
        print(f"  {comp['domain']} (appeared {comp['appearances']}x across keywords)")

    print(f"\nFull results saved to: {args.output}")
    print(
        f"\nSummary: {results['summary']['keywords_ranking_in_top_20']} of "
        f"{results['summary']['total_keywords_checked']} keywords ranking in top 20."
    )


if __name__ == "__main__":
    main()
