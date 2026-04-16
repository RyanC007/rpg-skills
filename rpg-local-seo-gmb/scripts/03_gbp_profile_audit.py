#!/usr/bin/env python3
"""
RPG Local SEO GMB — Step 3: GBP Profile Deep Audit
Pulls the client's GBP via SerpAPI Google Maps Place endpoint,
audits every field, scores completeness, and generates enhancement recommendations
for every possible GBP entry point.
"""

import os
import sys
import json
import re
import requests
import argparse
from urllib.parse import urlparse, parse_qs

SERP_API_KEY = os.environ.get("SERP_API_KEY", "")
BASE_URL = "https://serpapi.com/search"


# ─── GBP Data Retrieval ──────────────────────────────────────────────────────

def extract_place_id_from_url(gbp_url: str) -> str | None:
    """
    Attempt to extract a place_id or CID from a Google Maps URL.
    Handles formats:
      - maps.google.com/?cid=XXXXX
      - google.com/maps/place/.../data=...
      - maps.app.goo.gl short links (cannot extract directly — needs resolution)
    """
    # CID format
    cid_match = re.search(r"[?&]cid=(\d+)", gbp_url)
    if cid_match:
        return cid_match.group(1)

    # Place ID in URL path
    place_match = re.search(r"place_id=([A-Za-z0-9_\-]+)", gbp_url)
    if place_match:
        return place_match.group(1)

    # ChIJ format in data parameter
    chij_match = re.search(r"(ChIJ[A-Za-z0-9_\-]+)", gbp_url)
    if chij_match:
        return chij_match.group(1)

    return None


def resolve_short_url(short_url: str) -> str:
    """Follow redirects to resolve a short URL (e.g., maps.app.goo.gl)."""
    try:
        resp = requests.head(short_url, allow_redirects=True, timeout=10)
        return resp.url
    except Exception:
        return short_url


def search_gbp_by_name(business_name: str, location: str) -> dict:
    """Search for a GBP by business name + location when place_id is unavailable."""
    params = {
        "engine": "google_maps",
        "q": f"{business_name} {location}",
        "type": "search",
        "api_key": SERP_API_KEY,
    }
    resp = requests.get(BASE_URL, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_place_details(place_id: str) -> dict:
    """Fetch full GBP place details."""
    params = {
        "engine": "google_maps",
        "type": "place",
        "place_id": place_id,
        "api_key": SERP_API_KEY,
    }
    resp = requests.get(BASE_URL, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


# ─── GBP Completeness Scoring ────────────────────────────────────────────────

GBP_FIELDS = {
    # Field name: (weight, description)
    "title": (10, "Business name"),
    "type": (8, "Primary category"),
    "types": (7, "Secondary categories"),
    "address": (9, "Address"),
    "phone": (8, "Phone number"),
    "website": (7, "Website link"),
    "hours": (8, "Business hours"),
    "description": (9, "Business description"),
    "photos": (7, "Photos"),
    "rating": (5, "Rating (requires reviews)"),
    "reviews": (6, "Review count"),
    "service_options": (5, "Service options (delivery, dine-in, etc.)"),
    "amenities": (4, "Amenities"),
    "from_the_business": (6, "From the business section"),
    "questions_and_answers": (5, "Q&A section"),
    "posts": (6, "GBP posts"),
    "menu": (3, "Menu or services list"),
    "booking_link": (4, "Booking/appointment link"),
    "attributes": (5, "Business attributes"),
}


def score_gbp_completeness(place_data: dict) -> dict:
    """Score GBP profile completeness and identify missing fields."""
    place = place_data.get("place_results", place_data)

    scores = {}
    missing = []
    present = []
    enhancements = []

    total_weight = sum(w for w, _ in GBP_FIELDS.values())
    earned_weight = 0

    for field, (weight, label) in GBP_FIELDS.items():
        value = place.get(field)
        if value and value not in ({}, [], "", None, 0):
            scores[field] = {"present": True, "weight": weight, "label": label}
            earned_weight += weight
            present.append(field)
        else:
            scores[field] = {"present": False, "weight": weight, "label": label}
            missing.append(field)

    completeness_pct = round((earned_weight / total_weight) * 100, 1)

    # Generate enhancement recommendations for each missing/weak field
    enhancement_map = {
        "description": {
            "priority": "CRITICAL",
            "action": "Write a 750-character keyword-rich business description. Lead with primary service + city. Include 3-5 service keywords naturally. End with a CTA.",
            "example": "'[Business Name] is [City]'s trusted [service type]. We specialize in [service 1], [service 2], and [service 3] for residential and commercial clients across [service areas]. Call us for a free estimate.'",
        },
        "types": {
            "priority": "HIGH",
            "action": "Add up to 9 secondary GBP categories. Pull from competitor category analysis to find the highest-frequency categories your competitors use.",
            "example": "If primary is 'Plumber', add: 'Water heater installer', 'Drainage service', 'Gas installation service'",
        },
        "hours": {
            "priority": "HIGH",
            "action": "Set complete business hours including special hours for holidays. If 24/7 emergency service, mark accordingly.",
        },
        "photos": {
            "priority": "HIGH",
            "action": "Upload minimum 10 photos: exterior (2), interior (2), team/staff (2), work in progress (2), completed projects (2). Geo-tag all photos before uploading.",
        },
        "questions_and_answers": {
            "priority": "MEDIUM",
            "action": "Pre-populate 5-10 Q&As. Use questions customers actually ask. Embed service keywords and city name in answers.",
            "example": "Q: 'Do you offer emergency plumbing in Charlotte?' A: 'Yes, [Business] provides 24/7 emergency plumbing services throughout Charlotte and surrounding areas including...'",
        },
        "posts": {
            "priority": "HIGH",
            "action": "Start weekly GBP posts. Use the posting strategy from the 90-day plan. Each post: geo-tagged photo + 150-300 words + CTA + relevant keyword.",
        },
        "booking_link": {
            "priority": "MEDIUM",
            "action": "Add a booking or appointment URL. Even a contact form URL works. This adds a direct conversion path from the GBP.",
        },
        "from_the_business": {
            "priority": "MEDIUM",
            "action": "Complete the 'From the business' section. Add your founding year, highlights, and what makes you different. This feeds into Google's entity understanding.",
        },
        "service_options": {
            "priority": "LOW",
            "action": "Enable all applicable service options (online estimates, on-site services, etc.) to improve filter visibility.",
        },
        "menu": {
            "priority": "LOW",
            "action": "Add a services list via the Products/Services feature. Each service entry = another keyword signal to Google.",
        },
        "attributes": {
            "priority": "MEDIUM",
            "action": "Enable all applicable business attributes (veteran-owned, women-owned, LGBTQ+ friendly, etc.) to appear in filtered searches.",
        },
    }

    for field in missing:
        if field in enhancement_map:
            enhancements.append({
                "field": field,
                "label": GBP_FIELDS[field][1],
                "priority": enhancement_map[field]["priority"],
                "action": enhancement_map[field]["action"],
                "example": enhancement_map[field].get("example", ""),
            })

    # Sort by priority
    priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    enhancements.sort(key=lambda x: priority_order.get(x["priority"], 99))

    return {
        "completeness_score": completeness_pct,
        "earned_points": earned_weight,
        "total_points": total_weight,
        "present_fields": present,
        "missing_fields": missing,
        "enhancement_recommendations": enhancements,
        "field_scores": scores,
    }


def analyze_review_sentiment(place_data: dict) -> dict:
    """Analyze review data from GBP."""
    place = place_data.get("place_results", place_data)
    reviews_data = place.get("reviews_results", {})
    reviews = reviews_data.get("reviews", []) if isinstance(reviews_data, dict) else []

    if not reviews:
        return {
            "total_reviews": place.get("reviews", 0),
            "avg_rating": place.get("rating", 0),
            "sample_reviews": [],
            "response_rate": 0,
            "recent_activity": "No review data available via API",
        }

    responded = sum(1 for r in reviews if r.get("response"))
    response_rate = round(responded / len(reviews) * 100, 1) if reviews else 0

    return {
        "total_reviews": place.get("reviews", len(reviews)),
        "avg_rating": place.get("rating", 0),
        "sample_reviews": [
            {
                "rating": r.get("rating"),
                "snippet": r.get("snippet", "")[:200],
                "date": r.get("date", ""),
                "has_response": bool(r.get("response")),
            }
            for r in reviews[:5]
        ],
        "response_rate": response_rate,
        "owner_responses_pct": response_rate,
    }


def run_gbp_audit(gbp_url: str, business_name: str, location: str, output_dir: str = ".") -> str:
    """Full GBP audit pipeline."""
    print(f"\n[1/4] Resolving GBP URL and extracting place ID...")

    # Resolve short URLs
    if "goo.gl" in gbp_url or "maps.app" in gbp_url:
        gbp_url = resolve_short_url(gbp_url)
        print(f"      Resolved to: {gbp_url}")

    place_id = extract_place_id_from_url(gbp_url)

    if not place_id:
        print(f"      Could not extract place_id from URL. Searching by name...")
        search_result = search_gbp_by_name(business_name, location)
        local_results = search_result.get("local_results", [])
        if local_results:
            place_id = local_results[0].get("place_id", "")
            print(f"      Found place_id via search: {place_id}")
        else:
            print("ERROR: Could not find GBP. Check business name and location.")
            sys.exit(1)

    print(f"[2/4] Fetching GBP place details (place_id: {place_id})...")
    place_data = get_place_details(place_id)

    print(f"[3/4] Scoring GBP completeness...")
    completeness = score_gbp_completeness(place_data)

    print(f"[4/4] Analyzing reviews...")
    reviews = analyze_review_sentiment(place_data)

    place_info = place_data.get("place_results", place_data)

    report = {
        "meta": {
            "business_name": business_name,
            "location": location,
            "gbp_url": gbp_url,
            "place_id": place_id,
        },
        "gbp_snapshot": {
            "name": place_info.get("title", ""),
            "primary_category": place_info.get("type", ""),
            "secondary_categories": place_info.get("types", []),
            "address": place_info.get("address", ""),
            "phone": place_info.get("phone", ""),
            "website": place_info.get("website", ""),
            "rating": place_info.get("rating", 0),
            "reviews": place_info.get("reviews", 0),
            "description": place_info.get("description", ""),
            "hours": place_info.get("hours", {}),
            "service_options": place_info.get("service_options", {}),
        },
        "completeness_audit": completeness,
        "review_analysis": reviews,
    }

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "03_gbp_audit.json")
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n✅ GBP audit complete. Completeness score: {completeness['completeness_score']}%")
    print(f"   Output: {out_path}")
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RPG Local SEO — GBP Profile Audit")
    parser.add_argument("--gbp-url", required=True, help="Client GBP URL from Google Maps")
    parser.add_argument("--name", required=True, help="Business name (fallback search)")
    parser.add_argument("--location", required=True, help="City, State")
    parser.add_argument("--output", default="./rpg_local_seo_output", help="Output directory")
    args = parser.parse_args()

    if not SERP_API_KEY:
        print("ERROR: SERP_API_KEY environment variable not set.")
        sys.exit(1)

    run_gbp_audit(args.gbp_url, args.name, args.location, args.output)
