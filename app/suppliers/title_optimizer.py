POWER_WORDS = [
    "Premium",
    "Smart",
    "Portable",
    "Essential",
]

def optimize_title(title):
    title = title.strip()

    if not title:
        return title

    already_has_power_word = any(
        title.lower().startswith(word.lower())
        for word in POWER_WORDS
    )

    if not already_has_power_word:
        title = f"Premium {title}"

    return title[:120]
