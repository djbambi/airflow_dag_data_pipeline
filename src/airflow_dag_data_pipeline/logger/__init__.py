import logging
from pathlib import Path


def get_logger(name: str) -> logging.Logger:
    log = logging.getLogger(name)

    # Configure the logger only once to avoid duplicate handlers and log entries
    if not log.handlers:
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        # Use pathlib for the log file path
        log_file = log_dir / "log.txt"
        handler = logging.FileHandler(filename=log_file, mode="a")

        format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(fmt=format_str, datefmt="%Y-%m-%d %H:%M:%S%z")
        handler.formatter = formatter
        log.addHandler(handler)
        log.setLevel(logging.INFO)
    return log
