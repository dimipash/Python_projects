# Currency Converter

A Python-based currency converter that uses real-time exchange rates to convert between different currencies.

## Description

This Currency Converter is a command-line application that allows users to convert amounts between different currencies using up-to-date exchange rates. It fetches real-time currency conversion data from the Free Currency Converter API.

## Features

- Real-time currency conversion
- Support for a wide range of currencies
- User-friendly command-line interface
- Error handling for invalid inputs and network issues
- Option to perform multiple conversions in one session

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher installed on your system
- `requests` library installed (`pip install requests`)
- An API key from [Free Currency Converter API](https://free.currencyconverterapi.com/)

## Installation

1. Clone this repository or download the script.
2. Install the required library:
   ```
   pip install requests
   ```
3. Open the script and replace `'YOUR_API_KEY'` with your actual API key from Free Currency Converter API.

## Usage

To use the Currency Converter:

1. Run the script:
   ```
   python currency_converter.py
   ```
2. Follow the prompts to enter:
   - The amount you want to convert
   - The base currency code (e.g., USD)
   - The target currency code (e.g., EUR)
3. The converted amount will be displayed.
4. You can choose to perform another conversion or exit the program.

## Example

```
Welcome to the Currency Converter!
Enter the amount to
```
