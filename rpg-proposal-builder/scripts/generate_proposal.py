#!/usr/bin/env python3
"""
RPG Proposal Builder — Step 2: Generate Final Proposal HTML
Usage: python3 generate_proposal.py --data /path/to/approved_data.json --template /path/to/rpg-backpack-proposal.html --output /path/to/output.html

RULES:
- Copies the template verbatim. Only replaces defined placeholder tokens.
- Never modifies any CSS, layout, structure, or non-placeholder content.
- All replacements are surgical string substitutions only.
"""

import argparse
import json
import re
import shutil
from pathlib import Path


PLACEHOLDER_MAP = {
    # Cover
    "[Client Company Name]":              lambda d: d.get("client_company_name", "[Client Company Name]"),
    "[Month Year]":                        lambda d: d.get("proposal_month_year", "[Month Year]"),

    # What We Discussed — three paraphrase slots
    "[Paraphrase of a specific challenge or goal the prospect named in conversation.]":
        lambda d: d["pain_points"][0] if len(d.get("pain_points", [])) > 0 else "[Pain point 1]",
    "[Paraphrase of a second priority, concern, or point of friction they raised.]":
        lambda d: d["pain_points"][1] if len(d.get("pain_points", [])) > 1 else "[Pain point 2]",
    "[Paraphrase of a third observation about their current state or competitive pressure.]":
        lambda d: d["pain_points"][2] if len(d.get("pain_points", [])) > 2 else "[Pain point 3]",

    # Summary table — content plan row
    "[PLAN COLOR]":
        lambda d: "var(--orange)" if d.get("content_plan") == "Premium" else "var(--green)" if d.get("content_plan") == "Pro" else "var(--navy)",
    "[Premium / Pro] Content Plan":
        lambda d: f"{d.get('content_plan', 'TBD')} Content Plan" if d.get("content_plan") not in (None, "TBD — client to confirm") else "Content Plan (Craig to confirm: Pro $250/mo or Premium $650/mo)",
    "[$250 / $650]":
        lambda d: "$250" if d.get("content_plan") == "Pro" else "$650" if d.get("content_plan") == "Premium" else "$250 (Pro) / $650 (Premium)",
    "[Pro: we publish. Premium: your team publishes.]":
        lambda d: "Pro: your team publishes. Premium: we publish and manage everything.",

    # Website row
    "[New build / Redesign / Audit and optimization]":
        lambda d: d.get("website_type") or "New build",
    "[X] weeks":
        lambda d: f"{d.get('website_timeline_weeks', '4-6')} weeks",

    # Add-ons row
    "[List specific add-ons selected, e.g. SEO Deep Dive, Know Your Numbers, CRM Setup, Analytics Setup, Customer Journey Optimization, etc.]":
        lambda d: d.get("addons_description") or "To be confirmed",

    # Totals
    "$[TOTAL]":
        lambda d: d.get("total_upfront", "TBD"),
    "$[MONTHLY]":
        lambda d: d.get("monthly_ongoing", "TBD"),

    # Footer note
    "Backpack + first 3 months of content plan [+ website if applicable]":
        lambda d: _build_total_note(d),
}


def _build_total_note(data: dict) -> str:
    parts = ["Business Backpack"]
    if data.get("website_dev_fee"):
        parts.append(f"Website Development ({data['website_dev_fee']})")
    if data.get("knowledge_base_fee"):
        parts.append(f"Knowledge Base Setup ({data['knowledge_base_fee']})")
    parts.append("first 3 months of content plan")
    return " + ".join(parts)


def _replace_website_tbd(html: str, data: dict) -> str:
    """Replace the first $[TBD] (website row, line ~1455) with the confirmed fee."""
    fee = data.get("website_dev_fee") or "$[TBD]"
    return html.replace("$[TBD]", fee, 1)


def _replace_addons_tbd(html: str, data: dict) -> str:
    """Replace the second $[TBD] (add-ons row) with the confirmed fee."""
    fee = data.get("addons_fee") or "$[TBD]"
    return html.replace("$[TBD]", fee, 1)


def generate_proposal(data: dict, template_path: Path, output_path: Path) -> None:
    html = template_path.read_text(encoding="utf-8")

    # Apply all standard placeholder replacements
    for placeholder, resolver in PLACEHOLDER_MAP.items():
        replacement = resolver(data)
        html = html.replace(placeholder, replacement)

    # Handle the two $[TBD] occurrences separately (order matters)
    html = _replace_website_tbd(html, data)
    html = _replace_addons_tbd(html, data)

    output_path.write_text(html, encoding="utf-8")
    print(f"Proposal written to: {output_path}")

    # Verify no placeholders remain
    remaining = re.findall(r'\[[A-Z][^\]]{2,}\]', html)
    # Filter out known safe bracket patterns (e.g. CSS calc expressions)
    remaining = [r for r in remaining if not r.startswith("[CMD") and "var(" not in r]
    if remaining:
        print(f"\nWARNING: Possible unfilled placeholders remaining:")
        for r in set(remaining):
            print(f"  {r}")
    else:
        print("Verification passed: no unfilled placeholders detected.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate RPG proposal HTML from approved data JSON.")
    parser.add_argument("--data",     required=True, help="Path to the approved JSON data file.")
    parser.add_argument("--template", required=True, help="Path to the original rpg-backpack-proposal.html template.")
    parser.add_argument("--output",   required=True, help="Path for the generated proposal HTML file.")
    args = parser.parse_args()

    with open(args.data, "r") as f:
        data = json.load(f)

    generate_proposal(data, Path(args.template), Path(args.output))
