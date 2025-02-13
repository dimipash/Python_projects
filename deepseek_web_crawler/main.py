import asyncio
import argparse
import sys
from pathlib import Path
from typing import Dict, Any, Optional

from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv

from config import DEFAULT_CONFIG, CONFIGS
from utils.logger import setup_logger, logger
from utils.scraper_utils import ScraperManager

# Import custom configurations
try:
    from my_configs import *
except ImportError:
    logger.warning("No custom configurations found. Using default templates only.")

def parse_args() -> Dict[str, Any]:
    """
    Parse command line arguments.
    
    Returns:
        Dict[str, Any]: Parsed arguments
    """
    # Get available configurations
    default_configs = ["test", "ecommerce", "news", "jobs", "real_estate"]
    custom_configs = [k for k in CONFIGS.keys() if k not in default_configs]
    
    # Create help text
    help_text = "Configuration to use. Available options:\n"
    help_text += "\nDefault templates:\n"
    for config in default_configs:
        if config in CONFIGS:
            help_text += f"  {config}: For {config} scraping\n"
    
    if custom_configs:
        help_text += "\nCustom configurations:\n"
        for config in custom_configs:
            help_text += f"  {config}: Custom configuration\n"
    
    parser = argparse.ArgumentParser(
        description="Deep Seek Web Crawler",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        choices=list(CONFIGS.keys()),
        help=help_text,
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Directory for output files (default: output)"
    )
    
    parser.add_argument(
        "--cache-dir",
        type=str,
        default=".cache",
        help="Directory for cache files (default: .cache)"
    )
    
    parser.add_argument(
        "--proxy-file",
        type=str,
        help="Path to proxy configuration file"
    )
    
    parser.add_argument(
        "--log-file",
        type=str,
        help="Path to log file (default: logs/crawler.log)"
    )
    
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available configurations and exit"
    )
    
    args = parser.parse_args()
    
    if args.list:
        print("\nAvailable configurations:")
        print("\nDefault templates:")
        for config in default_configs:
            if config in CONFIGS:
                print(f"  {config}: For {config} scraping")
        if custom_configs:
            print("\nCustom configurations:")
            for config in custom_configs:
                print(f"  {config}: Custom configuration")
        sys.exit(0)
    
    return vars(args)


def get_config(template: str) -> Dict[str, Any]:
    """
    Get configuration based on template name.
    
    Args:
        template: Name of the configuration template
        
    Returns:
        Dict[str, Any]: Configuration dictionary
        
    Raises:
        SystemExit: If template is not found
    """
    if template not in CONFIGS:
        logger.error(f"Unknown configuration '{template}'")
        logger.info("\nTo see available configurations, run:")
        logger.info("python main.py --list")
        sys.exit(1)
    return CONFIGS[template]


async def crawl_items(
    config: Dict[str, Any],
    output_dir: str,
    cache_dir: str,
    proxy_file: Optional[str] = None
) -> bool:
    """
    Main function to crawl and extract data from websites.
    
    Args:
        config: Crawler configuration dictionary
        output_dir: Directory for output files
        cache_dir: Directory for cache files
        proxy_file: Optional path to proxy configuration file
        
    Returns:
        bool: True if crawling was successful
    """
    try:
        # Initialize scraper manager
        scraper = ScraperManager(
            config=config,
            output_dir=output_dir,
            cache_dir=cache_dir,
            proxy_file=proxy_file
        )
        
        # Execute crawling
        items = await scraper.crawl()
        return bool(items)
        
    except asyncio.CancelledError:
        logger.warning("\nCrawling interrupted by user.")
        return False
    except Exception as e:
        logger.error(f"\nAn error occurred: {str(e)}")
        return False


async def main():
    """Entry point of the script."""
    # Load environment variables
    load_dotenv()
    
    # Parse command line arguments
    args = parse_args()
    
    # Setup logging
    log_file = args.get("log_file") or "logs/crawler.log"
    log_level = getattr(sys.modules["logging"], args["log_level"])
    
    # Ensure logs directory exists
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Configure logger
    setup_logger(
        name="deepseek_crawler",
        log_file=log_file,
        level=log_level
    )
    
    # Get configuration
    config = get_config(args["config"])
    
    try:
        # Start crawling
        success = await crawl_items(
            config=config,
            output_dir=args["output_dir"],
            cache_dir=args["cache_dir"],
            proxy_file=args.get("proxy_file")
        )
        
        if not success:
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.warning("\nCrawling interrupted by user.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\nAn error occurred: {str(e)}")
        sys.exit(1)
    finally:
        logger.info("\nCrawling completed.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(1)
