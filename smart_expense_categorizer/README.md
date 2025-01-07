# Smart Expense Categorizer

An intelligent Python application that automatically categorizes and analyzes your expenses using machine learning.

## Features

- Automatic categorization of transactions using K-Means clustering
- Text-based pattern recognition for transaction descriptions
- Visual spending analysis with matplotlib
- Easy-to-use interface
- Customizable number of categories
- Sample dataset included for demonstration

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

The program will:
1. Generate sample transaction data
2. Automatically categorize transactions
3. Generate a bar chart visualization (category_spending.png)
4. Print analysis results to console

## Example Output

```text
Expense Analysis Results:
               amount       description
                sum count                <lambda>
category                                
0         1234.56    20       Uber Ride
1          987.65    15  Netflix Subscription
2         2345.67    25  Whole Foods Market
3          456.78    10    Starbucks Coffee
4         3456.78    30    Amazon Purchase
```

A bar chart visualization will be saved as `category_spending.png`.

## Customization

- Adjust number of categories by modifying `n_clusters` in `main.py`
- Add your own transaction data by modifying the sample data structure
- Customize visualization styles in the `analyze_categories` method

## Requirements

- Python 3.8+
- See requirements.txt for dependencies

## License

MIT License
