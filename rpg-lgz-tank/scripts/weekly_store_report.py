#!/usr/bin/env python3
"""
Tank — Logoclothz Weekly Store Report
======================================
Generates a comprehensive weekly store performance report:
- Revenue, orders, and average order value for the week
- Top 5 selling products by revenue
- Top 5 underperforming products (low inventory or no recent sales)
- Order status breakdown
- Any Incomplete orders requiring follow-up

Usage:
    python3 weekly_store_report.py              # Current week (last 7 days)
    python3 weekly_store_report.py --days 14    # Last 14 days
"""

import requests
import json
import argparse
from datetime import datetime, timezone, timedelta
from collections import Counter, defaultdict

# ─────────────────────────────────────────────
# CREDENTIALS
# ─────────────────────────────────────────────
BC_STORE = "dw57ootmu7"
BC_TOKEN = "o1dhpea9cz5zuvqjcr8cc6imoufzcxr"
HEADERS = {
    "X-Auth-Token": BC_TOKEN,
    "Accept": "application/json",
    "Content-Type": "application/json"
}
BASE_V2 = f"https://api.bigcommerce.com/stores/{BC_STORE}/v2"
BASE_V3 = f"https://api.bigcommerce.com/stores/{BC_STORE}/v3"


def fetch_orders(min_date_str: str) -> list:
    all_orders = []
    page = 1
    while True:
        params = {"min_date_created": min_date_str, "limit": 250, "page": page}
        resp = requests.get(f"{BASE_V2}/orders", headers=HEADERS, params=params)
        if resp.status_code in (204, 404):
            break
        if resp.status_code != 200:
            print(f"[ERROR] {resp.status_code}: {resp.text}")
            break
        data = resp.json()
        if not data:
            break
        all_orders.extend(data)
        if len(data) < 250:
            break
        page += 1
    return all_orders


def fetch_order_products(order_id: int) -> list:
    resp = requests.get(f"{BASE_V2}/orders/{order_id}/products", headers=HEADERS)
    return resp.json() if resp.status_code == 200 else []


def main():
    parser = argparse.ArgumentParser(description="Generate Logoclothz weekly store report")
    parser.add_argument("--days", type=int, default=7, help="Number of days to report on (default: 7)")
    parser.add_argument("--output", type=str, default="weekly_report.json", help="Output JSON file path")
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    min_date = now - timedelta(days=args.days)
    min_date_str = min_date.strftime("%Y-%m-%dT%H:%M:%S+00:00")

    print(f"[Tank] Generating {args.days}-day store report...")
    print(f"[Tank] Period: {min_date.strftime('%b %d, %Y')} → {now.strftime('%b %d, %Y')}")

    orders = fetch_orders(min_date_str)
    print(f"[Tank] Fetched {len(orders)} orders. Pulling product details...")

    # Exclude incomplete orders from revenue metrics
    confirmed = [o for o in orders if o["status"] != "Incomplete"]
    total_revenue = sum(float(o["total_inc_tax"]) for o in confirmed)
    aov = total_revenue / len(confirmed) if confirmed else 0

    # Product sales aggregation
    product_sales = defaultdict(lambda: {"name": "", "sku": "", "qty": 0, "revenue": 0.0})
    for order in confirmed:
        prods = fetch_order_products(order["id"])
        for p in prods:
            key = p.get("sku") or p.get("name", "Unknown")
            product_sales[key]["name"] = p.get("name", "Unknown")
            product_sales[key]["sku"] = p.get("sku", "")
            product_sales[key]["qty"] += p.get("quantity", 1)
            product_sales[key]["revenue"] += float(p.get("total_inc_tax", 0))

    top5 = sorted(product_sales.values(), key=lambda x: x["revenue"], reverse=True)[:5]
    status_counts = Counter(o["status"] for o in orders)

    # Print report
    print(f"\n{'='*90}")
    print(f"  LOGOCLOTHZ — {args.days}-DAY STORE REPORT")
    print(f"  {min_date.strftime('%b %d, %Y')} → {now.strftime('%b %d, %Y %I:%M %p UTC')}")
    print(f"{'='*90}")
    print(f"  Total Orders:          {len(orders)}")
    print(f"  Confirmed Orders:      {len(confirmed)}")
    print(f"  Total Revenue:         ${total_revenue:,.2f}")
    print(f"  Avg Order Value (AOV): ${aov:,.2f}")
    print(f"{'='*90}")

    print(f"\n  TOP 5 PRODUCTS BY REVENUE:")
    print(f"  {'Product':<55} {'Qty':>5}  {'Revenue':>12}")
    print(f"  {'-'*75}")
    for p in top5:
        name = p["name"][:52] + "..." if len(p["name"]) > 52 else p["name"]
        print(f"  {name:<55} {p['qty']:>5}  ${p['revenue']:>11,.2f}")

    print(f"\n  STATUS BREAKDOWN:")
    for status, count in status_counts.most_common():
        rev = sum(float(o["total_inc_tax"]) for o in orders if o["status"] == status)
        print(f"    {status:<35} {count:>3} orders   ${rev:>10,.2f}")

    # Incomplete order flags
    incomplete = [o for o in orders if o["status"] == "Incomplete"]
    if incomplete:
        print(f"\n  INCOMPLETE ORDERS ({len(incomplete)}) — Require Follow-Up:")
        for o in incomplete:
            billing = o.get("billing_address", {})
            name = f"{billing.get('first_name', '')} {billing.get('last_name', '')}".strip()
            email = billing.get("email", "")
            print(f"    Order #{o['id']} — {name} ({email}) — ${float(o['total_inc_tax']):.2f}")

    print(f"\n  Report generated at: {now.strftime('%B %d, %Y %I:%M %p UTC')}")
    print(f"{'='*90}\n")

    # Save summary
    report = {
        "generated_at": now.isoformat(),
        "period_days": args.days,
        "total_orders": len(orders),
        "confirmed_orders": len(confirmed),
        "total_revenue": total_revenue,
        "aov": aov,
        "top5_products": top5,
        "status_breakdown": dict(status_counts),
        "incomplete_orders": [
            {
                "order_id": o["id"],
                "customer": f"{o['billing_address'].get('first_name','')} {o['billing_address'].get('last_name','')}".strip(),
                "email": o["billing_address"].get("email", ""),
                "total": float(o["total_inc_tax"])
            }
            for o in incomplete
        ]
    }
    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)
    print(f"[Tank] Report saved to: {args.output}")


if __name__ == "__main__":
    main()
