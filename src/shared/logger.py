import logging
import os
from src.shared import config


def _configure_root_logger():
    if getattr(_configure_root_logger, "_configured", False):
        return
    level_name = getattr(config, "LOG_LEVEL", "INFO")
    level = getattr(logging, level_name, logging.INFO)
    fmt = (
        "%(asctime)s %(levelname)s %(process)d "
        "%(name)s %(filename)s:%(lineno)d %(message)s"
    )
    logging.basicConfig(level=level, format=fmt)
    _configure_root_logger._configured = True


def get_logger(name: str = __name__):
    _configure_root_logger()
    logger = logging.getLogger(name)
    try:
        level_name = getattr(config, "LOG_LEVEL", "INFO")
        logger.setLevel(getattr(logging, level_name, logging.INFO))
    except Exception:
        pass
    return logger
