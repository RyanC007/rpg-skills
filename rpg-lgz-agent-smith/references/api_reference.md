# Rpg Lgz Agent Smith — Financial Intelligence API Reference

**Version:** 1.0
**Last Updated:** March 18, 2026

---

## 1. Overview

Agent Smith primarily relies on internal data sources (BigCommerce via Tank, Google Drive spreadsheets, and CSV exports) rather than external APIs. However, it may occasionally interact with BigCommerce for high-level revenue data.

---

## 2. BigCommerce API (Revenue Data)

Agent Smith uses the BigCommerce API to pull aggregate sales data for P&L reporting.

### 2.1. Authentication
All requests must include the following headers:

| Header | Value |
|---|---|
| `X-Auth-Token` | `o1dhpea9cz5zuvqjcr8cc6imoufzcxr` |
| `Accept` | `application/json` |
| `Content-Type` | `application/json` |

The Store Hash is `dw57ootmu7`.
**Base URL:** `https://api.bigcommerce.com/stores/dw57ootmu7/`

### 2.2. Fetch Orders for Revenue Calculation
- **Endpoint:** `GET /v2/orders`
- **Purpose:** Retrieve orders within a specific date range to calculate gross revenue.
- **Key Parameters:**
    - `min_date_created`: Start date (ISO 8601)
    - `max_date_created`: End date (ISO 8601)
    - `status_id`: Filter by completed statuses (e.g., 2 for Shipped, 10 for Completed)
- **Example Request:**
  ```bash
  curl -s "https://api.bigcommerce.com/stores/dw57ootmu7/v2/orders?min_date_created=2026-02-01T00:00:00Z&max_date_created=2026-02-28T23:59:59Z&status_id=10" \
    -H "X-Auth-Token: o1dhpea9cz5zuvqjcr8cc6imoufzcxr" \
    -H "Accept: application/json"
  ```

---

## 3. Internal Data Sources

Agent Smith relies heavily on the following internal files located in the Logoclothz Google Drive (`manus_google_drive:Logoclothz/Financial Reports/`):

1.  **COGS Database:** `Logoclothz_COGS_Master.xlsx` (Contains unit costs for all SKUs)
2.  **Operating Expenses:** `Logoclothz_OpEx_2026.xlsx` (Contains monthly fixed and variable costs)
3.  **Historical P&L:** `Logoclothz_PL_Master.xlsx` (Used for month-over-month and year-over-year comparisons)
