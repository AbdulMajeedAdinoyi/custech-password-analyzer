import re

# Common weak words and local context (CUSTECH-related)
COMMON_WORDS = [
    "password", "qwerty", "admin", "school",
    "custech", "osara", "confluence", "portal", "student",
    "faculty", "staff", "login", "user", "test"
]

# Simple keyboard sequences
KEYBOARD_SEQS = ["qwerty", "asdf", "zxcv", "12345", "1111", "0000"]

# Regex for years (like 2025, 2024)
YEAR_REGEX = re.compile(r"(19|20)\d{2}")

def score_password(pw: str) -> dict:
    tips = []
    score = 0
    pw_lower = pw.lower()

    # Length check
    if len(pw) >= 12:
        score += 40
    elif len(pw) >= 8:
        score += 20
    else:
        tips.append("Increase length to at least 12 characters")

    # Character diversity
    classes = {
        "lower": bool(re.search(r"[a-z]", pw)),
        "upper": bool(re.search(r"[A-Z]", pw)),
        "digit": bool(re.search(r"\d", pw)),
        "symbol": bool(re.search(r"[^A-Za-z0-9]", pw))
    }
    score += sum(15 for present in classes.values() if present)
    if sum(classes.values()) < 3:
        tips.append("Add missing types (upper/lower/digit/symbol)")

    # Common words
    if any(w in pw_lower for w in COMMON_WORDS):
        score -= 20
        tips.append("Avoid predictable words (school names, common terms)")

    # Keyboard sequences
    if any(seq in pw_lower for seq in KEYBOARD_SEQS):
        score -= 15
        tips.append("Avoid keyboard patterns or simple sequences")

    # Year patterns
    if YEAR_REGEX.search(pw):
        score -= 10
        tips.append("Avoid adding years; attackers try names+years first")

    # Repeated characters
    if re.search(r"(.)\1{2,}", pw):
        score -= 10
        tips.append("Avoid repeating the same character")

    # Bound score between 0 and 100
    score = max(0, min(100, score))

    # Category
    if score < 40:
        category = "Weak"
    elif score < 70:
        category = "Moderate"
    else:
        category = "Strong"

    # Deduplicate feedback
    tips = list(dict.fromkeys(tips))

    return {
        "score": score,
        "category": category,
        "feedback": tips
    }