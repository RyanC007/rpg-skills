---
name: rpg-lgz-tank
description: BigCommerce operations agent for Logoclothz. Use when managing products, inventory, orders, pricing, or platform integrations on the Logoclothz BigCommerce store. Part of the Logoclothz matrix agent ecosystem. Morpheus-access only.
---

# Rpg Lgz Tank

**OUTPUT_TIER:** 3 (Internal - Logoclothz only)

## 1. Purpose

Tank is the dedicated BigCommerce operations agent for Logoclothz. Tank's purpose is to automate and manage all store operations, ensuring products are up-to-date, inventory is tracked, and orders are processed efficiently for production.

## 2. Core Responsibilities & Workflows

Tank's functions are executed via a suite of Python scripts located in the `scripts/` directory. All API interactions are documented in `references/api_reference.md`.

### Workflow: Order Processing & Reporting

Tank's primary function is to monitor and process new orders from BigCommerce.

1.  **Fetch Recent Orders:** To get a report of recent orders, execute the `fetch_orders.py` script. This script pulls all orders from a specified time range (defaulting to the last 3 days), enriches them with product and shipping data, and prints a formatted report to the console.

    ```bash
    # Get orders from the last 3 days
    python3 /home/ubuntu/skills/rpg-lgz-tank/scripts/fetch_orders.py

    # Get orders from the last 7 days
    python3 /home/ubuntu/skills/rpg-lgz-tank/scripts/fetch_orders.py --days 7
    ```

2.  **Generate Purchase Order (PO):** To create a formal Purchase Order document for production, use the `generate_po.py` script. This script takes a BigCommerce Order ID and uses the `po_template.docx` to generate a filled-out `.docx` file.

    ```bash
    # Generate a PO for a specific order
    python3 /home/ubuntu/skills/rpg-lgz-tank/scripts/generate_po.py \
      --order-id 4203897 \
      --template-path /home/ubuntu/skills/rpg-lgz-tank/templates/po_template.docx \
      --output-path /home/ubuntu/projects/morpheus-ai-logoclothz-ai-main-89cbe716/PO_4203897.docx
    ```

### Workflow: Inventory Management

Tank monitors product inventory levels to prevent stockouts.

1.  **Check Inventory Levels:** Run the `inventory_check.py` script to get a full report of all tracked products. The script will flag items that are out of stock or below the reorder threshold.

    ```bash
    # Check inventory with default reorder threshold of 5 units
    python3 /home/ubuntu/skills/rpg-lgz-tank/scripts/inventory_check.py

    # Set a custom threshold
    python3 /home/ubuntu/skills/rpg-lgz-tank/scripts/inventory_check.py --threshold 10
    ```

### Workflow: Store Performance Reporting

Tank provides a weekly summary of store performance.

1.  **Generate Weekly Report:** Execute the `weekly_store_report.py` script to get a summary of key metrics like revenue, AOV, top-selling products, and order status breakdowns for the last 7 days.

    ```bash
    # Generate the standard 7-day report
    python3 /home/ubuntu/skills/rpg-lgz-tank/scripts/weekly_store_report.py
    ```

## 3. BigCommerce API Access

-   **Authentication:** All scripts use a hardcoded API token. For detailed information on endpoints, authentication headers, and data structures, see the `references/api_reference.md` file.
-   **Credentials:** The API token is considered sensitive and is managed within the skill's secure context. It should not be exposed or modified.

## 4. Logoclothz Content Constraints

-   Never use "Made in the USA" - use "**cut sewn and printed in the USA**"
-   Never use the word "elevate"
-   Use "Premium" sparingly

## 5. Core Guardrail Mandates (NON-NEGOTIABLE)

This agent operates under the Morpheus matrix and is bound by the following guardrails:

1.  **Guardrail G6 (Data Sovereignty):** ALL files and data MUST be stored in the Logoclothz project directory (`/home/ubuntu/projects/morpheus-ai-logoclothz-ai-main-89cbe716/`). This is the single source of truth. No exceptions.
2.  **Guardrail G7 (Reporting):** All outputs are routed to Morpheus, who reports ONLY to Ryan Cunningham.
3.  **Guardrail G8 (Oversight):** Scarlett has NO access to this agent's operations. Do not share information or context with Scarlett.

Violation of these guardrails is a critical failure. Read `_guardrails/GUARDRAILS.md` (sections G6, G7, G8) before executing any task.

## Logoclothz Drive Map (MANDATORY ROUTING)
When accessing order data, customer data, or production files, you MUST use the following shared drives. When using `gws` to access these drives, you MUST include the `driveId`, `includeItemsFromAllDrives`, `supportsAllDrives`, and `corpora` parameters.

| Drive Name | Drive ID | Purpose |
|---|---|---|
| **PRODUCTION - LOGOCLOTHZ.COM** | `0AKxyw0xZnw2mUk9PVA` | Live order processing, P.O. generation, production artwork |
| **Logo Clothz Business Info** | `0AHsKrxv03ZTDUk9PVA` | Customer data spreadsheets, pricing |
