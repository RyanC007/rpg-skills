#!/usr/bin/env python3
"""
Tank — Logoclothz BigCommerce Inventory Check
==============================================
Pulls all active products and their inventory levels.
Flags any products below the reorder threshold.
Outputs a report to stdout and saves raw JSON to disk.

Usage:
    python3 inventory_check.py                  # Default threshold: 5 units
    python3 inventory_check.py --threshold 10   # Custom reorder threshold
"""

import requests
import json
import argparse

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
BASE_URL = f"https://api.bigcommerce.com/stores/{BC_STORE}/v3"


def fetch_all_products() -> list:
    """Fetch all products from the catalog with pagination."""
    all_products = []
    page = 1
    while True:
        params = {
            "limit": 250,
            "page": page,
            "include": "variants"
        }
        resp = requests.get(f"{BASE_URL}/catalog/products", headers=HEADERS, params=params)
        if resp.status_code != 200:
            print(f"[ERROR] Fetching products: HTTP {resp.status_code} — {resp.text}")
            break
        data = resp.json().get("data", [])
        if not data:
            break
        all_products.extend(data)
        meta = resp.json().get("meta", {}).get("pagination", {})
        if page >= meta.get("total_pages", 1):
            break
        page += 1
    return all_products


def print_inventory_report(products: list, threshold: int):
    """Print a formatted inventory report."""
    low_stock = []
    out_of_stock = []
    healthy = []

    for p in products:
        if not p.get("inventory_tracking") or p["inventory_tracking"] == "none":
            continue
        qty = p.get("inventory_level", 0)
        name = p.get("name", "Unknown")
        sku = p.get("sku", "")
        pid = p.get("id")

        entry = {"id": pid, "name": name, "sku": sku, "qty": qty}
        if qty == 0:
            out_of_stock.append(entry)
        elif qty <= threshold:
            low_stock.append(entry)
        else:
            healthy.append(entry)

    print(f"\n{'='*80}")
    print(f"  LOGOCLOTHZ — INVENTORY REPORT  (Reorder Threshold: {threshold} units)")
    print(f"{'='*80}")
    print(f"  Total tracked products: {len(low_stock) + len(out_of_stock) + len(healthy)}")
    print(f"  Out of stock: {len(out_of_stock)}  |  Low stock: {len(low_stock)}  |  Healthy: {len(healthy)}")
    print(f"{'='*80}")

    if out_of_stock:
        print(f"\n  OUT OF STOCK:")
        for p in out_of_stock:
            print(f"    [ID:{p['id']}] {p['name']} (SKU: {p['sku']}) — QTY: 0")

    if low_stock:
        print(f"\n  LOW STOCK (≤ {threshold} units):")
        for p in sorted(low_stock, key=lambda x: x["qty"]):
            print(f"    [ID:{p['id']}] {p['name']} (SKU: {p['sku']}) — QTY: {p['qty']}")

    print(f"\n{'='*80}\n")


def main():
    parser = argparse.ArgumentParser(description="Check Logoclothz product inventory")
    parser.add_argument("--threshold", type=int, default=5, help="Reorder threshold (default: 5)")
    parser.add_argument("--output", type=str, default="inventory_raw.json", help="Output JSON file path")
    args = parser.parse_args()

    print(f"[Tank] Fetching product inventory from BigCommerce...")
    products = fetch_all_products()
    print(f"[Tank] Found {len(products)} products.")

    with open(args.output, "w") as f:
        json.dump(products, f, indent=2)
    print(f"[Tank] Raw data saved to: {args.output}")

    print_inventory_report(products, args.threshold)


if __name__ == "__main__":
    main()
