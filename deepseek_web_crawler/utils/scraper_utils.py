import json
from typing import Dict, List, Set, Tuple, Any, Optional
import asyncio

from crawl4ai import (
    AsyncWebCrawler,
    CacheMode,
    CrawlerRunConfig,
    LLMExtractionStrategy,
)

from models.item import ScrapedItem
from utils.logger import logger
from utils.retry import async_retry
from utils.browser import BrowserManager
from utils.proxy import ProxyManager
from utils.progress import ProgressTracker
from utils.output import OutputManager

class ScraperManager:
    """Manages the web scraping process with advanced features."""
    
    def __init__(
        self,
        config: Dict[str, Any],
        output_dir: str = "output",
        cache_dir: str = ".cache",
        proxy_file: Optional[str] = None
    ):
        """
        Initialize scraper manager.
        
        Args:
            config: Scraping configuration dictionary
            output_dir: Directory for output files
            cache_dir: Directory for cache files
            proxy_file: Optional path to proxy configuration file
        """
        self.config = config
        self.output_manager = OutputManager(output_dir=output_dir)
        
        # Initialize proxy manager if proxy file provided
        self.proxy_manager = None
        if proxy_file:
            self.proxy_manager = ProxyManager(
                proxy_file=proxy_file,
                timeout=config["CRAWLER_CONFIG"].get("TIMEOUT", 30.0)
            )
        
        # Initialize browser manager
        self.browser_manager = BrowserManager(
            proxy_manager=self.proxy_manager,
            cache_dir=cache_dir,
            default_timeout=config["CRAWLER_CONFIG"].get("TIMEOUT", 30.0),
            default_wait_time=config["CRAWLER_CONFIG"].get("WAIT_TIME", 2.0)
        )
        
        # Initialize progress tracker
        self.progress = ProgressTracker(
            total_pages=config["CRAWLER_CONFIG"].get("MAX_PAGES"),
            show_progress_bar=True
        )
        
        # Track seen items to prevent duplicates
        self.seen_titles: Set[str] = set()
        
        # Get configuration values
        self.required_keys = config["REQUIRED_KEYS"]
        self.multi_page = config["CRAWLER_CONFIG"]["MULTI_PAGE"]
        self.max_pages = config["CRAWLER_CONFIG"].get("MAX_PAGES", 1)
        self.delay = config["CRAWLER_CONFIG"].get("DELAY_BETWEEN_PAGES", 2)
    
    def get_llm_strategy(self) -> LLMExtractionStrategy:
        """Get configured LLM extraction strategy."""
        return LLMExtractionStrategy(
            provider=self.config["LLM_CONFIG"].get(
                "PROVIDER", "groq/deepseek-r1-distill-llama-70b"
            ),
            api_token=self.config["LLM_CONFIG"].get("API_TOKEN"),
            schema=ScrapedItem.model_json_schema(),
            extraction_type=self.config["LLM_CONFIG"].get("EXTRACTION_TYPE", "schema"),
            instruction=self.config["LLM_CONFIG"].get("INSTRUCTION", (
                "Extract information from the content with these details:\n"
                "- Title/name of the item\n"
                "- Description or main content\n"
                "- Any URLs present\n"
                "- Dates if available\n"
                "- Categories or types\n"
                "- Tags or labels\n"
                "- Ratings if present\n"
                "- Price information\n"
                "- Location/address if applicable\n"
                "- Contact information\n"
                "- Any other relevant metadata\n"
                "\nFormat the output as structured data following the schema."
            )),
            input_format=self.config["LLM_CONFIG"].get("INPUT_FORMAT", "markdown"),
            verbose=True,
        )
    
    @async_retry(retries=3, delay=1.0, backoff=2.0)
    async def check_no_results(
        self,
        crawler: AsyncWebCrawler,
        url: str,
        session_id: str,
    ) -> bool:
        """
        Check if page indicates no results with retry support.
        
        Args:
            crawler: AsyncWebCrawler instance
            url: URL to check
            session_id: Session identifier
            
        Returns:
            bool: True if no results found
        """
        result = await crawler.arun(
            url=url,
            config=self.browser_manager.get_crawler_config(
                session_id=session_id,
                wait_until="networkidle"
            )
        )
        
        if result.success:
            no_results_phrases = [
                "No Results Found",
                "No matches found",
                "Nothing found",
                "No items found",
                "0 results",
                "No results",
                "Empty",
            ]
            return any(
                phrase.lower() in result.cleaned_html.lower()
                for phrase in no_results_phrases
            )
        
        logger.error(f"Error checking for no results: {result.error_message}")
        return False
    
    @async_retry(retries=3, delay=1.0, backoff=2.0)
    async def fetch_and_process_page(
        self,
        crawler: AsyncWebCrawler,
        page_number: int,
        session_id: str,
    ) -> Tuple[List[dict], bool]:
        """
        Fetch and process a single page with retry support.
        
        Args:
            crawler: AsyncWebCrawler instance
            page_number: Page number to process
            session_id: Session identifier
            
        Returns:
            Tuple[List[dict], bool]: Processed items and no results flag
        """
        # Construct URL for pagination
        url = self.config["BASE_URL"]
        if page_number > 1:
            if "?" in url:
                url = f"{url}&page={page_number}"
            else:
                url = f"{url}?page={page_number}"
        
        logger.info(f"Processing page {page_number}: {url}")
        
        # Check for no results
        no_results = await self.check_no_results(crawler, url, session_id)
        if no_results:
            logger.info("No results found on this page.")
            self.progress.update(current_page=page_number)
            return [], True
        
        # Fetch page content
        result = await crawler.arun(
            url=url,
            config=self.browser_manager.get_crawler_config(
                session_id=session_id,
                extraction_strategy=self.get_llm_strategy(),
                css_selector=self.config["CSS_SELECTOR"],
                wait_until="networkidle"
            )
        )
        
        if not result.success:
            logger.error(f"Error fetching page {page_number}: {result.error_message}")
            self.progress.update(
                current_page=page_number,
                failed_items=1
            )
            return [], False
        
        if not result.extracted_content:
            logger.warning(f"No content extracted from page {page_number}.")
            self.progress.update(current_page=page_number)
            return [], False
        
        # Parse extracted content
        try:
            extracted_data = json.loads(result.extracted_content)
            if not extracted_data:
                logger.warning(f"No data found on page {page_number}.")
                self.progress.update(current_page=page_number)
                return [], False
            
            logger.debug(f"Raw extracted data from page {page_number}:")
            logger.debug(json.dumps(extracted_data, indent=2))
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON from page {page_number}: {str(e)}")
            self.progress.update(
                current_page=page_number,
                failed_items=1
            )
            return [], False
        
        # Process items
        valid_items = []
        failed_items = 0
        duplicate_items = 0
        
        for item in extracted_data:
            # Remove error key if it's False
            if item.get("error") is False:
                item.pop("error", None)
            
            # Get the title (main identifier) of the item
            title = item.get("title")
            if not title:
                logger.debug("Item found without a title, skipping...")
                failed_items += 1
                continue
            
            # Check for required fields
            missing_keys = [
                key for key in self.required_keys
                if key not in item or not item[key]
            ]
            if missing_keys:
                logger.debug(
                    f"Incomplete data for '{title}'. "
                    f"Missing required fields: {', '.join(missing_keys)}"
                )
                failed_items += 1
                continue
            
            # Check for duplicates
            if title in self.seen_titles:
                logger.debug(f"Duplicate found: {title}")
                duplicate_items += 1
                continue
            
            # Add valid item
            self.seen_titles.add(title)
            valid_items.append(item)
        
        # Update progress
        self.progress.update(
            current_page=page_number,
            new_items=len(extracted_data),
            valid_items=len(valid_items),
            failed_items=failed_items,
            duplicate_items=duplicate_items
        )
        
        return valid_items, False
    
    async def crawl(self) -> List[Dict]:
        """
        Execute the crawling process.
        
        Returns:
            List[Dict]: List of all valid items found
        """
        logger.info(f"\nStarting crawler with {self.config['BASE_URL']}")
        logger.info(f"Mode: {'Multi-page' if self.multi_page else 'Single-page'}")
        if self.multi_page:
            logger.info(f"Max pages: {self.max_pages}")
        logger.info("Required fields: " + ", ".join(self.required_keys))
        logger.info("Optional fields: " + ", ".join(self.config.get("OPTIONAL_KEYS", [])))
        
        # Initialize crawler
        browser_config = self.browser_manager.get_browser_config(
            self.config["CRAWLER_CONFIG"]
        )
        
        all_items = []
        page_number = 1
        session_id = "crawl_session"
        
        try:
            # Test proxies if available
            if self.proxy_manager:
                await self.proxy_manager.test_proxies()
            
            # Start crawling
            async with AsyncWebCrawler(config=browser_config) as crawler:
                while True:
                    # Fetch and process current page
                    items, no_results = await self.fetch_and_process_page(
                        crawler,
                        page_number,
                        session_id
                    )
                    
                    if no_results:
                        logger.info("\nNo more items found. Ending crawl.")
                        break
                    
                    if not items:
                        logger.warning(f"\nNo items extracted from page {page_number}.")
                        break
                    
                    # Add items from this page
                    all_items.extend(items)
                    
                    # Check if we should continue
                    if not self.multi_page or page_number >= self.max_pages:
                        logger.info(
                            f"\nReached "
                            f"{'page limit' if self.multi_page else 'single page mode'}. "
                            f"Ending crawl."
                        )
                        break
                    
                    page_number += 1
                    logger.info(f"\nMoving to page {page_number}...")
                    await asyncio.sleep(self.delay)
        
        except asyncio.CancelledError:
            logger.warning("\nCrawling cancelled.")
            raise
        except Exception as e:
            logger.error(f"\nError during crawling: {str(e)}")
            raise
        finally:
            # Save results
            if all_items:
                # Save in all formats
                self.output_manager.save_all_formats(all_items)
            else:
                logger.warning("\nNo items were found during the crawl.")
            
            # Show final statistics
            self.progress.finish()
            
            # Show browser statistics
            logger.info("\nBrowser Statistics:")
            for key, value in self.browser_manager.get_stats().items():
                logger.info(f"  {key}: {value}")
        
        return all_items
