---
name: _guardrails
description: RPG universal content guardrails. Enforced automatically on all output. Defines three guardrail tiers (Public Outbound, Internal, Draft) with rules for tone, formatting, brand compliance, and content sanitization. Every skill must check the output destination and apply the correct tier. Includes Python sanitizer scripts.
---

# RPG Skill Guardrails

This skill defines the universal content guardrails applied to all RPG agent output. It is loaded automatically and should not need to be invoked manually.

## How It Works

1. Read `GUARDRAILS.md` for the full guardrail specification, including tier definitions and enforcement rules.
2. Before generating any content, determine the output destination (public, internal, or draft).
3. Apply the appropriate guardrail tier from `GUARDRAILS.md`.
4. For automated sanitization, use the `sanitize_output.py` script.

## Files

| File | Purpose |
| :--- | :--- |
| `GUARDRAILS.md` | Full guardrail specification with tiers and rules |
| `content_sanitizer.py` | Python module for automated content sanitization |
| `sanitize_output.py` | CLI script to sanitize output text |
