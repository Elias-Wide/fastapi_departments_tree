import logging


def get_logger(name: str) -> logging.Logger:
    """Returns a configured logger instance for the given name."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
        '[%(asctime)s] - %(name)s - %(message)s',
    )
    return logging.getLogger(name)
