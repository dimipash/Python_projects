import asyncio
import json
from pathlib import Path
from typing import List, Optional, Dict
import aiohttp
from utils.logger import logger
from utils.retry import async_retry

class ProxyManager:
    """Manages a pool of proxies with automatic testing and rotation."""
    
    def __init__(
        self,
        proxies: Optional[List[str]] = None,
        proxy_file: Optional[str] = None,
        test_url: str = "http://httpbin.org/ip",
        timeout: float = 10.0,
        min_speed: float = 1.0,
        max_fail_count: int = 3
    ):
        """
        Initialize the proxy manager.
        
        Args:
            proxies: List of proxy URLs (e.g., ["http://user:pass@host:port"])
            proxy_file: Path to JSON file containing proxy list
            test_url: URL to use for testing proxies
            timeout: Timeout for proxy tests in seconds
            min_speed: Minimum acceptable response time in seconds
            max_fail_count: Maximum number of failures before removing proxy
        """
        self.proxies: List[Dict] = []
        self.test_url = test_url
        self.timeout = timeout
        self.min_speed = min_speed
        self.max_fail_count = max_fail_count
        self._current_index = 0
        
        if proxy_file:
            self._load_from_file(proxy_file)
        elif proxies:
            self.proxies = [{"url": proxy, "fails": 0} for proxy in proxies]
    
    def _load_from_file(self, file_path: str):
        """Load proxy list from a JSON file."""
        path = Path(file_path)
        if not path.exists():
            logger.warning(f"Proxy file not found: {file_path}")
            return
        
        try:
            with open(path) as f:
                data = json.load(f)
            
            if isinstance(data, list):
                self.proxies = [{"url": proxy, "fails": 0} for proxy in data]
            elif isinstance(data, dict) and "proxies" in data:
                self.proxies = [{"url": proxy, "fails": 0} for proxy in data["proxies"]]
            else:
                logger.error(f"Invalid proxy file format: {file_path}")
        except Exception as e:
            logger.error(f"Error loading proxy file: {str(e)}")
    
    def _save_to_file(self, file_path: str):
        """Save current proxy list to a JSON file."""
        try:
            with open(file_path, 'w') as f:
                json.dump({"proxies": [p["url"] for p in self.proxies]}, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving proxy file: {str(e)}")
    
    @async_retry(retries=2, delay=1.0)
    async def _test_proxy(self, proxy: Dict) -> bool:
        """
        Test a proxy by making a request through it.
        
        Args:
            proxy: Proxy dictionary containing URL and fail count
            
        Returns:
            bool: True if proxy test succeeded
        """
        try:
            start_time = asyncio.get_event_loop().time()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.test_url,
                    proxy=proxy["url"],
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    if response.status == 200:
                        elapsed = asyncio.get_event_loop().time() - start_time
                        return elapsed <= self.min_speed
            
            return False
        except Exception as e:
            logger.debug(f"Proxy test failed for {proxy['url']}: {str(e)}")
            return False
    
    async def test_proxies(self):
        """Test all proxies in parallel and remove failed ones."""
        if not self.proxies:
            logger.warning("No proxies available to test")
            return
        
        tasks = []
        for proxy in self.proxies:
            tasks.append(self._test_proxy(proxy))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Update proxy list based on test results
        new_proxies = []
        for proxy, result in zip(self.proxies, results):
            if isinstance(result, Exception) or not result:
                proxy["fails"] += 1
                if proxy["fails"] >= self.max_fail_count:
                    logger.info(f"Removing failed proxy: {proxy['url']}")
                    continue
            else:
                proxy["fails"] = 0
            new_proxies.append(proxy)
        
        self.proxies = new_proxies
        logger.info(f"Proxy test complete. {len(self.proxies)} proxies available")
    
    def get_next_proxy(self) -> Optional[str]:
        """
        Get the next proxy URL using round-robin rotation.
        
        Returns:
            str: Next proxy URL or None if no proxies available
        """
        if not self.proxies:
            return None
        
        proxy = self.proxies[self._current_index]["url"]
        self._current_index = (self._current_index + 1) % len(self.proxies)
        return proxy
    
    @property
    def proxy_count(self) -> int:
        """Get the number of available proxies."""
        return len(self.proxies)
    
    def add_proxy(self, proxy_url: str):
        """
        Add a new proxy to the pool.
        
        Args:
            proxy_url: Proxy URL to add
        """
        if not any(p["url"] == proxy_url for p in self.proxies):
            self.proxies.append({"url": proxy_url, "fails": 0})
            logger.info(f"Added new proxy: {proxy_url}")
    
    def remove_proxy(self, proxy_url: str):
        """
        Remove a proxy from the pool.
        
        Args:
            proxy_url: Proxy URL to remove
        """
        self.proxies = [p for p in self.proxies if p["url"] != proxy_url]
        logger.info(f"Removed proxy: {proxy_url}")