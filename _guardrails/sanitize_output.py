#!/usr/bin/env python3
"""
RPG Universal Content Sanitizer CLI
A command-line tool to sanitize text files before saving or publishing.
Enforces the RPG Master Content Standard and Logoclothz Brand Constraints.
"""

import argparse
import os
import sys
from content_sanitizer import sanitize_content

def main():
    parser = argparse.ArgumentParser(description="Sanitize a text file according to RPG guardrails.")
    parser.add_argument("--input", required=True, help="Path to the input file")
    parser.add_argument("--output", help="Path to save the sanitized file (defaults to overwriting input)")
    parser.add_argument("--logoclothz", action="store_true", help="Apply Logoclothz brand constraints")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)
        
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
        
    print(f"Sanitizing {args.input}...")
    if args.logoclothz:
        print("Applying Logoclothz brand constraints...")
        
    sanitized_content = sanitize_content(content, is_logoclothz=args.logoclothz)
    
    output_path = args.output if args.output else args.input
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(sanitized_content)
        print(f"Successfully sanitized and saved to {output_path}")
    except Exception as e:
        print(f"Error writing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
