# Web Crawler Project

This project is a multi-threaded web crawler implemented in Python. It's designed to crawl websites, extract links, and store the crawled data efficiently.

## Project Structure

The project consists of several Python files, each with a specific role:

- `main.py`: The entry point of the application. It sets up and initiates the crawling process.
- `spider.py`: Contains the `Spider` class, which is responsible for the core crawling logic.
- `link_finder.py`: Implements the `LinkFinder` class, an HTML parser for extracting links from web pages.
- `domain.py`: Provides utility functions for working with URLs and domain names.
- `demo.py`: Contains helper functions for file operations and data structure conversions.

## Features

- Multi-threaded crawling for improved performance
- Respects the domain boundaries (doesn't crawl external links)
- Stores crawled and queued links in separate files
- Ability to pause and resume crawling

## Requirements

- Python 3.x

## Usage

1. Clone the repository:

   ```
   git clone <repository-url>
   cd web-crawler-project
   ```

2. Open `main.py` and set the `HOMEPAGE` variable to the URL you want to start crawling:

   ```python
   HOMEPAGE = 'https://example.com'
   ```

3. Run the crawler:

   ```
   python main.py
   ```

4. The crawler will create a new directory named after your project (default is 'thesite'). This directory will contain two files:
   - `queue.txt`: URLs queued for crawling
   - `crawled.txt`: URLs that have been crawled

## Customization

- You can adjust the number of threads by changing the `NUMBER_OF_THREADS` variable in `main.py`.
- Modify the `PROJECT_NAME` in `main.py` to change the name of the output directory.

## How It Works

1. The `Spider` class initializes the project by creating necessary directories and files.
2. It starts by crawling the homepage URL.
3. For each page, it:
   - Extracts all links using `LinkFinder`
   - Adds new links to the queue
   - Marks the current page as crawled
4. Multiple worker threads pick up URLs from the queue and crawl them concurrently.
5. The process continues until no more URLs are left in the queue.

## Limitations

- This crawler doesn't respect `robots.txt` files. Ensure you have permission to crawl the target website.
- It doesn't handle JavaScript-rendered content, as it only processes static HTML.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page] if you want to contribute.

## License

[MIT License](https://opensource.org/licenses/MIT)
