# ingestion/run_scraper.py

import argparse
from ingestion.config import RAW_DIR
from ingestion.storage import init_db, load_charging_sessions
from ingestion.scraper import run_scraper


def parse_args():
    parser = argparse.ArgumentParser(description="NCL Metering Scraper")
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run in test mode (3 meters x 7 days)"
    )
    parser.add_argument(
        "--load-sessions",
        action="store_true",
        help="Load supervisor CSV into charging_sessions table"
    )
    parser.add_argument(
        "--scrape",
        action="store_true",
        help="Scrape the metering portal (needs NCL_METERING_COOKIE in .env)"
    )
    parser.add_argument(
        "--sessions-csv",
        type=str,
        default=str(RAW_DIR / "usb_merged_final_data.csv"),
        help="Path to supervisor charging sessions CSV"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Step 1 - always initialise DB first
    init_db()

    # Step 2 - optionally load charging sessions
    if args.load_sessions:
        load_charging_sessions(args.sessions_csv)

    # Step 3 - scrape only when asked. The metering scrape is a 28.7M-row job
    # against a cookie-authenticated portal, and its output was investigated
    # then excluded (see notebooks/00); loading the session CSV must not
    # trigger it as a side effect.
    if args.scrape or args.test:
        run_scraper(test_mode=args.test)


if __name__ == "__main__":
    main()