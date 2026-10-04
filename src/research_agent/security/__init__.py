import re 
from fastapi import HTTPException 

injection_patterns = [
    r"(?i)ignore\s+(all\s+)?previous\s+instructions",
    r"(?i)reveal\s+(system|internal|hidden)\s+(prompt|instructions)",
    r"(?i)what\s+is\s+your\s+(initial|original|system)\s+prompt",
    r"(?i)repeat\s+(the\s+words\s+above|everything\s+above)",
    r"(?i)disregard\s+prior\s+directives"
]

scrub_patterns = [
    re.compile(r"System:\s*", re.IGNORECASE),
    re.compile(r"\[Internal Instructions\]", re.IGNORECASE),
    re.compile(r"<system_prompt>[\s\S]*?</system_prompt>", re.IGNORECASE),
    re.compile(r"Bearer\s+[a-zA-Z0-9_\-\.]+", re.IGNORECASE)
]

def senetize_input(text:str)->str:
    """Validates user text and raises HTTP 400 if malicious instructions are detected."""
    if not text :
        return ""
    for pat in injection_patterns:
        if re.search(pat, text):
            raise HTTPException(
                status_code=400,
                detail="Security violation: Prohibited or malicious instruction pattern detected."
            )
    return text.strip()

def scrub_output(text: str) -> str:
    """Removes sensitive tags, leaked instructions, or auth tokens from generated content."""
    if not text:
        return ""
    cleaned = text
    for pattern in scrub_patterns:
        cleaned = pattern.sub("", cleaned)
    return cleaned.strip()