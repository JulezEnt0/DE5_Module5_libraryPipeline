"""
Data validation functions.
"""


# Example function to implement:
def validate_isbn(isbn):
    if isbn is None:
        return None

    cleaned = str(isbn).replace("-", "")

    if not cleaned.isdigit():
        return None

    if len(cleaned) != 13:
        return None

    digits = []
    for character in cleaned:
        digits.append(int(character))

    total = 0
    for i in range(12):
        digit = digits[i]
        if i % 2 == 0:
            total += digit * 1
        else:
            total += digit * 3

    check_digit = (10 - (total % 10)) % 10

    if check_digit != digits[12]:
        return None

    return cleaned

    """Clean and validate an ISBN-13 value.

    Args:
        isbn: Raw ISBN value (may be a hyphenated string, a number, or None)

    Returns:
        The cleaned ISBN-13 string if valid, or None if invalid.

    TODO: Implement check-digit validation and formatting cleanup.
    """
    return isbn
