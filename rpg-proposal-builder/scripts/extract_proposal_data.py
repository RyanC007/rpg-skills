#!/usr/bin/env python3
"""
RPG Proposal Builder — Step 1: Extract Data from Discovery Notes
Usage: python3 extract_proposal_data.py --input /path/to/notes.md
Outputs structured JSON to stdout for Human-in-the-Loop review.
"""

import os
import sys
import json
import argparse
from openai import OpenAI

def extract_proposal_data(input_text: str) -> dict:
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_API_BASE"),
    )

    system_prompt = """You are an expert proposal analyst for Ready, Plan, Grow! (RPG).
Extract structured proposal data from discovery call notes or transcripts.

CRITICAL RULES:
- NEVER include "Conversion Strategy" — it is not an RPG service.
- Use RPG voice: direct, conversational, anti-BS, no jargon, no em dashes.
- Pain points must be written as short, punchy statements (1-2 sentences max).
- If a value is unknown or not mentioned, use null.
- Website dev fee is confirmed only if explicitly stated. Do not infer it.
- Content plan: only confirm if explicitly chosen. Otherwise set to "TBD — client to confirm".
"""

    user_prompt = f"""Extract the following from these discovery notes and return ONLY valid JSON:

{{
  "client_company_name": "string",
  "client_first_name": "string",
  "proposal_month_year": "Month YYYY",
  "pain_points": [
    "Pain point 1 in RPG voice (1-2 sentences)",
    "Pain point 2 in RPG voice (1-2 sentences)",
    "Pain point 3 in RPG voice (1-2 sentences)"
  ],
  "content_plan": "Pro | Premium | TBD — client to confirm",
  "website_dev_fee": "dollar amount as string, e.g. $2,000 | null",
  "website_type": "New build | Redesign | Audit and optimization | null",
  "website_timeline_weeks": "e.g. 4-6 | null",
  "knowledge_base_fee": "dollar amount as string, e.g. $1,500 | null",
  "addons_description": "comma-separated list or null",
  "addons_fee": "dollar amount as string or null",
  "total_upfront": "dollar amount as string or TBD",
  "monthly_ongoing": "dollar amount as string or TBD",
  "questions_for_human": ["Any gaps or ambiguities that need human confirmation"]
}}

DISCOVERY NOTES:
{input_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    return json.loads(response.choices[0].message.content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract proposal data from discovery notes.")
    parser.add_argument("--input", required=True, help="Path to the discovery notes/transcript file.")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        input_text = f.read()

    result = extract_proposal_data(input_text)
    print(json.dumps(result, indent=2))
