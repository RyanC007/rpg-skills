---
name: rpg-lgz-profit-analyzer
description: Logoclothz monthly profit analysis. Use when Ryan asks to analyze sales data, calculate real profit, or understand cost breakdown. This skill guides Morpheus through collecting all required inputs (sales CSV, InXpress PDFs, Braintree fee report, PayPal statements) and produces a fully enriched, hyperlinked profit spreadsheet with visualizations.
---

# Logoclothz Monthly Profit Analyzer

**OUTPUT_TIER: 3 (Internal - Logoclothz only)**

**Access Restriction: Morpheus-access only. Not available to Scarlett, Trinity, or Thor.**

This skill guides Morpheus through the process of creating the comprehensive monthly profit analysis spreadsheet for Logoclothz. It automates data extraction, enrichment, and visualization, culminating in a hyperlinked Excel report.

## Workflow Overview

The process involves these 5 steps:

1.  **Collect Inputs**: Prompt Ryan for all necessary files for the month.
2.  **Parse Shipping Costs**: Extract per-PO shipping costs from all InXpress PDF invoices.
3.  **Parse Transaction Fees**: Extract exact fees from the Braintree transaction report and determine the effective PayPal rate from merchant statements.
4.  **Build Master Spreadsheet**: Run the main script to merge all data sources, calculate real profit, and create the multi-tab Excel file.
5.  **Add Hyperlinks & Deliver**: Run the final script to add Google Drive and UPS hyperlinks to the spreadsheet and deliver it to Ryan.

---

## Step 1: Collect Inputs

At the start of the task, you MUST ask Ryan for the following files for the month being analyzed. Use the `message` tool with `ask` type. **Do not proceed until you have all files.**

> "Ryan, to build the monthly profit report, I need the following files for [Month Year]:
> 
> 1.  The **monthly sales data CSV** from the website admin.
> 2.  All **weekly InXpress shipping invoice PDFs** for the month.
> 3.  The **Braintree transaction-level fee report CSV**.
> 4.  The **PayPal monthly statement PDF** (if any custom orders were paid via PayPal)."

All uploaded files will be in `/home/ubuntu/upload/`. Note their paths for the next steps.

## Step 2: Parse Shipping Costs

This step uses `pdftotext` to extract data from all InXpress PDFs and a Python script to parse the output.

1.  **Find all InXpress PDFs**: Use `find /home/ubuntu/upload -name "*inxpress*.pdf"` to get a list of the PDF files.
2.  **Extract text**: For each PDF, run `pdftotext "/path/to/invoice.pdf" "/tmp/inxpress_N.txt"`.
3.  **Parse text files**: Run the `scripts/parse_inxpress.py` script. It will read all `/tmp/inxpress_*.txt` files and create `/tmp/shipping_costs.json` containing a dictionary of `{"PO_Number": cost}`.

```bash
# Example commands
find /home/ubuntu/upload -name "*inxpress*.pdf" -exec sh -c \
    'pdftotext "{}" "/tmp/inxpress_$(basename "{}" .pdf).txt"' \;
python3 /home/ubuntu/skills/rpg-lgz-profit-analyzer/scripts/parse_inxpress.py
```

## Step 3: Parse Transaction Fees

This step extracts fee data from the Braintree CSV and PayPal PDFs.

1.  **Braintree**: The main build script handles the Braintree CSV directly. Note the path to `/home/ubuntu/upload/transaction_level_fee_report_*.csv`.
2.  **PayPal**: If a PayPal statement PDF is provided, run the `scripts/parse_paypal.py` script on it. This will determine the effective flat-rate fee percentage.

```bash
# Example command if PayPal statement is present
python3 /home/ubuntu/skills/rpg-lgz-profit-analyzer/scripts/parse_paypal.py /home/ubuntu/upload/WW*.PDF
# The script will print the detected rate. Note this for the main build script.
```

## Step 4: Build Master Spreadsheet

This is the core step. The `scripts/build_master.py` script takes all the data sources and builds the main Excel file.

-   **Modify the script**: You may need to edit the `build_master.py` script to update the file paths for the sales CSV and Braintree report, and to input the correct PayPal fee rate if it was derived in the previous step.
-   **Run the script**: Execute the script. It will create the master spreadsheet in `/home/ubuntu/upload/`.

```bash
# Edit paths in the script first, then run:
python3 /home/ubuntu/skills/rpg-lgz-profit-analyzer/scripts/build_master.py
```

## Step 5: Add Hyperlinks & Deliver

This final step adds the Google Drive and UPS hyperlinks to the spreadsheet.

1.  **Get Drive folder map**: The `scripts/get_drive_folders.py` script will query the shared Google Drive folder and create `/tmp/drive_folder_map.json`.
2.  **Run hyperlink script**: The `scripts/build_hyperlinked_sheet.py` script reads the master spreadsheet and the folder map, and writes a new `_LINKED.xlsx` version with all hyperlinks.
3.  **Deliver**: Upload the final `_LINKED.xlsx` file to the `Logoclothz/Financial Reports/` folder in Google Drive and send the shareable link to Ryan using the `message` tool with `result` type.

```bash
# Run the scripts in order
python3 /home/ubuntu/skills/rpg-lgz-profit-analyzer/scripts/get_drive_folders.py
python3 /home/ubuntu/skills/rpg-lgz-profit-analyzer/scripts/build_hyperlinked_sheet.py

# Then upload and deliver the final file
rclone copy "/home/ubuntu/upload/Logoclothz_..._LINKED.xlsx" "manus_google_drive:Logoclothz/Financial Reports/" ...
rclone link "manus_google_drive:Logoclothz/Financial Reports/Logoclothz_..._LINKED.xlsx" ...
```
