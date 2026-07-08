"""
Application settings.
"""

from pathlib import Path
import os

from dotenv import load_dotenv

# --------------------------------------------------
# Base Directory
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env from project root
load_dotenv(BASE_DIR / ".env")

# --------------------------------------------------
# Telegram
# --------------------------------------------------

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

OWNER_ID = int(
    os.getenv(
        "OWNER_ID",
        "0",
    )
)

# --------------------------------------------------
# Database
# --------------------------------------------------

DATABASE = BASE_DIR / os.getenv(
    "DATABASE",
    "data/mirror.db",
)

# --------------------------------------------------
# Downloads
# --------------------------------------------------

DOWNLOAD_DIR = BASE_DIR / os.getenv(
    "DOWNLOAD_DIR",
    "downloads",
)

# --------------------------------------------------
# Logs
# --------------------------------------------------

LOG_DIR = BASE_DIR / "logs"

# --------------------------------------------------
# Logging
# --------------------------------------------------

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
).upper()

# --------------------------------------------------
# Retry Settings
# --------------------------------------------------

MAX_RETRIES = int(
    os.getenv(
        "MAX_RETRIES",
        "3",
    )
)

# --------------------------------------------------
# Rate Limiting
# --------------------------------------------------

RATE_LIMIT_PER_MINUTE = int(
    os.getenv(
        "RATE_LIMIT_PER_MINUTE",
        "80",
    )
)

# --------------------------------------------------
# Ensure Required Directories Exist
# --------------------------------------------------

DATABASE.parent.mkdir(
    parents=True,
    exist_ok=True,
)

DOWNLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)