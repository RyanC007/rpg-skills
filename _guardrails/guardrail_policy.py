"""
RPG Agent Guardrail Policy
Shared constants and deterministic policy helpers for input sanitization,
prompt-injection detection, and output sanitization.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List

SEVERITY_ORDER = {"clean": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}

TRUST_LEVELS = {
    "trusted_internal": "Content created by the active RPG agent or explicitly approved by Ryan or Marcela.",
    "user_direct": "Direct instruction from the active human user in the current conversation.",
    "external_untrusted": "Websites, PDFs, emails, Slack messages, Drive docs, scraped pages, uploaded files, or copied text.",
    "unknown": "Content with unclear origin. Treat as external_untrusted until proven otherwise.",
}

SOURCE_DEFAULT_TRUST = {
    "user": "user_direct",
    "chat": "user_direct",
    "web": "external_untrusted",
    "website": "external_untrusted",
    "pdf": "external_untrusted",
    "file": "external_untrusted",
    "drive": "external_untrusted",
    "gmail": "external_untrusted",
    "email": "external_untrusted",
    "slack": "external_untrusted",
    "api": "external_untrusted",
    "unknown": "unknown",
}

OUTPUT_TIERS = {
    "tier1": "Public outbound. Strictest. No client names, internal links, repos, credentials, system details, or sensitive IDs.",
    "tier2": "Client-facing. Client name allowed only inside their own deliverable. No unrelated client names, repos, secrets, or internal costs.",
    "tier3": "Internal team. Full operational context allowed, but secrets, credentials, private keys, and system-prompt leakage remain blocked.",
}

@dataclass
class Finding:
    code: str
    severity: str
    category: str
    message: str
    matched_text: str = ""
    recommended_action: str = ""

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


def max_severity(findings: List[Finding]) -> str:
    if not findings:
        return "clean"
    return max((f.severity for f in findings), key=lambda s: SEVERITY_ORDER.get(s, 0))


def should_block(severity: str) -> bool:
    return SEVERITY_ORDER.get(severity, 0) >= SEVERITY_ORDER["critical"]


def requires_confirmation(severity: str) -> bool:
    return SEVERITY_ORDER.get(severity, 0) >= SEVERITY_ORDER["high"]


def trust_for_source(source: str) -> str:
    return SOURCE_DEFAULT_TRUST.get((source or "unknown").lower(), "unknown")
