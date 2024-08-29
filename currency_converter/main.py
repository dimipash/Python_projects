import requests


def get_exchange_rate(base_currency, target_currency):
    url = f"https://free.currconv.com/api/v7/convert?apiKey=YOUR_API_KEY&q={base_currency}_{target_currency}&compact=ultra"
    response = requests.get(url)
    data = response.json()
    return data[f"{base_currency}_{target_currency}"]


def convert_currency(amount, base_currency, target_currency):
    rate = get_exchange_rate(base_currency, target_currency)
    converted_amount = amount * rate
    return converted_amount


def get_user_input():
    amount = float(input("Enter the amount to convert: "))
    base_currency = input("Enter the base currency code (e.g., USD): ").upper()
    target_currency = input("Enter the target currency code (e.g., EUR): ").upper()
    return amount, base_currency, target_currency


def main():
    print("Welcome to the Currency Converter!")

    while True:
        try:
            amount, base_currency, target_currency = get_user_input()
            result = convert_currency(amount, base_currency, target_currency)
            print(
                f"{amount} {base_currency} is equal to {result:.2f} {target_currency}"
            )
        except KeyError:
            print("Invalid currency code. Please try again.")
        except ValueError:
            print("Invalid amount. Please enter a number.")
        except requests.RequestException:
            print(
                "An error occurred while fetching the exchange rate. Please check your internet connection."
            )

        again = input("Do you want to perform another conversion? (yes/no): ").lower()
        if again != "yes":
            print("Thank you for using the Currency Converter. Goodbye!")
            break


if __name__ == "__main__":
    main()
