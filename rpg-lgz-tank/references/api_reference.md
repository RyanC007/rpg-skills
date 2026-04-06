# Rpg Lgz Tank — BigCommerce API Reference

**Version:** 1.0
**Last Updated:** March 16, 2026

---

## 1. Authentication

Tank authenticates to the BigCommerce Storefront API using a permanent API Account token. All requests must include the following headers:

| Header | Value |
|---|---|
| `X-Auth-Token` | `o1dhpea9cz5zuvqjcr8cc6imoufzcxr` |
| `Accept` | `application/json` |
| `Content-Type` | `application/json` |

The Store Hash is `dw57ootmu7`.

**Base URL:** `https://api.bigcommerce.com/stores/dw57ootmu7/`

---

## 2. Core Workflows & Endpoints

Tank's primary responsibilities involve monitoring orders, managing products, and reporting on store performance. The following endpoints are critical to these functions.

### 2.1. Order Management

This workflow is the core of Tank's function: pulling new orders, gathering all necessary data, and preparing it for production.

#### **Step 1: Fetch New Orders**

Tank polls for new orders using the `min_date_created` filter to get only the latest.

- **Endpoint:** `GET /v2/orders`
- **Purpose:** Retrieve a list of orders, sorted by creation date.
- **Key Parameters:**
    - `min_date_created`: (string, ISO 8601) The earliest date to fetch orders from.
    - `sort`: (string) `date_created:desc`
    - `limit`: (integer) `250` (max)
    - `page`: (integer) For paginating through results.
- **Example Request:**
  ```bash
  curl -s "https://api.bigcommerce.com/stores/dw57ootmu7/v2/orders?min_date_created=2026-03-13T00:00:00+00:00&sort=date_created:desc" \
    -H "X-Auth-Token: o1dhpea9cz5zuvqjcr8cc6imoufzcxr" \
    -H "Accept: application/json"
  ```

#### **Step 2: Get Order Products**

For each order, Tank retrieves the specific products that were purchased.

- **Endpoint:** `GET /v2/orders/{order_id}/products`
- **Purpose:** Get a list of all products associated with a specific order.
- **Example Request:**
  ```bash
  curl -s "https://api.bigcommerce.com/stores/dw57ootmu7/v2/orders/4203897/products" \
    -H "X-Auth-Token: o1dhpea9cz5zuvqjcr8cc6imoufzcxr" \
    -H "Accept: application/json"
  ```

#### **Step 3: Get Shipping Details**

Tank fetches the shipping address to determine the destination for the order.

- **Endpoint:** `GET /v2/orders/{order_id}/shipping_addresses`
- **Purpose:** Retrieve the shipping address(es) for an order.
- **Example Request:**
  ```bash
  curl -s "https://api.bigcommerce.com/stores/dw57ootmu7/v2/orders/4203897/shipping_addresses" \
    -H "X-Auth-Token: o1dhpea9cz5zuvqjcr8cc6imoufzcxr" \
    -H "Accept: application/json"
  ```

### 2.2. Product & Inventory Management

Tank can be tasked with updating product information or checking inventory levels.

#### **Get All Products**

- **Endpoint:** `GET /v3/catalog/products`
- **Purpose:** Retrieve a complete list of all products in the Logoclothz catalog.
- **Key Parameters:**
    - `limit`: (integer) `250` (max)
    - `include`: (string) `variants,images,custom_fields`
- **Example Request:**
  ```bash
  curl -s "https://api.bigcommerce.com/stores/dw57ootmu7/v3/catalog/products?limit=5" \
    -H "X-Auth-Token: o1dhpea9cz5zuvqjcr8cc6imoufzcxr" \
    -H "Accept: application/json"
  ```

#### **Update a Product**

- **Endpoint:** `PUT /v3/catalog/products/{product_id}`
- **Purpose:** Update properties of a specific product, such as price, description, or weight.
- **Request Body:** A JSON object containing the fields to be updated.
- **Example Request (updating weight):
  ```bash
  curl -s -X PUT "https://api.bigcommerce.com/stores/dw57ootmu7/v3/catalog/products/123" \
    -H "X-Auth-Token: o1dhpea9cz5zuvqjcr8cc6imoufzcxr" \
    -H "Accept: application/json" \
    -d '{"weight": 7.5}'
  ```

### 2.3. Store Reporting

Tank can generate reports on store performance.

#### **Get Store Information**

- **Endpoint:** `GET /v2/store`
- **Purpose:** Retrieve general information about the BigCommerce store.
- **Note:** The current API token `o1dhpea9cz5zuvqjcr8cc6imoufzcxr` **does not have the scope** for this endpoint. It will return a 403 Forbidden error. This is expected behavior.

---

## 3. Data Structures (Key Fields)

Below are the key JSON fields Tank relies on from the API responses.

### Order Object (`/v2/orders`)

```json
{
  "id": 4203897,
  "customer_id": 2427,
  "date_created": "Mon, 16 Mar 2026 20:11:55 +0000",
  "status": "Partially Shipped",
  "custom_status": "Proof approved...",
  "total_inc_tax": "189.9900",
  "payment_method": "Pay With Credit / Debit Card",
  "payment_status": "captured",
  "billing_address": {
    "first_name": "Patrick",
    "last_name": "Baldwin",
    "email": "patrick@fraxn.com",
    "company": "FRAXN"
  }
}
```

### Order Product Object (`/v2/orders/{id}/products`)

```json
{
  "id": 4020,
  "order_id": 4203897,
  "product_id": 111,
  "name": "Custom Table Throw - 6 Foot...",
  "sku": "6FT-FDS-THROW",
  "quantity": 1,
  "base_price": "189.9900",
  "product_options": [
    {
      "display_name": "Art File Upload",
      "display_value": "artfile.ai",
      "value": "{\"originalName\":\"artfile.ai\",\"path\":\"order-attribute-xyz.ai\"}"
    }
  ]
}
```

### Shipping Address Object (`/v2/orders/{id}/shipping_addresses`)

```json
{
  "id": 3360,
  "order_id": 4203897,
  "first_name": "Patrick",
  "last_name": "Baldwin",
  "company": "FRAXN",
  "street_1": "1104 Knightsbridge Rd",
  "city": "Waco",
  "state": "Texas",
  "zip": "76712",
  "country": "United States",
  "email": "patrick@fraxn.com",
  "shipping_method": "Free Shipping"
}
```
