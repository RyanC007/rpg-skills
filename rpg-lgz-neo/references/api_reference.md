# Rpg Lgz Neo — SEO & BigCommerce API Reference

**Version:** 1.0
**Last Updated:** March 18, 2026

---

## 1. Authentication

Neo interacts with the BigCommerce Storefront API to pull product data for optimization, and the Google Search Console API for reporting.

### BigCommerce API
All requests must include the following headers:

| Header | Value |
|---|---|
| `X-Auth-Token` | `o1dhpea9cz5zuvqjcr8cc6imoufzcxr` |
| `Accept` | `application/json` |
| `Content-Type` | `application/json` |

The Store Hash is `dw57ootmu7`.
**Base URL:** `https://api.bigcommerce.com/stores/dw57ootmu7/`

### Google Search Console API
Neo uses standard OAuth 2.0 or Service Account credentials to access the Google Search Console API.
**Base URL:** `https://www.googleapis.com/webmasters/v3/`

---

## 2. Core Workflows & Endpoints

### 2.1. Product Page Optimization (BigCommerce)

#### **Step 1: Fetch Product Data**
- **Endpoint:** `GET /v3/catalog/products/{product_id}`
- **Purpose:** Retrieve current title, meta description, and product description.
- **Key Parameters:**
    - `include`: `variants,images,custom_fields`
- **Example Request:**
  ```bash
  curl -s "https://api.bigcommerce.com/stores/dw57ootmu7/v3/catalog/products/123?include=images" \
    -H "X-Auth-Token: o1dhpea9cz5zuvqjcr8cc6imoufzcxr" \
    -H "Accept: application/json"
  ```

#### **Step 2: Update Product SEO Metadata**
- **Endpoint:** `PUT /v3/catalog/products/{product_id}`
- **Purpose:** Update the product with optimized SEO data.
- **Example Payload:**
  ```json
  {
    "page_title": "Custom Embroidered Polo Shirts | Logoclothz",
    "meta_description": "Shop custom embroidered polo shirts for your team. Cut sewn and printed in the USA. Fast turnaround and bulk pricing available.",
    "description": "<p>Optimized product description here...</p>"
  }
  ```

### 2.2. Weekly SEO Report (Google Search Console)

#### **Query Search Analytics**
- **Endpoint:** `POST /sites/{siteUrl}/searchAnalytics/query`
- **Purpose:** Retrieve clicks, impressions, CTR, and position data.
- **Example Payload:**
  ```json
  {
    "startDate": "2026-03-11",
    "endDate": "2026-03-18",
    "dimensions": ["page", "query"],
    "rowLimit": 100
  }
  ```
