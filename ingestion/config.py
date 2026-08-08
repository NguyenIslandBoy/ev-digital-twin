# ingestion/config.py

from datetime import datetime
from pathlib import Path
import os

from dotenv import load_dotenv

# ── PATHS ─────────────────────────────────────────────────────────────────────
ROOT_DIR      = Path(__file__).resolve().parent.parent

# The metering-portal cookie lives in <repo_root>/.env (gitignored). Load it
# explicitly so the scraper works from any working directory.
load_dotenv(ROOT_DIR / ".env")
DATA_DIR      = ROOT_DIR / "data"
RAW_DIR       = DATA_DIR / "raw"
DB_PATH       = DATA_DIR / "ev_twin.duckdb"
METER_IDS_PATH = RAW_DIR / "meter_ids.txt"

# ── SCRAPER ───────────────────────────────────────────────────────────────────
BASE_URL      = "https://metering.ncl.ac.uk/profiles/dailyprofile.aspx/GetProfile"
SESSION_COOKIE = os.environ.get("NCL_METERING_COOKIE", "")  # refresh when expired (in .env)

HEADERS = {
    "Content-Type": "application/json; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://metering.ncl.ac.uk/profiles/dailyprofile.aspx",
    "Cookie": SESSION_COOKIE,
}

# ── DATE RANGE ────────────────────────────────────────────────────────────────
START_DATE    = datetime(2021, 3, 18)
END_DATE      = datetime(2024, 7, 1)

# ── SCRAPER BEHAVIOUR ─────────────────────────────────────────────────────────
DELAY_SECONDS  = 0.5
MAX_WORKERS    = 5
BATCH_SIZE     = 1000  # rows before flushing to duckdb