import logging
import sys
from pathlib import Path
from typing import Optional

def setup_logger(
    name: str = "deepseek_crawler",
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up a logger with both console and file handlers.
    
    Args:
        name: Name of the logger
        log_file: Path to the log file (optional)
        level: Logging level
        format_string: Custom format string for log messages
        
    Returns:
        logging.Logger: Configured logger instance
    """
    if format_string is None:
        format_string = "[%(asctime)s] %(levelname)s [%(name)s] %(message)s"
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create formatters and handlers
    formatter = logging.Formatter(format_string)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log_file is provided)
    if log_file:
        # Create logs directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Create default logger instance
logger = setup_logger()