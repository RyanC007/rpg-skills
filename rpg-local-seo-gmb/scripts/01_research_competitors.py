#!/usr/bin/env python3
"""
RPG Local SEO GMB — Step 1: Research Competitors
Uses SerpAPI to pull Google Maps competitors, categories, ratings, reviews,
and entity signals for a given business type and location.
"""

import os
import sys
import json
import requests
import argparse
from datetime import datetime

SERP_API_KEY = os.environ.get("SERP_API_KEY", "")
BASE_URL = "https://serpapi.com/search"


def search_google_maps(query: str, location: str, num_results: int = 20) -> dict:
    """Pull Google Maps local results for a given query + location."""
    params = {
        "engine": "google_maps",
        "q": query,
        "location": location,
        "type": "search",
        "num": num_results,
        "api_key": SERP_API_KEY,
    }
    resp = requests.get(BASE_URL, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def search_local_pack(query: str, location: str) -> dict:
    """Pull Google Local Pack (3-pack) results for a query + location."""
    params = {
        "engine": "google",
        "q": query,
        "location": location,
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en",
        "api_key": SERP_API_KEY,
    }
    resp = requests.get(BASE_URL, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_place_details(place_id: str) -> dict:
    """Get full GBP/place details for a specific place_id."""
    params = {
        "engine": "google_maps",
        "type": "place",
        "place_id": place_id,
        "api_key": SERP_API_KEY,
    }
    resp = requests.get(BASE_URL, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def extract_competitor_data(maps_result: dict) -> list:
    """Extract structured competitor data from Google Maps results."""
    competitors = []
    local_results = maps_result.get("local_results", [])

    for biz in local_results:
        comp = {
            "name": biz.get("title", ""),
            "place_id": biz.get("place_id", ""),
            "rating": biz.get("rating", None),
            "reviews": biz.get("reviews", 0),
            "address": biz.get("address", ""),
            "phone": biz.get("phone", ""),
            "website": biz.get("website", ""),
            "type": biz.get("type", ""),
            "types": biz.get("types", []),
            "hours": biz.get("hours", ""),
            "thumbnail": biz.get("thumbnail", ""),
            "gps_coordinates": biz.get("gps_coordinates", {}),
            "description": biz.get("description", ""),
            "service_options": biz.get("service_options", {}),
            "extensions": biz.get("extensions", {}),
        }
        competitors.append(comp)

    return competitors


def extract_local_pack(serp_result: dict) -> list:
    """Extract the 3-pack local results from a standard SERP."""
    pack = []
    local_results = serp_result.get("local_results", {})
    places = local_results.get("places", []) if isinstance(local_results, dict) else []

    for place in places:
        pack.append({
            "name": place.get("title", ""),
            "rating": place.get("rating", None),
            "reviews": place.get("reviews", 0),
            "type": place.get("type", ""),
            "address": place.get("address", ""),
            "phone": place.get("phone", ""),
            "website": place.get("links", {}).get("website", ""),
            "place_id": place.get("place_id", ""),
            "position": place.get("position", 0),
        })

    return pack


def analyze_category_distribution(competitors: list) -> dict:
    """Analyze the spread of GBP categories across all competitors."""
    category_counts = {}
    for comp in competitors:
        primary = comp.get("type", "")
        if primary:
            category_counts[primary] = category_counts.get(primary, 0) + 1
        for cat in comp.get("types", []):
            if cat and cat != primary:
                category_counts[cat] = category_counts.get(cat, 0) + 1

    sorted_cats = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    return {
        "all_categories": dict(sorted_cats),
        "top_10": dict(sorted_cats[:10]),
        "total_unique": len(sorted_cats),
    }


def analyze_review_landscape(competitors: list) -> dict:
    """Summarize the review/rating landscape across competitors."""
    ratings = [c["rating"] for c in competitors if c.get("rating")]
    review_counts = [c["reviews"] for c in competitors if c.get("reviews")]

    if not ratings:
        return {"error": "No rating data available"}

    avg_rating = sum(ratings) / len(ratings)
    avg_reviews = sum(review_counts) / len(review_counts) if review_counts else 0
    max_reviews = max(review_counts) if review_counts else 0
    min_reviews = min(review_counts) if review_counts else 0

    # Identify leaders and laggards
    leaders = sorted(
        [c for c in competitors if c.get("reviews", 0) >= avg_reviews],
        key=lambda x: x.get("reviews", 0),
        reverse=True
    )[:5]

    return {
        "avg_rating": round(avg_rating, 2),
        "avg_reviews": round(avg_reviews, 1),
        "max_reviews": max_reviews,
        "min_reviews": min_reviews,
        "review_leaders": [{"name": l["name"], "rating": l["rating"], "reviews": l["reviews"]} for l in leaders],
        "to_beat_reviews": leaders[0]["reviews"] if leaders else 0,
        "to_beat_rating": leaders[0]["rating"] if leaders else 0,
    }


def run_research(business_type: str, location: str, output_dir: str = ".") -> str:
    """Full research pipeline: maps + local pack + analysis."""
    print(f"\n[1/4] Searching Google Maps: '{business_type}' in '{location}'...")
    maps_data = search_google_maps(f"{business_type} near {location}", location)
    competitors = extract_competitor_data(maps_data)
    print(f"      Found {len(competitors)} competitors on Google Maps.")

    print(f"[2/4] Pulling Local Pack results...")
    serp_data = search_local_pack(f"{business_type} {location}", location)
    local_pack = extract_local_pack(serp_data)
    print(f"      Found {len(local_pack)} businesses in the 3-pack.")

    print(f"[3/4] Analyzing categories and review landscape...")
    category_analysis = analyze_category_distribution(competitors)
    review_analysis = analyze_review_landscape(competitors)

    print(f"[4/4] Assembling research report...")
    report = {
        "meta": {
            "business_type": business_type,
            "location": location,
            "timestamp": datetime.now().isoformat(),
            "total_competitors_found": len(competitors),
        },
        "local_pack_3": local_pack,
        "all_competitors": competitors,
        "category_analysis": category_analysis,
        "review_landscape": review_analysis,
    }

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "01_competitor_research.json")
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n✅ Research complete. Output: {out_path}")
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RPG Local SEO — Competitor Research")
    parser.add_argument("--type", required=True, help="Business type (e.g., 'plumber', 'HVAC contractor')")
    parser.add_argument("--location", required=True, help="City, State (e.g., 'Charlotte, NC')")
    parser.add_argument("--output", default="./rpg_local_seo_output", help="Output directory")
    args = parser.parse_args()

    if not SERP_API_KEY:
        print("ERROR: SERP_API_KEY environment variable not set.")
        sys.exit(1)

    run_research(args.type, args.location, args.output)
