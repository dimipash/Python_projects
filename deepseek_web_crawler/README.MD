# DeepSeek Web Crawler 🤖

A powerful and flexible web crawler that uses Groq's LLM API to intelligently extract structured data from any website. Perfect for data scientists, researchers, and developers who need to gather and analyze web data.

## ✨ Features

🧠 **Intelligent Extraction**
- Uses Groq's LLM API for smart data parsing
- Understands context and extracts meaningful data
- Handles various data formats and structures

🎯 **Flexible Targeting**
- CSS selector-based element targeting
- Multi-page crawling support
- Configurable delay between requests
- Cache support for faster development

🛠️ **Enhanced Features**
- Multiple output formats (CSV, JSON, Excel)
- Proxy support with automatic rotation
- Rate limiting and retry mechanisms
- Progress tracking with detailed statistics
- Advanced error handling and logging
- Customizable browser configurations
- Duplicate detection and filtering

🔒 **Safe & Respectful**
- Configurable delays between requests
- User-agent rotation
- Proxy support with health checks
- Cache mechanism to reduce server load
- Rate limiting to prevent overloading

## Getting Started

### 1. Environment Setup

1. First, install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```
   Get your API key from [Groq Console](https://console.groq.com)

### 2. Basic Usage

Run the crawler with a predefined configuration:
```bash
python main.py --config test
```

### 3. Advanced Usage

The crawler supports various command-line options for customization:

```bash
python main.py --config <config_name> [options]

Options:
  --output-dir DIR    Directory for output files (default: output)
  --cache-dir DIR     Directory for cache files (default: .cache)
  --proxy-file FILE   Path to proxy configuration file
  --log-file FILE     Path to log file (default: logs/crawler.log)
  --log-level LEVEL   Logging level (DEBUG/INFO/WARNING/ERROR/CRITICAL)
  --list              List available configurations and exit
```

### 4. Proxy Configuration

Create a JSON file with proxy settings:
```json
{
  "proxies": [
    "http://user:pass@host1:port",
    "http://user:pass@host2:port"
  ]
}
```

Then use it with the crawler:
```bash
python main.py --config test --proxy-file proxies.json
```

### 5. Output Formats

The crawler automatically saves data in multiple formats:
- `items.csv`: CSV format with all items
- `items.json`: JSON format with all items
- `items.xlsx`: Excel format with all items

### 6. Configuration Templates

Available configuration templates:
- `test`: Local testing configuration
- `ecommerce`: E-commerce product scraping
- `news`: News article scraping
- `jobs`: Job listing scraping
- `real_estate`: Real estate listing scraping

View all available configurations:
```bash
python main.py --list
```

### 7. Creating Custom Configurations

1. Use the generator script:
   ```bash
   python create_config.py
   ```
   This will guide you through creating a new configuration.

2. Or manually create one in `config.py`:
   ```python
   "my_config": {
       **DEFAULT_CONFIG,
       "BASE_URL": "https://example.com",
       "CSS_SELECTOR": "div.item",
       "REQUIRED_KEYS": ["name", "price"],
       "OPTIONAL_KEYS": ["description", "category"],
       "CRAWLER_CONFIG": {
           **DEFAULT_CONFIG["CRAWLER_CONFIG"],
           "MULTI_PAGE": True,
           "MAX_PAGES": 5,
           "DELAY_BETWEEN_PAGES": 2,
           "HEADLESS": True,
           "DEVICE_TYPE": "desktop"  # desktop, mobile, tablet
       },
       "LLM_CONFIG": {
           **DEFAULT_CONFIG["LLM_CONFIG"],
           "INSTRUCTION": """
           Extract product information:
           - Name: Product title
           - Price: Current price
           - Description: Product description
           - Category: Product category
           """
       }
   }
   ```

### 8. Progress Tracking

The crawler provides real-time progress information:
- Current page and total pages
- Items processed (total/valid/failed/duplicate)
- Processing rate (items/second)
- Success rate
- Browser statistics
- Proxy usage (if enabled)

### 9. Error Handling

The crawler implements robust error handling:
- Automatic retries for failed requests
- Proxy rotation on failures
- Detailed error logging
- Rate limiting to prevent overload
- Cache mechanism for development

### 10. Troubleshooting

If you encounter issues:
1. Check your GROQ_API_KEY in .env
2. Ensure all dependencies are installed
3. Try the test configuration first
4. Check the log file for detailed error messages
5. Adjust rate limiting and delays if needed
6. Verify proxy configuration if using proxies

### 11. Development

The project structure:
```
deepseek_web_crawler/
├── config.py           # Configuration templates
├── create_config.py    # Configuration generator
├── main.py            # Main entry point
├── requirements.txt    # Dependencies
├── models/            # Data models
│   └── item.py
└── utils/             # Utility modules
    ├── browser.py     # Browser management
    ├── data_utils.py  # Data processing
    ├── logger.py      # Logging setup
    ├── output.py      # Output handling
    ├── progress.py    # Progress tracking
    ├── proxy.py       # Proxy management
    ├── retry.py       # Retry mechanisms
    └── scraper_utils.py  # Core scraping logic
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests.
