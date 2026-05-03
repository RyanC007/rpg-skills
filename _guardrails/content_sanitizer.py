"""
RPG Universal Content Sanitizer
Scans and replaces banned phrasing, detects sensitive data leaks, and applies
output-tier guardrails across the RPG agent ecosystem.
"""

from __future__ import annotations

import re
from typing import Dict, List, Tuple

try:
    from guardrail_policy import Finding, max_severity
except ImportError:  # pragma: no cover
    from .guardrail_policy import Finding, max_severity

FORBIDDEN_BRAND_REPLACEMENTS = {
    r"(?i)shine\s+strategic\s+ops": "RPG",
    r"(?i)shine\s+enterprises": "Ready, Plan, Grow!",
    r"(?i)shine\s+ops": "RPG",
    r"(?i)shinestrategic": "RPG",
    r"(?i)shineenterprises": "ReadyPlanGrow",
}

LOGOCLOTHZ_REPLACEMENTS = {
    r"(?i)\bmade in the usa\b": "cut sewn and printed in the USA",
    r"(?i)\belevate\b": "",
    r"(?i)\belevates\b": "",
    r"(?i)\belevating\b": "",
    r"(?i)\belevated\b": "",
}

RPG_SLOP_REPLACEMENTS = {
    r"(?i)\bleverage\b": "use",
    r"(?i)\butilize\b": "use",
    r"(?i)\benhance\b": "improve",
    r"(?i)\btransform\b": "change",
    r"(?i)\boptimize\b": "improve",
    r"(?i)\bstreamline\b": "simplify",
    r"(?i)\bimplement\b": "start",
    r"(?i)\bempower\b": "help",
    r"(?i)\bcultivate\b": "build",
    r"(?i)\bfoster\b": "build",
    r"(?i)\bvibrant tapestry\b": "",
    r"(?i)\bin today'?s digital age\b": "today",
    r"(?i)\bgame[- ]changer\b": "big shift",
    r"(?i)\bgame[- ]changing\b": "important",
    r"(?i)\bout of the box\b": "",
    r"(?i)\bever-evolving landscape\b": "the way things work",
    r"(?i)\bnavigating the landscape\b": "the reality is",
    r"(?i)\bit'?s worth noting that\b": "also,",
    r"(?i)\bfurthermore\b": "also",
    r"(?i)\bnotably\b": "also",
    r"(?i)\bessentially\b": "basically",
    r"(?i)\bconsequently\b": "so",
    r"(?i)\bcrucial role in shaping\b": "important part of",
    r"(?i)\bpivotal\b": "important",
    r"(?i)\bintricate\b": "complex",
    r"(?i)\bobjective study aimed at\b": "we've seen",
    r"(?i)\bresearch needed to understand\b": "the numbers show",
    r"(?i)\bdespite facing\b": "even when",
    r"(?i)\btestament to\b": "proof that",
    r"(?i)\bdelve into\b": "look at",
    r"(?i)\bunderscore\b": "highlight",
    r"(?i)\brealm\b": "area",
    r"(?i)\bharness\b": "use",
    r"(?i)\billuminate\b": "show",
    r"(?i)\bfacilitate\b": "help",
    r"(?i)\brefine\b": "improve",
    r"(?i)\bbolster\b": "strengthen",
    r"(?i)\bdifferentiate\b": "stand out",
    r"(?i)\becosystem\b": "system",
    r"(?i)\brobust\b": "strong",
    r"(?i)\bdynamic\b": "active",
    r"(?i)\binnovative\b": "new",
    r"(?i)\bcutting-edge\b": "new",
    r"(?i)\btransformative\b": "major",
    r"(?i)\brevolutionize\b": "change",
    r"(?i)\bscalable solution\b": "solution",
    r"(?i)\bseamless integration\b": "integration",
    r"(?i)\bthat being said\b": "but",
    r"(?i)\bat its core\b": "basically",
    r"(?i)\bto put it simply\b": "simply put",
    r"(?i)\bthis underscores the importance of\b": "this shows why",
    r"(?i)\ba key takeaway is\b": "the main point is",
    r"(?i)\bgenerally speaking\b": "",
    r"(?i)\btypically\b": "",
    r"(?i)\btends to\b": "",
    r"(?i)\barguably\b": "",
    r"(?i)\bto some extent\b": "",
    r"(?i)\bbroadly speaking\b": "",
    r"(?i)\bvisibility that compounds\b": "growing visibility",
    r"(?i)\bholistic growth\b": "growth",
    r"(?i)\bstrategic alignment\b": "alignment",
    r"(?i)\bintentional execution\b": "execution",
    r"—": " - ",
    r"–": " - ",
}

SECRET_PATTERNS: List[Tuple[str, str, str]] = [
    ("OUT_OPENAI_KEY", "critical", r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    ("OUT_GITHUB_TOKEN", "critical", r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    ("OUT_GOOGLE_API_KEY", "critical", r"\bAIza[0-9A-Za-z_-]{20,}\b"),
    ("OUT_PRIVATE_KEY", "critical", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ("OUT_ENV_ASSIGNMENT", "high", r"(?im)^\s*[A-Z0-9_]{3,}\s*=\s*['\"]?[^\s'\"]{12,}"),
    ("OUT_PASSWORD", "high", r"(?is)\b(password|passwd|pwd|secret|token)\b\s*[:=]\s*[^\s`]{8,}"),
]

TIER_PATTERNS: Dict[str, List[Tuple[str, str, str, str]]] = {
    "tier1": [
        ("OUT_DRIVE_LINK", "high", "sensitive_link", r"https://drive\.google\.com/[^\s)]+|https://docs\.google\.com/[^\s)]+"),
        ("OUT_GITHUB_LINK", "high", "repo_reference", r"https://github\.com/RyanC007/[^\s)]+|\bRyanC007/[A-Za-z0-9_.-]+\b"),
        ("OUT_LOCAL_PATH", "medium", "internal_path", r"/home/ubuntu/[^\s)]+"),
        ("OUT_MANUS_LINK", "medium", "internal_link", r"https?://[^\s)]*manus[^\s)]*"),
        ("OUT_AGENT_INTERNALS", "medium", "agent_internals", r"(?i)\b(system prompt|developer instructions|tool schema|MCP server|Drive folder ID|Shared Drive ID)\b"),
    ],
    "tier2": [
        ("OUT_GITHUB_LINK", "high", "repo_reference", r"https://github\.com/RyanC007/[^\s)]+|\bRyanC007/[A-Za-z0-9_.-]+\b"),
        ("OUT_LOCAL_PATH", "medium", "internal_path", r"/home/ubuntu/[^\s)]+"),
        ("OUT_INTERNAL_COST", "high", "internal_cost", r"(?i)\b(internal rate|internal cost|agent cost|margin|profit margin)\b"),
    ],
    "tier3": [],
}

CLIENT_NAME_PATTERNS = [
    r"\bElite Design Group\b",
    r"\bLogoclothz\b",
    r"\bXL Real Estate\b",
    r"\bFood Design Associates\b",
]


def sanitize_content(text: str, is_logoclothz: bool = False, tier: str = "tier3", client_name: str | None = None, return_report: bool = False):
    if not text:
        return (text, {"severity": "clean", "findings": []}) if return_report else text

    sanitized_text = text
    findings: List[Finding] = []

    for pattern, replacement in FORBIDDEN_BRAND_REPLACEMENTS.items():
        sanitized_text = re.sub(pattern, replacement, sanitized_text)

    for pattern, replacement in RPG_SLOP_REPLACEMENTS.items():
        sanitized_text = re.sub(pattern, replacement, sanitized_text)

    if is_logoclothz:
        for pattern, replacement in LOGOCLOTHZ_REPLACEMENTS.items():
            sanitized_text = re.sub(pattern, replacement, sanitized_text)

    for code, severity, pattern in SECRET_PATTERNS:
        for match in re.finditer(pattern, sanitized_text):
            findings.append(Finding(code, severity, "secret_leak", "Potential secret or credential detected in output.", match.group(0)[:120], "Remove the secret before delivery."))
            sanitized_text = re.sub(pattern, "[REDACTED_SECRET]", sanitized_text)

    tier_key = normalize_tier(tier)
    for code, severity, category, pattern in TIER_PATTERNS.get(tier_key, []):
        for match in re.finditer(pattern, sanitized_text):
            findings.append(Finding(code, severity, category, f"Output violates {tier_key} guardrail: {category}.", match.group(0)[:160], "Remove, generalize, or move to an internal-only note."))

    if tier_key == "tier1":
        for pattern in CLIENT_NAME_PATTERNS:
            for match in re.finditer(pattern, sanitized_text):
                findings.append(Finding("OUT_CLIENT_NAME_PUBLIC", "high", "client_privacy", "Client name found in public outbound output.", match.group(0), "Replace with 'a client' or 'a business we work with'."))
                sanitized_text = re.sub(pattern, "a client", sanitized_text)

    if tier_key == "tier2" and client_name:
        for pattern in CLIENT_NAME_PATTERNS:
            for match in re.finditer(pattern, sanitized_text):
                if match.group(0).lower() != client_name.lower():
                    findings.append(Finding("OUT_OTHER_CLIENT_NAME", "high", "client_privacy", "Another client name appears in a client-facing deliverable.", match.group(0), "Remove the unrelated client reference."))
                    sanitized_text = re.sub(pattern, "another client", sanitized_text)

    sanitized_text = re.sub(r" {2,}", " ", sanitized_text)
    sanitized_text = re.sub(r" \.", ".", sanitized_text)
    sanitized_text = re.sub(r" ,", ",", sanitized_text)
    sanitized_text = sanitized_text.strip()

    report = {
        "tier": tier_key,
        "severity": max_severity(findings),
        "finding_count": len(findings),
        "findings": [f.to_dict() for f in findings],
    }
    return (sanitized_text, report) if return_report else sanitized_text


def normalize_tier(tier: str) -> str:
    value = str(tier or "tier3").lower().replace(" ", "")
    if value in {"1", "public", "publicoutbound", "tier1"}:
        return "tier1"
    if value in {"2", "client", "clientfacing", "tier2"}:
        return "tier2"
    return "tier3"
