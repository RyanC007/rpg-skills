#!/usr/bin/env python3
"""
RPG Local SEO GMB — Step 5: 90-Day Roadmap Generator
Synthesizes all prior research (competitor, entity, GBP audit, posting strategy)
into a comprehensive, client-ready 90-Day Local SEO Game Plan in Markdown.
"""

import os
import json
import argparse
from datetime import datetime


def load_json(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def build_executive_summary(competitor: dict, entity: dict, gbp: dict) -> str:
    """Build the executive summary section."""
    gaps = entity.get("gap_analysis", {})
    critical = gaps.get("critical_gaps", [])
    high = gaps.get("high_priority_gaps", [])
    review_data = competitor.get("review_landscape", {})
    completeness = gbp.get("completeness_audit", {}).get("completeness_score", 0)
    local_pack = competitor.get("local_pack_3", [])
    pack_leader = local_pack[0] if local_pack else {}

    top_issues = []
    for g in (critical + high)[:3]:
        top_issues.append(f"- **{g['area']}:** {g['issue']}")

    pack_leader_text = ""
    if pack_leader:
        pack_leader_text = (
            f"The current Map Pack leader is **{pack_leader.get('name', 'Unknown')}** "
            f"with {pack_leader.get('reviews', 0)} reviews at {pack_leader.get('rating', 0)} stars."
        )

    return f"""## Executive Summary

**GBP Completeness Score:** {completeness}% — {"Needs significant work" if completeness < 60 else "Solid foundation, gaps to close" if completeness < 85 else "Strong profile, optimize for dominance"}

**Top 3 Critical Issues:**
{chr(10).join(top_issues) if top_issues else "- No critical gaps detected — focus on optimization and scale"}

**Competitive Landscape:**
{pack_leader_text}
The local market has **{competitor.get('meta', {}).get('total_competitors_found', 0)} active competitors** on Google Maps.
Average competitor rating: **{review_data.get('avg_rating', 0)} stars** with **{review_data.get('avg_reviews', 0)} reviews** on average.
To reach the top of the Map Pack, the target is **{review_data.get('to_beat_reviews', 0)} reviews** at **{review_data.get('to_beat_rating', 0)} stars**.

**Primary Goal:** Rank in the Google Maps 3-Pack for primary and supporting keywords within 90 days.
"""


def build_research_findings(competitor: dict, entity: dict, gbp: dict) -> str:
    """Build the research findings section."""
    # Competitor categories
    top_cats = competitor.get("category_analysis", {}).get("top_10", {})
    cat_rows = "\n".join([f"| {cat} | {count} competitors |" for cat, count in list(top_cats.items())[:8]])

    # Website findings
    web = entity.get("website_entities", {})
    page_count = web.get("total_pages_crawled", 0)
    service_pages = len(web.get("service_pages", []))
    location_pages = len(web.get("location_pages", []))
    nap_pct = web.get("nap_coverage_pct", 0)
    schema = web.get("schema_types_found", {})
    schema_text = ", ".join(schema.keys()) if schema else "None detected"

    # Top competitors
    pack = competitor.get("local_pack_3", [])
    comp_rows = "\n".join([
        f"| {p.get('position', i+1)} | {p.get('name', '')} | {p.get('rating', '')} | {p.get('reviews', '')} | {p.get('type', '')} |"
        for i, p in enumerate(pack[:5])
    ])

    # GBP snapshot
    gbp_snap = gbp.get("gbp_snapshot", {})
    missing_fields = gbp.get("completeness_audit", {}).get("missing_fields", [])
    missing_text = ", ".join(missing_fields[:8]) if missing_fields else "None"

    return f"""## Research Findings

### 1. Google Maps Competitive Landscape

| Position | Business | Rating | Reviews | Primary Category |
| :--- | :--- | :--- | :--- | :--- |
{comp_rows if comp_rows else "| — | No pack data available | — | — | — |"}

**Dominant Categories in This Market:**

| Category | Usage |
| :--- | :--- |
{cat_rows if cat_rows else "| No category data available | — |"}

---

### 2. Website Audit

| Signal | Status |
| :--- | :--- |
| Pages crawled | {page_count} |
| Dedicated service pages | {service_pages} {"✅" if service_pages > 0 else "❌ MISSING"} |
| City/location landing pages | {location_pages} {"✅" if location_pages > 0 else "❌ MISSING"} |
| NAP in footer | {nap_pct}% of pages {"✅" if nap_pct >= 80 else "⚠️ INCONSISTENT"} |
| Schema markup | {schema_text} {"✅" if schema else "❌ MISSING"} |

---

### 3. GBP Profile Audit

| Field | Status |
| :--- | :--- |
| Business name | {gbp_snap.get("name", "—")} |
| Primary category | {gbp_snap.get("primary_category", "—")} |
| Secondary categories | {len(gbp_snap.get("secondary_categories", []))} set |
| Rating | {gbp_snap.get("rating", 0)} ⭐ |
| Reviews | {gbp_snap.get("reviews", 0)} |
| Description | {"✅ Present" if gbp_snap.get("description") else "❌ Missing"} |
| Hours | {"✅ Set" if gbp_snap.get("hours") else "❌ Missing"} |
| Website linked | {"✅ Yes" if gbp_snap.get("website") else "❌ No"} |

**Missing GBP Fields:** {missing_text}
"""


def build_rebuild_plan(entity: dict, gbp: dict, competitor: dict) -> str:
    """Build the rebuild/fix plan section."""
    gaps = entity.get("gap_analysis", {})
    enhancements = gbp.get("completeness_audit", {}).get("enhancement_recommendations", [])
    missing_cats = gaps.get("missing_competitor_categories", [])[:5]

    # All gaps combined and sorted
    all_gaps = (
        gaps.get("critical_gaps", []) +
        gaps.get("high_priority_gaps", []) +
        gaps.get("medium_priority_gaps", [])
    )

    gap_rows = "\n".join([
        f"| {g['type']} | {g['area']} | {g['issue']} | {g['fix']} |"
        for g in all_gaps[:10]
    ])

    # GBP enhancements
    enh_rows = "\n".join([
        f"| {e['priority']} | {e['label']} | {e['action'][:120]}{'...' if len(e['action']) > 120 else ''} |"
        for e in enhancements[:8]
    ])

    # Missing categories
    cat_text = "\n".join([f"- Add **{cat}** as a secondary GBP category" for cat in missing_cats])

    return f"""## Rebuild Plan

### Website Fixes

| Priority | Area | Issue | Fix |
| :--- | :--- | :--- | :--- |
{gap_rows if gap_rows else "| — | No critical gaps | — | — |"}

---

### GBP Enhancement Queue

| Priority | Field | Action |
| :--- | :--- | :--- |
{enh_rows if enh_rows else "| — | No enhancements needed | — |"}

---

### GBP Category Expansion

Based on competitor analysis, add these secondary categories to your GBP:

{cat_text if cat_text else "- Current categories appear well-aligned with the market"}

> **Rule:** Your primary category is the most important ranking signal. Never change it unless it's genuinely wrong. Add secondary categories to capture adjacent searches.
"""


def build_90_day_roadmap(competitor: dict, entity: dict, gbp: dict, posting: dict) -> str:
    """Build the 90-day roadmap table."""
    gaps = entity.get("gap_analysis", {})
    has_critical = len(gaps.get("critical_gaps", [])) > 0
    has_service_pages = entity.get("gap_analysis", {}).get("website_has_service_pages", True)
    has_location_pages = entity.get("gap_analysis", {}).get("website_has_location_pages", True)
    completeness = gbp.get("completeness_audit", {}).get("completeness_score", 0)
    review_target = competitor.get("review_landscape", {}).get("to_beat_reviews", 20)
    posts_per_week = posting.get("posting_frequency", {}).get("posts_per_week", 1)

    # Dynamic week 1 priority
    w1_priority = "CRITICAL" if completeness < 50 or has_critical else "HIGH"
    w1_action = "Complete GBP profile (description, photos, hours, categories)" if completeness < 70 else "Optimize GBP categories + launch review request workflow"

    return f"""## 90-Day Local SEO Roadmap

### MONTH 1 (Days 1–30): Foundation

| Week | Priority | Key Actions |
| :--- | :--- | :--- |
| Week 1 | {w1_priority} | {w1_action} + fix any broken website navigation |
| Week 2 | HIGH | {"Create dedicated service pages with [Service] + [City] keyword targeting" if not has_service_pages else "Optimize existing service pages — meta titles, H1s, internal links"} |
| Week 3 | HIGH | Citation audit — check NAP consistency on Yelp, BBB, Angi, Houzz, Thumbtack. Correct all mismatches. |
| Week 4 | HIGH | Launch review request system (SMS/email within 48 hrs of job completion). Target: 5 new reviews by Day 30. |

---

### MONTH 2 (Days 31–60): Content & Reputation

| Week | Priority | Key Actions |
| :--- | :--- | :--- |
| Week 5 | HIGH | {"Build first city landing page: [Primary Service] in [City], [State]" if not has_location_pages else "Expand city pages — add next target service area"} |
| Week 6 | HIGH | Publish first 2 blog posts targeting local keywords. Link each post to a service page. |
| Week 7 | MEDIUM | Begin GBP post cadence: {posts_per_week}x/week. Use content calendar. Geo-tag all photos. |
| Week 8 | MEDIUM | Local backlink outreach: Chamber of Commerce, neighborhood associations, local news. |

---

### MONTH 3 (Days 61–90): Optimization & Scale

| Week | Priority | Key Actions |
| :--- | :--- | :--- |
| Week 9 | HIGH | Review GSC + GBP Insights data. Identify top-performing pages and lowest-performing pages. |
| Week 10 | HIGH | Re-optimize 2 underperforming pages (update meta titles, add internal links, improve content). |
| Week 11 | MEDIUM | Add next city landing page. Submit to 3 additional local directories. |
| Week 12 | MEDIUM | 90-day performance review. Plan next sprint. Celebrate wins. |

---

### KPI Tracking

| KPI | Baseline (Day 1) | 30-Day Target | 90-Day Target |
| :--- | :--- | :--- | :--- |
| GBP Completeness | {completeness}% | 90%+ | 100% |
| Google Reviews | {gbp.get("gbp_snapshot", {}).get("reviews", 0)} | +5 new | +{min(review_target, 20)} new |
| Map Pack Ranking (primary keyword) | Not in top 3 | Top 10 | Top 3 |
| Organic Traffic (monthly sessions) | [Pull from GA4] | +20% | +50% |
| Monthly Leads (calls + forms) | [Pull from CRM] | +30% | +75% |
| GBP Profile Views | [Pull from GBP Insights] | +40% | +100% |
"""


def build_posting_section(posting: dict) -> str:
    """Build the posting strategy section."""
    freq = posting.get("posting_frequency", {})
    calendar = posting.get("content_calendar", [])
    practices = posting.get("posting_best_practices", [])

    # Show first 8 posts as sample
    sample_rows = "\n".join([
        f"| {p['date_str']} | {p['day_of_week']} | {p['post_type']} | {p['service_focus']} | {p['geo_focus']} | {p['topic'][:60]}{'...' if len(p['topic']) > 60 else ''} |"
        for p in calendar[:8]
    ])

    practices_text = "\n".join([f"- {p}" for p in practices])

    return f"""## GBP Posting Strategy

**Recommended Frequency:** {freq.get('posts_per_week', 1)} post(s) per week
**Best Days:** {', '.join(freq.get('best_days', ['Tuesday', 'Wednesday', 'Thursday']))}
**Best Time:** {freq.get('best_time', '9am–11am local time')}
**Rationale:** {freq.get('rationale', '')}

**Total posts planned over 90 days:** {posting.get('total_posts_planned', 0)}

### Sample Content Calendar (First 8 Posts)

| Date | Day | Post Type | Service Focus | Geo Focus | Topic |
| :--- | :--- | :--- | :--- | :--- | :--- |
{sample_rows if sample_rows else "| — | — | — | — | — | No calendar data |"}

> The full 90-day calendar is in `04_posting_strategy.json`.

### Posting Best Practices

{practices_text}
"""


def generate_full_report(
    competitor_json: str,
    entity_json: str,
    gbp_json: str,
    posting_json: str,
    output_dir: str = ".",
) -> str:
    """Generate the full 90-day Local SEO Game Plan as Markdown."""
    print("\n[1/6] Loading all research data...")
    competitor = load_json(competitor_json)
    entity = load_json(entity_json)
    gbp = load_json(gbp_json)
    posting = load_json(posting_json)

    meta = competitor.get("meta", {})
    biz_type = meta.get("business_type", "Business")
    location = meta.get("location", "")
    biz_name = gbp.get("meta", {}).get("business_name", "Client")
    generated_date = datetime.now().strftime("%B %d, %Y")

    print("[2/6] Building executive summary...")
    exec_summary = build_executive_summary(competitor, entity, gbp)

    print("[3/6] Building research findings...")
    research = build_research_findings(competitor, entity, gbp)

    print("[4/6] Building rebuild plan...")
    rebuild = build_rebuild_plan(entity, gbp, competitor)

    print("[5/6] Building 90-day roadmap...")
    roadmap = build_90_day_roadmap(competitor, entity, gbp, posting)

    print("[6/6] Building posting strategy section...")
    post_section = build_posting_section(posting)

    # Assemble full report
    report_md = f"""# 90-Day Local SEO Game Plan
### {biz_name} | {biz_type} | {location}
*Generated by RPG Local SEO GMB Agent — {generated_date}*

---

{exec_summary}

---

{research}

---

{rebuild}

---

{roadmap}

---

{post_section}

---

## Next Steps

1. **Share this report** with the client for review and approval before making any changes.
2. **Prioritize GBP completeness** — every missing field is a missed ranking signal.
3. **Start the review engine immediately** — reviews are the fastest-moving local ranking factor.
4. **Schedule a 30-day check-in** to review GBP Insights data and adjust the roadmap.
5. **Track everything from Day 1** — baseline data is critical for proving ROI.

---

*This report was generated using real Google Maps and SERP data via SerpAPI.
All recommendations are specific to the competitive landscape in {location}.*

*Ready, Plan, Grow! | readyplangrow.com*
"""

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "90_day_local_seo_game_plan.md")
    with open(out_path, "w") as f:
        f.write(report_md)

    print(f"\n✅ 90-Day Game Plan generated: {out_path}")
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RPG Local SEO — 90-Day Game Plan Generator")
    parser.add_argument("--competitor-json", required=True)
    parser.add_argument("--entity-json", required=True)
    parser.add_argument("--gbp-json", required=True)
    parser.add_argument("--posting-json", required=True)
    parser.add_argument("--output", default="./rpg_local_seo_output")
    args = parser.parse_args()

    generate_full_report(
        args.competitor_json,
        args.entity_json,
        args.gbp_json,
        args.posting_json,
        args.output,
    )
