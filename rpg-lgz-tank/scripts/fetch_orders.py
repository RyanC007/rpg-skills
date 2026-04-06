#!/usr/bin/env python3
"""
Tank — Logoclothz BigCommerce Orders Fetcher
============================================
Pulls all orders from a specified date range (default: last 3 days).
Enriches each order with product details and shipping address.
Outputs a clean summary report to stdout and saves raw JSON to disk.

Usage:
    python3 fetch_orders.py                  # Last 3 days
    python3 fetch_orders.py --days 7         # Last 7 days
    python3 fetch_orders.py --since 2026-03-01  # Since a specific date

Output:
    - Console: Formatted order table + status breakdown + action flags
    - File: orders_raw.json (in current directory)
"""

import requests
import json
import argparse
from datetime import datetime, timezone, timedelta
from collections import Counter

# ─────────────────────────────────────────────
# CREDENTIALS (stored in Google Drive — do not hardcode in external files)
# ─────────────────────────────────────────────
BC_STORE = "dw57ootmu7"
BC_TOKEN = "o1dhpea9cz5zuvqjcr8cc6imoufzcxr"
HEADERS = {
    "X-Auth-Token": BC_TOKEN,
    "Accept": "application/json",
    "Content-Type": "application/json"
}
BASE_URL = f"https://api.bigcommerce.com/stores/{BC_STORE}/v2"


def fetch_orders(min_date_str: str) -> list:
    """Fetch all orders since min_date_str with pagination."""
    all_orders = []
    page = 1
    while True:
        params = {
            "min_date_created": min_date_str,
            "limit": 250,
            "page": page,
            "sort": "date_created:desc"
        }
        resp = requests.get(f"{BASE_URL}/orders", headers=HEADERS, params=params)
        if resp.status_code in (204, 404):
            break
        if resp.status_code != 200:
            print(f"[ERROR] Fetching orders: HTTP {resp.status_code} — {resp.text}")
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
    """Fetch product line items for a specific order."""
    resp = requests.get(f"{BASE_URL}/orders/{order_id}/products", headers=HEADERS)
    if resp.status_code == 200:
        return resp.json()
    return []


def fetch_shipping_address(order_id: int) -> dict:
    """Fetch the shipping address for a specific order."""
    resp = requests.get(f"{BASE_URL}/orders/{order_id}/shipping_addresses", headers=HEADERS)
    if resp.status_code == 200:
        data = resp.json()
        return data[0] if data else {}
    return {}


def enrich_orders(raw_orders: list) -> list:
    """Enrich each order with product details, shipping address, and art file info."""
    enriched = []
    for order in raw_orders:
        products = fetch_order_products(order["id"])
        shipping = fetch_shipping_address(order["id"])

        product_lines = []
        art_files = []
        product_options_summary = []

        for p in products:
            qty = p.get("quantity", 1)
            name = p.get("name", "Unknown Product")
            sku = p.get("sku", "")
            price = float(p.get("base_price", 0))
            product_lines.append(f"{name} (SKU: {sku}, Qty: {qty}, Price: ${price:.2f})")

            # Extract product options (fabric color, production time, art file, etc.)
            for opt in p.get("product_options", []):
                display_name = opt.get("display_name", "")
                display_value = opt.get("display_value", "")
                if "Art" in display_name or "Upload" in display_name:
                    art_files.append(display_value)
                else:
                    product_options_summary.append(f"{display_name}: {display_value}")

        billing = order.get("billing_address", {})
        customer_name = f"{billing.get('first_name', '')} {billing.get('last_name', '')}".strip()

        enriched.append({
            "order_id": order["id"],
            "date_created": order["date_created"],
            "customer_name": customer_name,
            "customer_email": billing.get("email", ""),
            "company": billing.get("company", ""),
            "status": order["status"],
            "custom_status": order.get("custom_status", ""),
            "total": float(order["total_inc_tax"]),
            "subtotal": float(order["subtotal_inc_tax"]),
            "shipping_cost": float(order.get("shipping_cost_inc_tax", 0)),
            "payment_method": order.get("payment_method", ""),
            "payment_status": order.get("payment_status", ""),
            "items_total": order.get("items_total", 0),
            "items_shipped": order.get("items_shipped", 0),
            "products": product_lines,
            "product_options": product_options_summary,
            "art_files": art_files,
            "ship_to_name": f"{shipping.get('first_name', '')} {shipping.get('last_name', '')}".strip(),
            "ship_to_company": shipping.get("company", ""),
            "ship_to_address": f"{shipping.get('street_1', '')}, {shipping.get('city', '')}, {shipping.get('state', '')} {shipping.get('zip', '')}",
            "ship_to_country": shipping.get("country", ""),
            "shipping_method": shipping.get("shipping_method", ""),
        })
    return enriched


def print_report(orders: list, now: datetime, min_date: datetime):
    """Print a formatted order report to stdout."""
    total_revenue = sum(o["total"] for o in orders)
    confirmed_orders = [o for o in orders if o["status"] != "Incomplete"]
    confirmed_revenue = sum(o["total"] for o in confirmed_orders)

    print(f"\n{'='*110}")
    print(f"  LOGOCLOTHZ — ORDER REPORT")
    print(f"  Period: {min_date.strftime('%b %d, %Y %I:%M %p UTC')} → {now.strftime('%b %d, %Y %I:%M %p UTC')}")
    print(f"{'='*110}")
    print(f"  Total Orders: {len(orders)}   |   Total Revenue: ${total_revenue:,.2f}   |   "
          f"Confirmed Revenue (excl. Incomplete): ${confirmed_revenue:,.2f}")
    print(f"{'='*110}")
    print(f"{'Order #':<12} {'Date (UTC)':<30} {'Customer':<25} {'Status':<25} {'Total':>10}")
    print(f"{'-'*110}")

    for o in orders:
        print(f"#{o['order_id']:<11} {o['date_created']:<30} {o['customer_name']:<25} {o['status']:<25} ${o['total']:>9.2f}")

    print(f"{'-'*110}")
    print(f"{'TOTAL':<68} ${total_revenue:>9.2f}")
    print(f"{'='*110}")

    # Status breakdown
    status_counts = Counter(o["status"] for o in orders)
    print(f"\n  STATUS BREAKDOWN:")
    for status, count in status_counts.most_common():
        rev = sum(o["total"] for o in orders if o["status"] == status)
        print(f"    {status:<35} {count:>3} orders   ${rev:>10,.2f}")

    # Action flags
    incomplete_customers = {}
    for o in orders:
        if o["status"] == "Incomplete":
            incomplete_customers[o["customer_name"]] = incomplete_customers.get(o["customer_name"], 0) + 1

    if incomplete_customers or any(o["status"] == "Awaiting Pickup" for o in orders):
        print(f"\n  ACTION FLAGS:")
        for name, count in incomplete_customers.items():
            if count > 1:
                print(f"    ⚑  {name} has {count} Incomplete orders — possible checkout friction. Consider direct outreach.")
        for o in orders:
            if o["status"] == "Awaiting Pickup":
                print(f"    ⚑  Order #{o['order_id']} ({o['customer_name']}) — Awaiting Pickup. Follow up to confirm.")

    print(f"\n  Report generated at: {now.strftime('%B %d, %Y %I:%M %p UTC')}")
    print(f"{'='*110}\n")


def main():
    parser = argparse.ArgumentParser(description="Fetch Logoclothz BigCommerce orders")
    parser.add_argument("--days", type=int, default=3, help="Number of days back to fetch (default: 3)")
    parser.add_argument("--since", type=str, default=None, help="Fetch orders since this date (YYYY-MM-DD)")
    parser.add_argument("--output", type=str, default="orders_raw.json", help="Output JSON file path")
    args = parser.parse_args()

    now = datetime.now(timezone.utc)

    if args.since:
        min_date = datetime.strptime(args.since, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    else:
        min_date = now - timedelta(days=args.days)

    min_date_str = min_date.strftime("%Y-%m-%dT%H:%M:%S+00:00")

    print(f"[Tank] Fetching orders from BigCommerce...")
    print(f"[Tank] Range: {min_date_str} → now")

    raw_orders = fetch_orders(min_date_str)
    print(f"[Tank] Found {len(raw_orders)} orders. Enriching with product and shipping details...")

    enriched = enrich_orders(raw_orders)

    with open(args.output, "w") as f:
        json.dump(enriched, f, indent=2)
    print(f"[Tank] Raw data saved to: {args.output}")

    print_report(enriched, now, min_date)


if __name__ == "__main__":
    main()
