#!/usr/bin/env python3
"""
Link: Outreach Sequence Generator
Generates a 3-touch email sequence for a specific lead or industry, adhering to Logoclothz brand constraints.
"""

import argparse
import json
import sys
import os

# Add guardrails to path to import sanitizer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../_guardrails')))
from content_sanitizer import sanitize_content

def generate_sequence(industry, company_name):
    """Generates a 3-touch email sequence."""
    
    # Base copy
    touch_1_body = f"Hi [Name],\n\nI noticed {company_name} is growing its team in the {industry} space. We help businesses like yours outfit their staff with high-quality, custom branded apparel.\n\nEverything we do is cut sewn and printed in the USA, ensuring fast turnaround times and consistent quality.\n\nAre you the right person to speak with about team uniforms or corporate gear?\n\nBest,\nRyan"
    
    touch_2_body = f"Hi [Name],\n\nFollowing up on my previous note. We recently helped another {industry} company outfit their 50-person team in under two weeks.\n\nWould you be open to a quick chat next week to see if we're a fit for {company_name}?\n\nBest,\nRyan"
    
    touch_3_body = f"Hi [Name],\n\nI don't want to clog your inbox. If custom apparel isn't a priority for {company_name} right now, just let me know.\n\nIf it is, I'd love to send over a few samples of our work.\n\nBest,\nRyan"
    
    sequence = {
        "Touch 1": {
            "Subject": sanitize_content(f"Custom apparel for the {industry} team at {company_name}", is_logoclothz=True),
            "Body": sanitize_content(touch_1_body, is_logoclothz=True)
        },
        "Touch 2": {
            "Subject": sanitize_content("Re: Custom apparel for the team", is_logoclothz=True),
            "Body": sanitize_content(touch_2_body, is_logoclothz=True)
        },
        "Touch 3": {
            "Subject": sanitize_content("Quick question", is_logoclothz=True),
            "Body": sanitize_content(touch_3_body, is_logoclothz=True)
        }
    }
    return sequence

def main():
    parser = argparse.ArgumentParser(description="Generate Outreach Sequence")
    parser.add_argument("--industry", required=True, help="Target industry")
    parser.add_argument("--company", required=True, help="Target company name")
    parser.add_argument("--output", help="Path to save the JSON sequence")
    
    args = parser.parse_args()
    
    print(f"Generating sanitized sequence for {args.company} in the {args.industry} industry...")
    sequence = generate_sequence(args.industry, args.company)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(sequence, f, indent=2)
        print(f"Sequence saved to {args.output}")
    else:
        print(json.dumps(sequence, indent=2))

if __name__ == "__main__":
    main()
