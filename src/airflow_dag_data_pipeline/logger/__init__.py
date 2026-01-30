import logging


def get_logger(name: str) -> logging.Logger:
    log = logging.getLogger(name)
    handler = logging.FileHandler(filename="logs/log.txt", mode="a")

    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(fmt=format_str, datefmt="%Y-%m-%d %H:%M:%S%z")
    handler.formatter = formatter
    log.addHandler(handler)
    log.setLevel(logging.INFO)

    return log
