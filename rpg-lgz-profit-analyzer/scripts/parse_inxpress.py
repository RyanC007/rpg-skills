"""
parse_inxpress.py
-----------------
Reads all /tmp/inxpress_*.txt files (extracted from InXpress weekly invoice PDFs)
and builds a JSON dict of {PO_Number: shipping_cost}.

Output: /tmp/shipping_costs.json
"""

import re
import json
import glob

shipping_costs = {}

txt_files = sorted(glob.glob('/tmp/inxpress_*.txt'))
if not txt_files:
    print("No InXpress text files found in /tmp/. Run pdftotext on the PDFs first.")
    exit(1)

print(f"Parsing {len(txt_files)} InXpress invoice files...")

for fpath in txt_files:
    with open(fpath, 'r', errors='replace') as f:
        content = f.read()

    # InXpress invoices list shipments in blocks. Each block has a reference
    # (the PO number) and a total charge. The pattern varies slightly by invoice
    # version, so we try multiple approaches.

    # Approach 1: Look for lines with a PO-style reference followed by a dollar amount
    # Pattern: "4203803" or "P.O. 4203803" near a dollar amount on the same or next line
    blocks = re.split(r'\n{2,}', content)
    for block in blocks:
        # Find PO reference
        po_match = re.search(
            r'(?:P\.O\.?\s*)?(\d{7}[A-Z]?|[A-Z]{3,20}\d{0,4}[A-Z]?)\b',
            block
        )
        if not po_match:
            continue
        po = po_match.group(1).strip()

        # Find the charge amount — look for the last dollar amount in the block
        # InXpress shows "Net Charge" or "Total" near the amount
        amounts = re.findall(r'\$?\s*([\d,]+\.\d{2})', block)
        if not amounts:
            continue

        # Use the last amount in the block as the charge (usually the total)
        try:
            cost = float(amounts[-1].replace(',', ''))
        except ValueError:
            continue

        # Sanity check: shipping costs are typically $3–$200
        if 2.0 <= cost <= 500.0:
            if po in shipping_costs:
                # If PO appears in multiple invoices (split shipments), sum them
                shipping_costs[po] += cost
            else:
                shipping_costs[po] = cost

print(f"Found shipping costs for {len(shipping_costs)} PO numbers.")
for po, cost in sorted(shipping_costs.items()):
    print(f"  {po}: ${cost:.2f}")

with open('/tmp/shipping_costs.json', 'w') as f:
    json.dump(shipping_costs, f, indent=2)

print(f"\nSaved to /tmp/shipping_costs.json")
