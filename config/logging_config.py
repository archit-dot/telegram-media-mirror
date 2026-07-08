import logging

from logging.handlers import RotatingFileHandler

from config.settings import LOG_DIR, LOG_LEVEL


def setup_logging() -> None:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    root = logging.getLogger()

    root.setLevel(LOG_LEVEL)

    if root.handlers:
        return

    console = logging.StreamHandler()

    console.setFormatter(formatter)

    root.addHandler(console)

    activity = RotatingFileHandler(
        LOG_DIR / "activity.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )

    activity.setFormatter(formatter)

    activity.setLevel(logging.INFO)

    root.addHandler(activity)

    error = RotatingFileHandler(
        LOG_DIR / "error.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )

    error.setFormatter(formatter)

    error.setLevel(logging.ERROR)

    root.addHandler(error)