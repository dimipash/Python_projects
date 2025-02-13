import sys
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

from utils.logger import logger

@dataclass
class CrawlStats:
    """Statistics for a crawling session."""
    start_time: datetime
    total_pages: int = 0
    current_page: int = 0
    total_items: int = 0
    valid_items: int = 0
    failed_items: int = 0
    duplicate_items: int = 0
    
    @property
    def elapsed_time(self) -> float:
        """Get elapsed time in seconds."""
        return (datetime.now() - self.start_time).total_seconds()
    
    @property
    def items_per_second(self) -> float:
        """Calculate items processed per second."""
        elapsed = self.elapsed_time
        return self.total_items / elapsed if elapsed > 0 else 0
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        return (self.valid_items / self.total_items * 100
                if self.total_items > 0 else 0)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert stats to dictionary."""
        return {
            "elapsed_time": f"{self.elapsed_time:.1f}s",
            "items_per_second": f"{self.items_per_second:.2f}",
            "total_pages": self.total_pages,
            "current_page": self.current_page,
            "total_items": self.total_items,
            "valid_items": self.valid_items,
            "failed_items": self.failed_items,
            "duplicate_items": self.duplicate_items,
            "success_rate": f"{self.success_rate:.1f}%"
        }


class ProgressTracker:
    """Tracks and displays crawling progress."""
    
    def __init__(
        self,
        total_pages: Optional[int] = None,
        show_progress_bar: bool = True,
        update_interval: float = 0.5
    ):
        """
        Initialize progress tracker.
        
        Args:
            total_pages: Total number of pages to crawl (optional)
            show_progress_bar: Whether to show progress bar
            update_interval: Minimum time between progress updates
        """
        self.stats = CrawlStats(start_time=datetime.now())
        self.stats.total_pages = total_pages or 0
        self.show_progress_bar = show_progress_bar
        self.update_interval = update_interval
        self._last_update = 0
        
        # Terminal width for progress bar
        self.term_width = 80
        try:
            import shutil
            self.term_width = shutil.get_terminal_size().columns
        except:
            pass
    
    def update(
        self,
        current_page: Optional[int] = None,
        new_items: int = 0,
        valid_items: int = 0,
        failed_items: int = 0,
        duplicate_items: int = 0
    ):
        """
        Update progress statistics.
        
        Args:
            current_page: Current page number (optional)
            new_items: Number of new items found
            valid_items: Number of valid items
            failed_items: Number of failed items
            duplicate_items: Number of duplicate items
        """
        now = time.time()
        if now - self._last_update < self.update_interval:
            return
        
        if current_page is not None:
            self.stats.current_page = current_page
        
        self.stats.total_items += new_items
        self.stats.valid_items += valid_items
        self.stats.failed_items += failed_items
        self.stats.duplicate_items += duplicate_items
        
        self._display_progress()
        self._last_update = now
    
    def _display_progress(self):
        """Display progress information."""
        if not self.show_progress_bar:
            return
        
        # Clear line
        sys.stdout.write('\r' + ' ' * self.term_width + '\r')
        
        # Basic progress info
        progress = f"Page {self.stats.current_page}"
        if self.stats.total_pages:
            progress += f"/{self.stats.total_pages}"
        
        # Items info
        items_info = (
            f"Items: {self.stats.total_items} "
            f"(Valid: {self.stats.valid_items}, "
            f"Failed: {self.stats.failed_items}, "
            f"Dupes: {self.stats.duplicate_items})"
        )
        
        # Rate info
        rate_info = (
            f"Rate: {self.stats.items_per_second:.1f} items/s "
            f"Success: {self.stats.success_rate:.1f}%"
        )
        
        # Combine all info
        status = f"{progress} | {items_info} | {rate_info}"
        
        # Progress bar if total pages known
        if self.stats.total_pages:
            bar_width = min(50, self.term_width - len(status) - 5)
            if bar_width > 10:
                progress = self.stats.current_page / self.stats.total_pages
                filled = int(bar_width * progress)
                bar = (
                    '['
                    + '=' * filled
                    + '>' * min(1, bar_width - filled)
                    + ' ' * (bar_width - filled - 1)
                    + ']'
                )
                status = f"{bar} {status}"
        
        # Truncate if too long
        if len(status) > self.term_width:
            status = status[:self.term_width - 3] + "..."
        
        sys.stdout.write(status)
        sys.stdout.flush()
    
    def finish(self):
        """Display final statistics."""
        if self.show_progress_bar:
            sys.stdout.write('\n')
        
        logger.info("Crawling completed!")
        logger.info("Final Statistics:")
        for key, value in self.stats.to_dict().items():
            logger.info(f"  {key}: {value}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics as dictionary."""
        return self.stats.to_dict()