#!/usr/bin/env python3
"""
Neo: Product Page Optimization Script
Fetches product data from BigCommerce, allows for SEO optimization, and updates the product.
"""

import argparse
import requests
import json
import sys
import os

# Add guardrails to path to import sanitizer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../_guardrails')))
from content_sanitizer import sanitize_content

# BigCommerce Configuration
STORE_HASH = "dw57ootmu7"
API_TOKEN = "o1dhpea9cz5zuvqjcr8cc6imoufzcxr"
BASE_URL = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v3"

HEADERS = {
    "X-Auth-Token": API_TOKEN,
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def fetch_product(product_id):
    """Fetches product details from BigCommerce."""
    url = f"{BASE_URL}/catalog/products/{product_id}?include=images"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json().get("data", {})
    else:
        print(f"Error fetching product {product_id}: {response.status_code} - {response.text}")
        sys.exit(1)

def update_product(product_id, payload):
    """Updates product SEO metadata in BigCommerce."""
    url = f"{BASE_URL}/catalog/products/{product_id}"
    response = requests.put(url, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        print(f"Successfully updated product {product_id}.")
        return response.json().get("data", {})
    else:
        print(f"Error updating product {product_id}: {response.status_code} - {response.text}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Optimize BigCommerce Product Page SEO")
    parser.add_argument("--product-id", required=True, help="BigCommerce Product ID")
    parser.add_argument("--title", help="New SEO Title Tag (under 60 chars)")
    parser.add_argument("--meta-desc", help="New Meta Description (under 160 chars)")
    parser.add_argument("--description", help="New Product Description (HTML)")
    
    args = parser.parse_args()
    
    print(f"Fetching product {args.product_id}...")
    product = fetch_product(args.product_id)
    
    print(f"Current Title: {product.get('page_title') or product.get('name')}")
    print(f"Current Meta: {product.get('meta_description')}")
    
    payload = {}
    if args.title:
        payload["page_title"] = sanitize_content(args.title, is_logoclothz=True)
    if args.meta_desc:
        payload["meta_description"] = sanitize_content(args.meta_desc, is_logoclothz=True)
    if args.description:
        payload["description"] = sanitize_content(args.description, is_logoclothz=True)
        
    if payload:
        print(f"Updating product {args.product_id} with sanitized SEO data...")
        update_product(args.product_id, payload)
    else:
        print("No update parameters provided. Exiting.")

if __name__ == "__main__":
    main()
