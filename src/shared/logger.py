import logging
from src.shared import config


def _configure_root_logger():
    level_name = getattr(config, "LOG_LEVEL", "INFO")
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )


def get_logger(name: str = __name__):
    _configure_root_logger()
    logger = logging.getLogger(name)
    try:
        level_name = getattr(config, "LOG_LEVEL", "INFO")
        logger.setLevel(getattr(logging, level_name, logging.INFO))
    except Exception:
        pass
    return logger
