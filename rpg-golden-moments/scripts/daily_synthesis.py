#!/usr/bin/env python3
"""
Golden Moments: Daily Synthesis Script
Pulls logged moments and generates sanitized content drafts for LinkedIn, Substack, and X.
"""

import argparse
import json
import sys
import os

# Add guardrails to path to import sanitizer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../_guardrails')))
from content_sanitizer import sanitize_content

def synthesize_moments(raw_moments_text):
    """Generates content drafts from raw moments."""
    
    # In a real scenario, this would use an LLM to generate the drafts.
    # Here we simulate the generation and apply the sanitizer.
    
    raw_linkedin = f"Today was a game changer. We leveraged new tools to elevate our workflow. It's worth noting that this is a robust solution. {raw_moments_text}"
    raw_x = f"Just implemented a transformative new system. Seamless integration. #buildinpublic"
    
    drafts = {
        "linkedin_draft": sanitize_content(raw_linkedin, is_logoclothz=False),
        "x_draft": sanitize_content(raw_x, is_logoclothz=False)
    }
    
    return drafts

def main():
    parser = argparse.ArgumentParser(description="Golden Moments Daily Synthesis")
    parser.add_argument("--input", required=True, help="Path to raw moments text or CSV")
    parser.add_argument("--output", help="Path to save the generated drafts (JSON)")
    
    args = parser.parse_args()
    
    try:
        with open(args.input, 'r') as f:
            raw_text = f.read()
    except Exception as e:
        print(f"Error reading input file: {e}")
        # Fallback for testing
        raw_text = "We built a new feature today."
        
    print("Synthesizing and sanitizing daily moments...")
    drafts = synthesize_moments(raw_text)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(drafts, f, indent=2)
        print(f"Drafts saved to {args.output}")
    else:
        print(json.dumps(drafts, indent=2))

if __name__ == "__main__":
    main()
