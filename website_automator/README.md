# Webpage Opener

A simple Python script to open predefined sets of webpages based on categories.

## Features

- Open multiple webpages at once
- Predefined categories for different webpage sets (e.g., work, personal)
- Command-line interface for easy usage

## Requirements

- Python 3.x
- `webbrowser` module (part of Python's standard library)

## Installation

1. Clone this repository.

2. No additional installation is required as the script uses Python's standard library.

## Usage

Run the script from the command line, providing a category as an argument:

```
python main.py [category]
```

Where `[category]` is either `work` or `personal`.

Examples:

- To open work-related pages:
  ```
  python main.py work
  ```
- To open personal pages:
  ```
  python main.py personal
  ```

## Customization

You can customize the URLs for each category by modifying the `URLS` dictionary in the script:

```python
URLS = {
    "work": ["https://www.slack.com", "https://www.google.com"],
    "personal": ["https://www.spotify.com", "https://www.youtube.com"],
}
```

Add or modify categories and URLs as needed.
