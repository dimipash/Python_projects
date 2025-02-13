from dataclasses import dataclass
from typing import Dict, List, Optional
import random
from crawl4ai import BrowserConfig, CacheMode, CrawlerRunConfig

from utils.logger import logger
from utils.proxy import ProxyManager

@dataclass
class UserAgent:
    """Represents a user agent configuration."""
    name: str
    string: str
    device_type: str  # desktop, mobile, tablet

# Common user agents for different devices
USER_AGENTS = [
    UserAgent(
        "Chrome Desktop",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "desktop"
    ),
    UserAgent(
        "Firefox Desktop",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "desktop"
    ),
    UserAgent(
        "Safari Desktop",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "desktop"
    ),
    UserAgent(
        "Chrome Mobile",
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "mobile"
    ),
    UserAgent(
        "Safari Mobile",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
        "mobile"
    ),
    UserAgent(
        "Chrome Tablet",
        "Mozilla/5.0 (Linux; Android 10; SAMSUNG SM-T510) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "tablet"
    ),
]

class BrowserManager:
    """Manages browser configuration and behavior."""
    
    def __init__(
        self,
        proxy_manager: Optional[ProxyManager] = None,
        user_agents: Optional[List[UserAgent]] = None,
        cache_dir: Optional[str] = ".cache",
        default_timeout: float = 30.0,
        default_wait_time: float = 2.0
    ):
        """
        Initialize browser manager.
        
        Args:
            proxy_manager: Optional proxy manager for rotating proxies
            user_agents: Optional list of user agents to use
            cache_dir: Directory for caching responses
            default_timeout: Default timeout for requests in seconds
            default_wait_time: Default time to wait for page load in seconds
        """
        self.proxy_manager = proxy_manager
        self.user_agents = user_agents or USER_AGENTS
        self.cache_dir = cache_dir
        self.default_timeout = default_timeout
        self.default_wait_time = default_wait_time
        
        # Track browser statistics
        self.stats = {
            "requests": 0,
            "errors": 0,
            "cached_hits": 0,
            "proxy_switches": 0
        }
    
    def get_random_user_agent(self, device_type: Optional[str] = None) -> str:
        """
        Get a random user agent string, optionally filtered by device type.
        
        Args:
            device_type: Optional device type to filter by (desktop, mobile, tablet)
            
        Returns:
            str: User agent string
        """
        if device_type:
            filtered_agents = [ua for ua in self.user_agents if ua.device_type == device_type]
            if filtered_agents:
                return random.choice(filtered_agents).string
        return random.choice(self.user_agents).string
    
    def get_browser_config(
        self,
        config: Dict,
        session_id: Optional[str] = None
    ) -> BrowserConfig:
        """
        Get browser configuration with optional proxy and random user agent.
        
        Args:
            config: Configuration dictionary
            session_id: Optional session identifier
            
        Returns:
            BrowserConfig: Browser configuration
        """
        # Get proxy if available
        proxy = None
        if self.proxy_manager and self.proxy_manager.proxy_count > 0:
            proxy = self.proxy_manager.get_next_proxy()
            if proxy:
                self.stats["proxy_switches"] += 1
                logger.debug(f"Using proxy: {proxy}")
        
        # Get user agent based on device preference
        device_type = config.get("DEVICE_TYPE")
        user_agent = self.get_random_user_agent(device_type)
        
        return BrowserConfig(
            browser_type=config.get("BROWSER_TYPE", "chromium"),
            headless=config.get("HEADLESS", True),
            proxy=proxy,
            user_agent=user_agent,
            timeout=config.get("TIMEOUT", self.default_timeout),
            viewport=config.get("VIEWPORT", {"width": 1280, "height": 800}),
            verbose=config.get("VERBOSE_LOGGING", True)
        )
    
    def get_crawler_config(
        self,
        cache_mode: CacheMode = CacheMode.BYPASS,
        session_id: Optional[str] = None,
        **kwargs
    ) -> CrawlerRunConfig:
        """
        Get crawler run configuration.
        
        Args:
            cache_mode: Cache mode to use
            session_id: Optional session identifier
            **kwargs: Additional configuration options
            
        Returns:
            CrawlerRunConfig: Crawler configuration
        """
        if cache_mode != CacheMode.BYPASS and self.cache_dir:
            self.stats["cached_hits"] += 1
        
        return CrawlerRunConfig(
            cache_mode=cache_mode,
            cache_dir=self.cache_dir,
            session_id=session_id,
            wait_until=kwargs.get("wait_until", "networkidle"),
            wait_time=kwargs.get("wait_time", self.default_wait_time),
            **kwargs
        )
    
    def update_stats(self, success: bool = True):
        """Update browser statistics."""
        self.stats["requests"] += 1
        if not success:
            self.stats["errors"] += 1
    
    def get_stats(self) -> Dict:
        """Get current browser statistics."""
        return {
            **self.stats,
            "success_rate": (
                (self.stats["requests"] - self.stats["errors"]) /
                self.stats["requests"] * 100
                if self.stats["requests"] > 0 else 0
            )
        }
    
    def reset_stats(self):
        """Reset browser statistics."""
        self.stats = {k: 0 for k in self.stats}