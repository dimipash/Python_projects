import logging
import sys

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)-10s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


_configured = False


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:

    global _configured

    if not _configured:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT))

        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        root_logger.addHandler(handler)

        _configured = True

    return logging.getLogger(name)
