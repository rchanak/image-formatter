import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def get_logger(name="imgfmt",
               level="INFO",
               log_dir: Path | None = None) -> logging.Logger:
    
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    format = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")

    ch = logging.StreamHandler()
    ch.setFormatter(format)
    logger.addHandler(ch)

    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_dir / "app.log",
            maxBytes=2_000_000,
            backupCount =3
        )
        file_handler.setFormatter(format)
        logger.addHandler(file_handler)

    return logger