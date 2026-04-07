---
name: seven-economic-routing
description: Defines Seven's LLM routing rules for always choosing the cheapest viable model. Use when Seven (Ryan's super agent / top-level coordinator) needs to determine which LLM to call for any given task. Applies ONLY to Seven, not to other RPG agents.
---

# Seven Economic LLM Routing

OUTPUT_TIER: 3

This skill defines how Seven routes tasks to the cheapest viable LLM. Always start at the cheapest tier and only escalate when the task strictly requires it.

## Task-to-Model Mapping

| Task Type | Model | Tier |
| :--- | :--- | :--- |
| File scanning, Drive searches, basic lookups | Gemini 2.5 Flash | Cheapest |
| Summarization, content analysis, bulk processing | Gemini 2.5 Flash | Cheapest |
| Code generation, structured data, API integration | OpenAI GPT (standard) | Mid |
| Complex reasoning, multi-step analysis, high-stakes writing | Claude / GPT-4 | Premium |

## Escalation Rules

1. Default to Gemini 2.5 Flash for all tasks unless a specific need requires escalation.
2. Escalate to OpenAI GPT only when the task involves code, strict JSON/XML output, or complex API calls.
3. Escalate to premium models (Claude Opus, GPT-4) only when deep strategic reasoning, nuanced voice matching, or real-time web research is required.
4. If a cheaper model fails to produce a viable result, escalate one tier and retry.
5. Never ask the user for permission to use the cheaper model; route automatically.

## Approximate Pricing Reference

| Tier | Model | Input (per 1K tokens) | Output (per 1K tokens) |
| :--- | :--- | :--- | :--- |
| Cheapest | Gemini 2.5 Flash | Free / ~$0.00015 | Free / ~$0.0006 |
| Mid | OpenAI GPT (standard) | ~$0.001 - $0.01 | ~$0.002 - $0.03 |
| Premium | Claude / GPT-4 | ~$0.015 - $0.03 | ~$0.06 - $0.075 |

*(Prices are approximate. Check provider dashboards for current rates.)*

## Scope

These rules apply **only to Seven**. Do not apply them to Trinity, Scarlett, Thor, or any other RPG agent. Existing routing rules for all other agents remain unchanged.

## Full Reference

The full routing document is stored at:
- **Ryans-AI Drive:** `07_Seven/SEVEN_ECONOMIC_ROUTING.md`
