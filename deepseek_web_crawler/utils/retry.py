import asyncio
import time
from functools import wraps
from typing import Any, Callable, Optional, Type, Union

from utils.logger import logger

class RetryError(Exception):
    """Raised when all retry attempts have been exhausted."""
    pass

class RateLimiter:
    """Rate limiter for controlling request frequency."""
    
    def __init__(self, calls: int, period: float):
        """
        Initialize rate limiter.
        
        Args:
            calls: Number of calls allowed
            period: Time period in seconds
        """
        self.calls = calls
        self.period = period
        self.timestamps = []
    
    async def acquire(self):
        """Wait if necessary to stay within rate limits."""
        now = time.time()
        
        # Remove timestamps outside the current period
        self.timestamps = [ts for ts in self.timestamps if now - ts <= self.period]
        
        if len(self.timestamps) >= self.calls:
            # Wait until the oldest timestamp is outside the period
            sleep_time = self.timestamps[0] + self.period - now
            if sleep_time > 0:
                logger.debug(f"Rate limit reached. Waiting {sleep_time:.2f} seconds")
                await asyncio.sleep(sleep_time)
                # Recalculate now after sleeping
                now = time.time()
        
        self.timestamps.append(now)

def async_retry(
    retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Union[Type[Exception], tuple[Type[Exception], ...]] = Exception,
    rate_limit: Optional[tuple[int, float]] = None
):
    """
    Decorator for retrying async functions with exponential backoff.
    
    Args:
        retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each retry
        exceptions: Exception types to catch and retry
        rate_limit: Optional tuple of (calls, period) for rate limiting
        
    Returns:
        Decorated function that implements retry logic
    """
    def decorator(func: Callable) -> Callable:
        limiter = RateLimiter(*rate_limit) if rate_limit else None
        
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_delay = delay
            last_exception = None
            
            for attempt in range(retries + 1):
                try:
                    if limiter:
                        await limiter.acquire()
                    
                    return await func(*args, **kwargs)
                    
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == retries:
                        logger.error(
                            f"All {retries} retry attempts failed for {func.__name__}. "
                            f"Last error: {str(e)}"
                        )
                        raise RetryError(
                            f"Function {func.__name__} failed after {retries} retries. "
                            f"Last error: {str(e)}"
                        ) from e
                    
                    logger.warning(
                        f"Attempt {attempt + 1}/{retries} failed for {func.__name__}. "
                        f"Error: {str(e)}. Retrying in {current_delay:.2f} seconds..."
                    )
                    
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff
            
            # This should never be reached due to the raise in the loop
            raise RetryError("Unexpected error in retry logic") from last_exception
        
        return wrapper
    
    return decorator