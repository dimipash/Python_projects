"""
Validate a credit card number using the Luhn algorithm.

This function implements the Luhn algorithm to check if a given credit card number
is valid. It performs the following steps:
1. Doubles every second digit from right to left.
2. If doubling results in a two-digit number, adds those digits together.
3. Sums all the untouched digits and the doubled-digit sums.
4. Checks if the total sum is divisible by 10.

Args:
    card_number (str): The credit card number to validate.

Returns:
    None: Prints "Valid Credit Card Number" if the number is valid,
          or "Invalid Credit Card Number" if it's not.

Example:
    card_number = "5610591081018250"
    # Output: Valid Credit Card Number
"""

card_number = "5610591081018250"
odd_sum = 0
even_sum = 0
double_list = []
number = list(card_number)

for idx, val in enumerate(number):
    if idx % 2 != 0:
        odd_sum += int(val)
    else:
        double_list.append(int(val) * 2)

double_string = ""
for x in double_list:
    double_string += str(x)

double_list = list(double_string)

for x in double_list:
    even_sum += int(x)

net_sum = odd_sum + even_sum
if net_sum % 10 == 0:
    print("Valid Credit Card Number")
else:
    print("Invalid Credit Card Number")
