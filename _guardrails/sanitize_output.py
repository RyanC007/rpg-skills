"""
RPG Universal Output Sanitizer CLI
Sanitizes text files before saving, sharing, publishing, or committing.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from content_sanitizer import normalize_tier, sanitize_content
from guardrail_policy import SEVERITY_ORDER


def main() -> int:
    parser = argparse.ArgumentParser(description="Sanitize a text file according to RPG guardrails.")
    parser.add_argument("--input", required=True, help="Path to the input file")
    parser.add_argument("--output", help="Path to save the sanitized file. Defaults to overwriting input.")
    parser.add_argument("--report", help="Optional JSON report path")
    parser.add_argument("--tier", default="tier3", help="Output tier: tier1/public, tier2/client, tier3/internal")
    parser.add_argument("--client-name", help="Allowed client name for tier2 deliverables")
    parser.add_argument("--logoclothz", action="store_true", help="Apply Logoclothz brand constraints")
    parser.add_argument("--fail-on", choices=["clean", "low", "medium", "high", "critical"], default=None, help="Exit non-zero when severity is at or above this level")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.", file=sys.stderr)
        return 1

    content = Path(args.input).read_text(encoding="utf-8")
    sanitized_content, report = sanitize_content(
        content,
        is_logoclothz=args.logoclothz,
        tier=normalize_tier(args.tier),
        client_name=args.client_name,
        return_report=True,
    )

    output_path = Path(args.output if args.output else args.input)
    output_path.write_text(sanitized_content + "\n", encoding="utf-8")

    if args.report:
        Path(args.report).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Sanitized {args.input} -> {output_path} | tier={report['tier']} | severity={report['severity']} | findings={report['finding_count']}")

    if args.fail_on and SEVERITY_ORDER[report["severity"]] >= SEVERITY_ORDER[args.fail_on]:
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
