import logging


def setup_logging() -> None:
    """Configures the global logging settings for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format=(
            '%(filename)s:%(lineno)d #%(levelname)-8s '
            '[%(asctime)s] - %(name)s - %(message)s'
        ),
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """Returns a configured logger instance for the given name."""
    return logging.getLogger(name)
