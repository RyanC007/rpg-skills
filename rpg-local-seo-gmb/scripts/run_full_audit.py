#!/usr/bin/env python3
"""
RPG Local SEO GMB — Master Orchestrator
Runs the full 5-step pipeline end-to-end:
  1. Competitor research (Google Maps + Local Pack)
  2. Entity & website alignment
  3. GBP profile deep audit
  4. Posting strategy & content calendar
  5. 90-day game plan generation

Usage:
  python run_full_audit.py \
    --type "plumber" \
    --name "ABC Plumbing" \
    --location "Charlotte, NC" \
    --website "https://abcplumbing.com" \
    --gbp-url "https://maps.google.com/?cid=12345" \
    --gbp-categories "Plumber,Drainage service" \
    --service-areas "Charlotte,Mint Hill,Concord,Kannapolis" \
    --services "drain cleaning,water heater repair,leak detection" \
    --output "./rpg_local_seo_output"
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent


def run_step(script: str, args: list, step_label: str) -> str:
    """Run a pipeline step and return the output JSON path."""
    print(f"\n{'='*60}")
    print(f"  {step_label}")
    print(f"{'='*60}")

    cmd = [sys.executable, str(SCRIPT_DIR / script)] + args
    result = subprocess.run(cmd, capture_output=False, text=True)

    if result.returncode != 0:
        print(f"\n❌ Step failed: {step_label}")
        print(f"   Return code: {result.returncode}")
        sys.exit(1)

    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="RPG Local SEO GMB — Full Audit Pipeline")
    parser.add_argument("--type", required=True, help="Business type (e.g., 'plumber', 'HVAC contractor')")
    parser.add_argument("--name", required=True, help="Business name")
    parser.add_argument("--location", required=True, help="Primary city, State (e.g., 'Charlotte, NC')")
    parser.add_argument("--website", required=True, help="Client website URL")
    parser.add_argument("--gbp-url", required=True, help="Client GBP URL from Google Maps")
    parser.add_argument("--gbp-categories", default="", help="Comma-separated current GBP categories")
    parser.add_argument("--service-areas", default="", help="Comma-separated service areas")
    parser.add_argument("--services", default="", help="Comma-separated top services")
    parser.add_argument("--output", default="./rpg_local_seo_output", help="Output directory")
    args = parser.parse_args()

    if not os.environ.get("SERP_API_KEY"):
        print("\n❌ ERROR: SERP_API_KEY environment variable is not set.")
        print("   Set it with: export SERP_API_KEY='your_key_here'")
        sys.exit(1)

    output = args.output
    os.makedirs(output, exist_ok=True)

    print(f"\n🚀 RPG Local SEO GMB — Full Audit")
    print(f"   Business: {args.name} ({args.type})")
    print(f"   Location: {args.location}")
    print(f"   Website:  {args.website}")
    print(f"   Output:   {output}")

    # Step 1: Competitor Research
    run_step("01_research_competitors.py", [
        "--type", args.type,
        "--location", args.location,
        "--output", output,
    ], "STEP 1/5: Competitor Research (Google Maps + Local Pack)")

    competitor_json = os.path.join(output, "01_competitor_research.json")

    # Step 2: Entity & Website Alignment
    run_step("02_entity_website_alignment.py", [
        "--url", args.website,
        "--competitor-json", competitor_json,
        "--gbp-categories", args.gbp_categories,
        "--output", output,
    ], "STEP 2/5: Entity & Website Alignment")

    entity_json = os.path.join(output, "02_entity_alignment.json")

    # Step 3: GBP Profile Audit
    run_step("03_gbp_profile_audit.py", [
        "--gbp-url", args.gbp_url,
        "--name", args.name,
        "--location", args.location,
        "--output", output,
    ], "STEP 3/5: GBP Profile Deep Audit")

    gbp_json = os.path.join(output, "03_gbp_audit.json")

    # Step 4: Posting Strategy
    run_step("04_posting_strategy.py", [
        "--type", args.type,
        "--name", args.name,
        "--location", args.location,
        "--service-areas", args.service_areas or args.location,
        "--services", args.services or args.type,
        "--competitor-json", competitor_json,
        "--gbp-audit-json", gbp_json,
        "--output", output,
    ], "STEP 4/5: Posting Strategy & Content Calendar")

    posting_json = os.path.join(output, "04_posting_strategy.json")

    # Step 5: 90-Day Game Plan
    run_step("05_generate_roadmap.py", [
        "--competitor-json", competitor_json,
        "--entity-json", entity_json,
        "--gbp-json", gbp_json,
        "--posting-json", posting_json,
        "--output", output,
    ], "STEP 5/5: 90-Day Game Plan Generation")

    game_plan = os.path.join(output, "90_day_local_seo_game_plan.md")

    print(f"\n{'='*60}")
    print(f"  ✅ AUDIT COMPLETE")
    print(f"{'='*60}")
    print(f"\n  Output files:")
    print(f"  📊 {competitor_json}")
    print(f"  🔍 {entity_json}")
    print(f"  📋 {gbp_json}")
    print(f"  📅 {posting_json}")
    print(f"  📄 {game_plan}  ← DELIVER THIS TO CLIENT")
    print(f"\n  Next: Review the game plan, sanitize client-sensitive data,")
    print(f"        then deliver via the RPG proposal workflow.")


if __name__ == "__main__":
    main()
