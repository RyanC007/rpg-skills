#!/usr/bin/env python3
"""
Agent Smith: P&L Generation Script
Placeholder script for calculating monthly P&L based on revenue, COGS, and OpEx.
"""

import argparse
import json
from datetime import datetime

def calculate_pl(month, year, revenue, cogs, opex):
    """Calculates basic P&L metrics."""
    
    gross_profit = revenue - cogs
    gross_margin_pct = (gross_profit / revenue) * 100 if revenue > 0 else 0
    net_profit = gross_profit - opex
    net_margin_pct = (net_profit / revenue) * 100 if revenue > 0 else 0
    
    report = {
        "period": f"{month} {year}",
        "generated_at": datetime.now().isoformat(),
        "metrics": {
            "gross_revenue": round(revenue, 2),
            "cogs": round(cogs, 2),
            "gross_profit": round(gross_profit, 2),
            "gross_margin_pct": round(gross_margin_pct, 2),
            "operating_expenses": round(opex, 2),
            "net_profit": round(net_profit, 2),
            "net_margin_pct": round(net_margin_pct, 2)
        },
        "analysis": []
    }
    
    if gross_margin_pct < 40:
        report["analysis"].append("Warning: Gross margin is below the 40% target threshold. Review COGS or pricing.")
    if net_profit < 0:
        report["analysis"].append("Alert: Operating at a net loss for this period.")
        
    return report

def main():
    parser = argparse.ArgumentParser(description="Generate Monthly P&L Report")
    parser.add_argument("--month", required=True, help="Month (e.g., 'February')")
    parser.add_argument("--year", required=True, type=int, help="Year (e.g., 2026)")
    parser.add_argument("--revenue", required=True, type=float, help="Total Gross Revenue")
    parser.add_argument("--cogs", required=True, type=float, help="Total Cost of Goods Sold")
    parser.add_argument("--opex", required=True, type=float, help="Total Operating Expenses")
    parser.add_argument("--output", help="Path to save the JSON report")
    
    args = parser.parse_args()
    
    print(f"Generating P&L for {args.month} {args.year}...")
    report = calculate_pl(args.month, args.year, args.revenue, args.cogs, args.opex)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"P&L report saved to {args.output}")
    else:
        print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
