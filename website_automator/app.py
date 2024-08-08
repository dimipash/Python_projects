"""Opens a set of predefined webpages in the default web browser."""

import sys
import webbrowser

URLS = {
    "work": ["https://www.slack.com", "https://www.google.com"],
    "personal": ["https://www.spotify.com", "https://www.youtube.com"],
}


def open_webpages(urls):
    for url in urls:
        webbrowser.open(url)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Please provide a category (work or personal) as a command-line argument."
        )
        sys.exit(1)

    set_name = sys.argv[1]
    if set_name not in URLS:
        print(f"Invalid category '{set_name}'. Please use 'work' or 'personal'.")
        sys.exit(1)

    urls = URLS[set_name]
    open_webpages(urls)
