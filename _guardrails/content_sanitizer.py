#!/usr/bin/env python3
"""
RPG Universal Content Sanitizer
Automatically scans and removes/replaces banned words and phrases across the RPG ecosystem.
Enforces the RPG Master Content Standard and Logoclothz Brand Constraints.
"""

import re

# Layer 0: Forbidden Brand Names (Hard Block)
# These must NEVER appear in any RPG output. Replace with correct RPG branding.
FORBIDDEN_BRAND_REPLACEMENTS = {
    r"(?i)shine\s+strategic\s+ops": "RPG",
    r"(?i)shine\s+enterprises": "Ready, Plan, Grow!",
    r"(?i)shine\s+ops": "RPG",
    r"(?i)shinestrategic": "RPG",
    r"(?i)shineenterprises": "ReadyPlanGrow"
}

# Layer 1: Logoclothz Brand Constraints
LOGOCLOTHZ_REPLACEMENTS = {
    r"(?i)\bmade in the usa\b": "cut sewn and printed in the USA",
    r"(?i)\belevate\b": "",  # Remove entirely
    r"(?i)\belevates\b": "",
    r"(?i)\belevating\b": "",
    r"(?i)\belevated\b": ""
}

# Layer 2: RPG Master Content Standard (The Slop Blacklist)
# These are words/phrases that signal AI writing or corporate marketing language.
RPG_SLOP_REPLACEMENTS = {
    # Action Verbs
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
    
    # AI Clichés
    r"(?i)\bvibrant tapestry\b": "",
    r"(?i)\bin today'?s digital age\b": "today",
    r"(?i)\bgame changer\b": "big shift",
    r"(?i)\bgame-changer\b": "big shift",
    r"(?i)\bgame changing\b": "important",
    r"(?i)\bgame-changing\b": "important",
    r"(?i)\bout of the box\b": "",
    r"(?i)\bever-evolving landscape\b": "the way things work",
    r"(?i)\bnavigating the landscape\b": "the reality is",
    
    # Robotic Fillers
    r"(?i)\bit'?s worth noting that\b": "also,",
    r"(?i)\bfurthermore\b": "also",
    r"(?i)\bnotably\b": "also",
    r"(?i)\bessentially\b": "basically",
    r"(?i)\bconsequently\b": "so",
    r"(?i)\bcrucial role in shaping\b": "important part of",
    r"(?i)\bpivotal\b": "important",
    r"(?i)\bintricate\b": "complex",
    
    # Academic Fluff
    r"(?i)\bobjective study aimed at\b": "we've seen",
    r"(?i)\bresearch needed to understand\b": "the numbers show",
    r"(?i)\bdespite facing\b": "even when",
    r"(?i)\btestament to\b": "proof that",
    
    # High-Frequency AI Words
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
    
    # AI Transition Phrases
    r"(?i)\bthat being said\b": "but",
    r"(?i)\bat its core\b": "basically",
    r"(?i)\bto put it simply\b": "simply put",
    r"(?i)\bthis underscores the importance of\b": "this shows why",
    r"(?i)\ba key takeaway is\b": "the main point is",
    
    # Hedging Language
    r"(?i)\bgenerally speaking\b": "",
    r"(?i)\btypically\b": "",
    r"(?i)\btends to\b": "",
    r"(?i)\barguably\b": "",
    r"(?i)\bto some extent\b": "",
    r"(?i)\bbroadly speaking\b": "",
    
    # Abstract Marketing Language
    r"(?i)\bvisibility that compounds\b": "growing visibility",
    r"(?i)\bholistic growth\b": "growth",
    r"(?i)\bstrategic alignment\b": "alignment",
    r"(?i)\bintentional execution\b": "execution",
    
    # Punctuation
    r"—": " - ",  # Replace em dashes with spaced en dashes or hyphens
    r"–": " - "   # Replace en dashes just in case
}

def sanitize_content(text, is_logoclothz=False):
    """
    Scans text and replaces/removes banned words according to RPG standards.
    If is_logoclothz is True, applies additional brand-specific constraints.
    """
    if not text:
        return text
        
    sanitized_text = text
    
    # Apply Layer 0: Forbidden brand name replacements (always runs first)
    for pattern, replacement in FORBIDDEN_BRAND_REPLACEMENTS.items():
        sanitized_text = re.sub(pattern, replacement, sanitized_text)
    
    # Apply RPG Master Content Standard replacements
    for pattern, replacement in RPG_SLOP_REPLACEMENTS.items():
        sanitized_text = re.sub(pattern, replacement, sanitized_text)
        
    # Apply Logoclothz specific replacements if flagged
    if is_logoclothz:
        for pattern, replacement in LOGOCLOTHZ_REPLACEMENTS.items():
            sanitized_text = re.sub(pattern, replacement, sanitized_text)
            
    # Clean up any double spaces created by removals
    sanitized_text = re.sub(r" {2,}", " ", sanitized_text)
    
    # Clean up spaces before punctuation created by removals
    sanitized_text = re.sub(r" \.", ".", sanitized_text)
    sanitized_text = re.sub(r" ,", ",", sanitized_text)
    
    return sanitized_text.strip()

if __name__ == "__main__":
    # Simple test
    test_text = "In today's digital age, we leverage cutting-edge tools to elevate our brand. Made in the USA. It's worth noting that this is a game changer."
    print("Original:", test_text)
    print("Sanitized (Standard):", sanitize_content(test_text))
    print("Sanitized (Logoclothz):", sanitize_content(test_text, is_logoclothz=True))
