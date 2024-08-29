import re


def validate_credit_card(card_number):
    """
    Validate a credit card number using the Luhn algorithm.

    Args:
    card_number (str): The credit card number to validate.

    Returns:
    bool: True if the card number is valid, False otherwise.

    Raises:
    ValueError: If the input contains non-digit characters or is empty.
    """
    # Remove any non-digit characters
    card_number = re.sub(r"\D", "", card_number)

    if not card_number:
        raise ValueError("Card number cannot be empty.")

    # Check if the card number is of valid length
    if len(card_number) < 13 or len(card_number) > 19:
        return False

    # Apply Luhn algorithm
    digits = [int(d) for d in card_number]
    checksum = 0
    is_even = False

    for digit in digits[::-1]:
        if is_even:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
        is_even = not is_even

    return checksum % 10 == 0


def get_card_type(card_number):
    """
    Determine the type of credit card based on its number.

    Args:
    card_number (str): The credit card number.

    Returns:
    str: The type of credit card, or "Unknown" if not recognized.
    """
    patterns = {
        r"^4": "Visa",
        r"^5[1-5]": "MasterCard",
        r"^3[47]": "American Express",
        r"^6(?:011|5)": "Discover",
        r"^35(?:2[89]|[3-8]\d)": "JCB",
    }

    for pattern, card_type in patterns.items():
        if re.match(pattern, card_number):
            return card_type

    return "Unknown"
