#!/usr/bin/env python3
"""
RPG Local SEO GMB — Step 4: GBP Posting Strategy & Content Calendar
Generates a data-driven posting strategy based on:
  - Business type and vertical
  - Competitor category analysis
  - Seasonal/local signals
  - GBP post type best practices
Outputs a 90-day content calendar with post topics, types, and CTAs.
"""

import os
import json
import argparse
from datetime import datetime, timedelta
from typing import Optional


# ─── Post Type Definitions ───────────────────────────────────────────────────

POST_TYPES = {
    "whats_new": {
        "label": "What's New",
        "frequency": "weekly",
        "purpose": "Announce updates, new services, seasonal offers",
        "lifespan_days": 7,
        "best_for": ["promotions", "new services", "team news"],
        "cta_options": ["Learn more", "Call now", "Get a quote", "Book online"],
    },
    "offer": {
        "label": "Offer",
        "frequency": "bi-weekly",
        "purpose": "Time-limited discounts or promotions",
        "lifespan_days": 7,
        "best_for": ["seasonal deals", "referral discounts", "first-time customer offers"],
        "cta_options": ["Get offer", "Call now", "Book online"],
    },
    "event": {
        "label": "Event",
        "frequency": "monthly",
        "purpose": "Local events, community involvement, open houses",
        "lifespan_days": 14,
        "best_for": ["community events", "trade shows", "workshops"],
        "cta_options": ["Learn more", "Sign up", "Register"],
    },
    "product": {
        "label": "Product/Service Spotlight",
        "frequency": "weekly",
        "purpose": "Highlight a specific service with keyword-rich copy",
        "lifespan_days": 7,
        "best_for": ["service pages", "seasonal services", "upsell opportunities"],
        "cta_options": ["Learn more", "Get a quote", "Call now"],
    },
}


# ─── Vertical-Specific Topic Banks ───────────────────────────────────────────

TOPIC_BANKS = {
    "home_services": [
        "Before/after project photo with service + city keyword",
        "Seasonal maintenance tip (e.g., 'Prepare your HVAC for summer in [City]')",
        "Common problem + how we fix it (educational post)",
        "Customer testimonial spotlight with project details",
        "Meet the team / technician spotlight",
        "Emergency service availability reminder",
        "How to know when you need [service] (FAQ format)",
        "Local project completion announcement",
        "Industry certification or license highlight",
        "Community involvement or local sponsorship",
        "Warranty or guarantee highlight",
        "Free estimate offer post",
        "Seasonal offer (spring tune-up, winter prep, etc.)",
        "Photo gallery: recent work in [specific neighborhood]",
        "FAQ: 'How much does [service] cost in [City]?'",
    ],
    "professional_services": [
        "Client success story (anonymized)",
        "Industry news and what it means for [City] businesses",
        "Free resource or checklist offer",
        "Team expertise spotlight",
        "Common mistake + how to avoid it",
        "Process walkthrough: what to expect when you hire us",
        "Community event participation",
        "Award or recognition announcement",
        "Seasonal business tip relevant to vertical",
        "FAQ: 'What does [service] cost in [City]?'",
    ],
    "retail": [
        "New product arrival with photo",
        "Limited-time sale or discount",
        "Behind-the-scenes: how products are sourced",
        "Customer review spotlight",
        "Seasonal collection feature",
        "Gift guide for local holidays/events",
        "Store hours update",
        "Community event or pop-up announcement",
        "Product comparison or buying guide",
        "Loyalty program highlight",
    ],
    "restaurant_food": [
        "Daily or weekly special with photo",
        "New menu item spotlight",
        "Behind-the-scenes kitchen photo",
        "Chef or team spotlight",
        "Customer review highlight",
        "Local ingredient sourcing story",
        "Holiday or seasonal menu announcement",
        "Catering or event hosting offer",
        "Reservation availability reminder",
        "Community involvement or charity tie-in",
    ],
    "health_wellness": [
        "Health tip relevant to season",
        "Patient/client success story (with permission)",
        "New service or treatment spotlight",
        "Insurance or payment option update",
        "Staff introduction or credentials highlight",
        "Community health event participation",
        "FAQ: 'Do you accept [insurance] in [City]?'",
        "Seasonal health reminder",
        "Appointment availability announcement",
        "Before/after (where appropriate and ethical)",
    ],
    "generic": [
        "Service spotlight with city keyword",
        "Customer testimonial",
        "Team or staff highlight",
        "Seasonal tip or reminder",
        "Community involvement",
        "FAQ post",
        "Project or work showcase",
        "Offer or promotion",
        "Industry news or update",
        "Behind-the-scenes post",
    ],
}


def detect_vertical(business_type: str) -> str:
    """Detect the business vertical from the business type string."""
    bt = business_type.lower()

    home_signals = ["plumb", "hvac", "electric", "roof", "landscap", "remodel",
                    "paint", "clean", "pest", "lawn", "garage", "flooring", "window",
                    "handyman", "contractor", "construction", "pool", "fence"]
    professional_signals = ["attorney", "lawyer", "accountant", "cpa", "financial",
                             "insurance", "real estate", "consultant", "marketing",
                             "agency", "advisor", "broker", "therapist", "counselor"]
    retail_signals = ["store", "shop", "boutique", "retail", "clothing", "furniture",
                      "electronics", "jewelry", "gift", "hardware"]
    food_signals = ["restaurant", "cafe", "bakery", "pizza", "sushi", "food",
                    "catering", "bar", "brewery", "coffee", "diner"]
    health_signals = ["dental", "medical", "clinic", "chiropractic", "optometry",
                      "physical therapy", "spa", "salon", "gym", "fitness", "wellness",
                      "urgent care", "pharmacy"]

    if any(s in bt for s in home_signals):
        return "home_services"
    if any(s in bt for s in professional_signals):
        return "professional_services"
    if any(s in bt for s in retail_signals):
        return "retail"
    if any(s in bt for s in food_signals):
        return "restaurant_food"
    if any(s in bt for s in health_signals):
        return "health_wellness"
    return "generic"


def generate_posting_frequency(gbp_completeness: float, competitor_count: int) -> dict:
    """Recommend posting frequency based on competitive landscape."""
    # Base: 1 post/week. Scale up for competitive markets.
    if competitor_count >= 15 or gbp_completeness < 50:
        posts_per_week = 2
        rationale = "High competition or low GBP completeness — post 2x/week to accelerate visibility"
    elif competitor_count >= 8:
        posts_per_week = 1
        rationale = "Moderate competition — 1 post/week maintains consistent presence"
    else:
        posts_per_week = 1
        rationale = "Lower competition — 1 post/week is sufficient; focus on quality over quantity"

    return {
        "posts_per_week": posts_per_week,
        "posts_per_month": posts_per_week * 4,
        "posts_per_90_days": posts_per_week * 13,
        "rationale": rationale,
        "best_days": ["Tuesday", "Wednesday", "Thursday"],
        "best_time": "Between 9am–11am local time (peak search hours for local queries)",
    }


def generate_content_calendar(
    business_type: str,
    business_name: str,
    location: str,
    service_areas: list,
    top_services: list,
    start_date: Optional[datetime] = None,
    posts_per_week: int = 1,
    days: int = 90,
) -> list:
    """Generate a 90-day GBP post content calendar."""
    vertical = detect_vertical(business_type)
    topics = TOPIC_BANKS.get(vertical, TOPIC_BANKS["generic"])

    if start_date is None:
        start_date = datetime.now()

    calendar = []
    post_num = 0
    current_date = start_date
    topic_index = 0

    # Cycle through post types
    post_type_cycle = ["product", "whats_new", "offer", "product", "whats_new",
                       "product", "event", "whats_new"]

    while current_date <= start_date + timedelta(days=days):
        # Skip weekends for posting (optional — most local businesses post weekdays)
        if current_date.weekday() >= 5:
            current_date += timedelta(days=1)
            continue

        # Only post on recommended days
        if current_date.weekday() not in [1, 2, 3]:  # Tue, Wed, Thu
            current_date += timedelta(days=1)
            continue

        # Check if we've hit weekly quota
        week_num = (current_date - start_date).days // 7
        posts_this_week = sum(1 for p in calendar if (p["date"] - start_date).days // 7 == week_num)
        if posts_this_week >= posts_per_week:
            current_date += timedelta(days=1)
            continue

        # Select topic and rotate through service areas
        topic_template = topics[topic_index % len(topics)]
        service = top_services[post_num % len(top_services)] if top_services else business_type
        area = service_areas[post_num % len(service_areas)] if service_areas else location
        post_type_key = post_type_cycle[post_num % len(post_type_cycle)]
        post_type = POST_TYPES[post_type_key]

        # Personalize topic
        topic = topic_template.replace("[City]", area).replace("[service]", service)

        # Build post brief
        post = {
            "post_number": post_num + 1,
            "date": current_date,
            "date_str": current_date.strftime("%Y-%m-%d"),
            "day_of_week": current_date.strftime("%A"),
            "week": f"Week {week_num + 1}",
            "month": f"Month {(current_date - start_date).days // 30 + 1}",
            "post_type": post_type["label"],
            "topic": topic,
            "service_focus": service,
            "geo_focus": area,
            "suggested_cta": post_type["cta_options"][0],
            "copy_brief": build_copy_brief(topic, service, area, business_name, post_type_key),
            "photo_direction": build_photo_direction(topic, service, post_type_key),
            "keywords_to_include": [
                f"{service} {area}",
                f"{service} {location}",
                business_type,
            ],
        }
        calendar.append(post)

        post_num += 1
        topic_index += 1
        current_date += timedelta(days=1)

    return calendar


def build_copy_brief(topic: str, service: str, area: str, biz_name: str, post_type: str) -> str:
    """Generate a copy brief for each post."""
    briefs = {
        "product": f"Spotlight {service} in {area}. Open with a problem statement, explain how {biz_name} solves it, include 1-2 keywords naturally, end with CTA. 150-250 words.",
        "whats_new": f"Share a recent update, project completion, or team news related to {service}. Mention {area} for geo-relevance. Keep it conversational. 100-200 words.",
        "offer": f"Announce a time-limited offer for {service}. State the discount/benefit clearly, include expiry date, mention {area} coverage. 100-150 words.",
        "event": f"Announce or recap a community event or local involvement. Tie back to {service} expertise. Mention {area}. 100-200 words.",
    }
    return briefs.get(post_type, f"Write a post about {topic} for {area}. Include {service} keywords. 150-200 words.")


def build_photo_direction(topic: str, service: str, post_type: str) -> str:
    """Generate photo direction for each post."""
    directions = {
        "product": f"Use a high-quality photo of completed {service} work. Geo-tag the photo to the service location before uploading. Avoid stock photos.",
        "whats_new": "Use a real team photo, project photo, or behind-the-scenes image. Authenticity > polish for GBP posts.",
        "offer": "Create a simple graphic with the offer details OR use a project photo with text overlay. Keep branding consistent.",
        "event": "Use a photo from the event or a community-relevant image. Real photos perform better than stock.",
    }
    return directions.get(post_type, f"Use a real photo related to {service}. Geo-tag before uploading.")


def run_posting_strategy(
    business_type: str,
    business_name: str,
    location: str,
    service_areas: list,
    top_services: list,
    competitor_json: str,
    gbp_audit_json: str,
    output_dir: str = ".",
) -> str:
    """Full posting strategy pipeline."""
    print(f"\n[1/3] Loading competitor and GBP data...")
    with open(competitor_json, "r") as f:
        competitor_data = json.load(f)
    with open(gbp_audit_json, "r") as f:
        gbp_data = json.load(f)

    competitor_count = competitor_data.get("meta", {}).get("total_competitors_found", 10)
    gbp_completeness = gbp_data.get("completeness_audit", {}).get("completeness_score", 50)

    print(f"[2/3] Calculating posting frequency...")
    frequency = generate_posting_frequency(gbp_completeness, competitor_count)

    print(f"[3/3] Generating 90-day content calendar ({frequency['posts_per_week']} posts/week)...")
    calendar = generate_content_calendar(
        business_type=business_type,
        business_name=business_name,
        location=location,
        service_areas=service_areas,
        top_services=top_services,
        posts_per_week=frequency["posts_per_week"],
        days=90,
    )

    # Convert dates to strings for JSON serialization
    calendar_serializable = []
    for post in calendar:
        p = post.copy()
        p["date"] = p["date"].isoformat()
        calendar_serializable.append(p)

    report = {
        "meta": {
            "business_name": business_name,
            "business_type": business_type,
            "location": location,
            "service_areas": service_areas,
            "top_services": top_services,
            "vertical_detected": detect_vertical(business_type),
        },
        "posting_frequency": frequency,
        "content_calendar": calendar_serializable,
        "total_posts_planned": len(calendar),
        "posting_best_practices": [
            "Always use real photos — never stock images on GBP posts",
            "Geo-tag every photo to the service location before uploading",
            "Include the city/area name in the post copy at least once",
            "Add a clear CTA with every post (call, book, get a quote)",
            "Respond to all GBP reviews within 24 hours — this signals activity to Google",
            "Post consistently — gaps of 2+ weeks hurt visibility",
            "Use the 'Offer' post type for time-sensitive promotions (they display differently in Maps)",
            "Include your primary keyword + city in the first sentence of every post",
            "Link to a relevant service page on your website from each post",
            "Monitor GBP Insights monthly to see which posts drive the most clicks and calls",
        ],
    }

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "04_posting_strategy.json")
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2, default=str)

    print(f"\n✅ Posting strategy complete. {len(calendar)} posts planned over 90 days.")
    print(f"   Output: {out_path}")
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RPG Local SEO — Posting Strategy")
    parser.add_argument("--type", required=True, help="Business type")
    parser.add_argument("--name", required=True, help="Business name")
    parser.add_argument("--location", required=True, help="Primary city, State")
    parser.add_argument("--service-areas", default="", help="Comma-separated service areas")
    parser.add_argument("--services", default="", help="Comma-separated top services")
    parser.add_argument("--competitor-json", required=True, help="Path to 01_competitor_research.json")
    parser.add_argument("--gbp-audit-json", required=True, help="Path to 03_gbp_audit.json")
    parser.add_argument("--output", default="./rpg_local_seo_output", help="Output directory")
    args = parser.parse_args()

    areas = [a.strip() for a in args.service_areas.split(",") if a.strip()] or [args.location]
    services = [s.strip() for s in args.services.split(",") if s.strip()] or [args.type]

    run_posting_strategy(
        business_type=args.type,
        business_name=args.name,
        location=args.location,
        service_areas=areas,
        top_services=services,
        competitor_json=args.competitor_json,
        gbp_audit_json=args.gbp_audit_json,
        output_dir=args.output,
    )
