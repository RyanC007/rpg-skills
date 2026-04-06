#!/usr/bin/env python3
"""
Morpheus: Task Routing Script
Analyzes a user request and determines which Logoclothz matrix agent should handle it.
"""

import argparse
import json

def determine_agent(task_description):
    """Basic keyword-based routing logic."""
    task_lower = task_description.lower()
    
    if any(kw in task_lower for kw in ["seo", "keyword", "meta", "search console", "rank"]):
        return "Neo (rpg-lgz-neo)"
    elif any(kw in task_lower for kw in ["inventory", "stock", "order", "bigcommerce", "product update"]):
        return "Tank (rpg-lgz-tank)"
    elif any(kw in task_lower for kw in ["lead", "outbound", "sdr", "prospect", "sequence", "email campaign"]):
        return "Link (rpg-lgz-link)"
    elif any(kw in task_lower for kw in ["blog", "post", "wordpress", "social", "caption", "content"]):
        return "Ghost (rpg-lgz-ghost)"
    elif any(kw in task_lower for kw in ["p&l", "profit", "margin", "revenue", "cost", "financial"]):
        return "Agent Smith (rpg-lgz-agent-smith)"
    else:
        return "Morpheus (Requires manual breakdown or cross-agent coordination)"

def main():
    parser = argparse.ArgumentParser(description="Route Task to Matrix Agent")
    parser.add_argument("--task", required=True, help="Description of the task to be routed")
    
    args = parser.parse_args()
    
    print(f"Analyzing task: '{args.task}'")
    agent = determine_agent(args.task)
    
    result = {
        "task": args.task,
        "assigned_agent": agent,
        "status": "Routed"
    }
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
