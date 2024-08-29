from credit_card_validator import validate_credit_card, get_card_type


def main():
    print("Welcome to the Credit Card Validator!")
    print("Enter 'q' to quit at any time.")

    while True:
        card_number = input("\nPlease enter a credit card number: ").strip()

        if card_number.lower() == "q":
            print("Thank you for using the Credit Card Validator. Goodbye!")
            break

        try:
            is_valid = validate_credit_card(card_number)
            card_type = get_card_type(card_number)

            if is_valid:
                print(f"Valid {card_type} credit card number.")
            else:
                print(
                    f"Invalid credit card number. It appears to be a {card_type} format."
                )

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
