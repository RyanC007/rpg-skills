"""
parse_paypal.py
---------------
Reads a PayPal monthly merchant statement PDF and extracts:
- All payment transactions (gross, fee, net)
- The effective fee rate (fee / gross)

Usage: python3 parse_paypal.py /path/to/statement.pdf

Output: prints the effective rate and saves /tmp/paypal_rate.json
"""

import sys
import re
import json
import subprocess

if len(sys.argv) < 2:
    print("Usage: python3 parse_paypal.py /path/to/statement.pdf")
    sys.exit(1)

pdf_path = sys.argv[1]
txt_path = '/tmp/paypal_statement.txt'

# Extract text from PDF
result = subprocess.run(['pdftotext', pdf_path, txt_path], capture_output=True)
if result.returncode != 0:
    print(f"pdftotext failed: {result.stderr.decode()}")
    sys.exit(1)

with open(txt_path, 'r', errors='replace') as f:
    content = f.read()

# Find payment transaction rows: date, description, gross, fee, net
# PayPal statements typically have columns: Date | Description | Gross | Fee | Net
transactions = []
lines = content.split('\n')

for i, line in enumerate(lines):
    # Look for lines with dollar amounts that look like payment rows
    amounts = re.findall(r'-?\$?([\d,]+\.\d{2})', line)
    if len(amounts) >= 3:
        try:
            gross = float(amounts[0].replace(',', ''))
            fee   = float(amounts[1].replace(',', ''))
            net   = float(amounts[2].replace(',', ''))
            # Validate: fee should be negative or positive but smaller than gross
            if gross > 0 and 0 < abs(fee) < gross:
                transactions.append({'gross': gross, 'fee': abs(fee), 'net': net})
        except (ValueError, IndexError):
            continue

if not transactions:
    print("No transactions found. The statement format may differ from expected.")
    print("Defaulting to 3.157% PayPal rate (derived from Jan/Dec 2025-26 statements).")
    rate = 0.03157
else:
    total_gross = sum(t['gross'] for t in transactions)
    total_fees  = sum(t['fee']   for t in transactions)
    rate = total_fees / total_gross if total_gross > 0 else 0.03157
    print(f"Found {len(transactions)} transactions.")
    print(f"Total gross: ${total_gross:,.2f}")
    print(f"Total fees:  ${total_fees:,.2f}")
    print(f"Effective PayPal rate: {rate*100:.3f}%")

output = {'paypal_rate': rate, 'transaction_count': len(transactions)}
with open('/tmp/paypal_rate.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\nSaved to /tmp/paypal_rate.json")
print(f"Use rate: {rate:.5f} in build_master.py")
