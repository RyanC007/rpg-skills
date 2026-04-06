#!/usr/bin/env python3
"""
Agent Smith: Product Margin Analysis Script
Placeholder script for analyzing margins on specific products or categories.
"""

import argparse
import json

def analyze_margins(products_data):
    """Analyzes margins for a list of products."""
    
    results = []
    for product in products_data:
        name = product.get("name", "Unknown")
        price = product.get("price", 0)
        cogs = product.get("cogs", 0)
        
        margin = price - cogs
        margin_pct = (margin / price) * 100 if price > 0 else 0
        
        status = "Healthy"
        if margin_pct < 30:
            status = "Critical - Review Pricing"
        elif margin_pct < 45:
            status = "Warning - Low Margin"
            
        results.append({
            "product": name,
            "price": price,
            "cogs": cogs,
            "gross_margin": round(margin, 2),
            "margin_percentage": round(margin_pct, 2),
            "status": status
        })
        
    # Sort by margin percentage (lowest first)
    results.sort(key=lambda x: x["margin_percentage"])
    return results

def main():
    parser = argparse.ArgumentParser(description="Analyze Product Margins")
    parser.add_argument("--input", required=True, help="Path to JSON file containing product data (name, price, cogs)")
    parser.add_argument("--output", help="Path to save the analysis report")
    
    args = parser.parse_args()
    
    try:
        with open(args.input, 'r') as f:
            products_data = json.load(f)
    except Exception as e:
        print(f"Error reading input file: {e}")
        return
        
    print(f"Analyzing margins for {len(products_data)} products...")
    analysis = analyze_margins(products_data)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"Analysis saved to {args.output}")
    else:
        print(json.dumps(analysis, indent=2))

if __name__ == "__main__":
    main()
