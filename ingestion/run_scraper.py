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
        "--sessions-csv",
        type=str,
        default=str(RAW_DIR / "usb_merged_final_data.csv"),
        help="Path to supervisor charging sessions CSV"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Step 1 — always initialise DB first
    init_db()

    # Step 2 — optionally load charging sessions
    if args.load_sessions:
        load_charging_sessions(args.sessions_csv)

    # Step 3 — run scraper
    run_scraper(test_mode=args.test)


if __name__ == "__main__":
    main()