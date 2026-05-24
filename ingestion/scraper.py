# ingestion/scraper.py

import json
import time
import requests
import pandas as pd
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

from ingestion.config import (
    BASE_URL, HEADERS, DELAY_SECONDS, MAX_WORKERS,
    BATCH_SIZE, START_DATE, END_DATE, METER_IDS_PATH
)
from ingestion.storage import (
    insert_metering_batch, mark_checkpoint, get_completed_pairs
)


def load_meter_ids() -> list[str]:
    with open(METER_IDS_PATH) as f:
        return [line.strip() for line in f if line.strip()]


def date_range(start, end) -> list[str]:
    dates, current = [], start
    while current <= end:
        dates.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)
    return dates


def fetch_one(meter_id: str, date_iso: str) -> tuple[list[dict], str]:
    """
    Fetch a single (meter_id, date) pair.
    Returns (records, status) where status is 'ok' | 'empty' | 'error'
    """
    payload = json.dumps({"meterID": meter_id, "dateISO": date_iso})
    try:
        resp = requests.post(BASE_URL, headers=HEADERS, data=payload, timeout=15)
        resp.raise_for_status()
        inner = json.loads(resp.json()["d"])
        records = inner.get("data", [])

        if not records:
            return [], "empty"

        rows = [
            {
                "meter_id": meter_id,
                "datetime": r["x"],
                "value":    r["y"],
            }
            for r in records
        ]
        return rows, "ok"

    except Exception as e:
        print(f"  ERROR {meter_id} {date_iso}: {e}")
        return [], "error"


def build_task_list(meter_ids: list[str], dates: list[str]) -> list[tuple]:
    """Skip already completed (meter_id, date) pairs."""
    completed = get_completed_pairs()
    tasks = [
        (m, d) for m in meter_ids for d in dates
        if (m, d) not in completed
    ]
    skipped = len(meter_ids) * len(dates) - len(tasks)
    print(f"Total tasks : {len(meter_ids) * len(dates)}")
    print(f"Skipped     : {skipped} (already scraped)")
    print(f"Remaining   : {len(tasks)}")
    return tasks


def _flush(batch: list[dict]) -> int:
    """Parse datetimes and flush batch to DuckDB."""
    df = pd.DataFrame(batch)
    df["datetime"] = pd.to_datetime(df["datetime"], format="%d/%m/%Y %H:%M")
    return insert_metering_batch(df)


def run_scraper(meter_ids: list[str] | None = None, test_mode: bool = False) -> None:
    """
    Main scraper entrypoint.
    - test_mode: limits to first 3 meters x 7 days for quick validation
    """
    all_meter_ids = load_meter_ids() if meter_ids is None else meter_ids
    dates = date_range(START_DATE, END_DATE)

    if test_mode:
        all_meter_ids = all_meter_ids[:3]
        dates = dates[:7]
        print("TEST MODE — 3 meters x 7 days")

    tasks = build_task_list(all_meter_ids, dates)
    if not tasks:
        print("Nothing to scrape — all tasks already completed.")
        return

    total      = len(tasks)
    done       = 0
    inserted   = 0
    errors     = 0
    batch      = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(fetch_one, m, d): (m, d)
            for m, d in tasks
        }

        for future in as_completed(futures):
            meter_id, date_iso = futures[future]
            rows, status = future.result()

            mark_checkpoint(meter_id, date_iso, status)

            if status == "error":
                errors += 1
            else:
                batch.extend(rows)

            # Flush batch to DuckDB
            if len(batch) >= BATCH_SIZE:
                inserted += _flush(batch)
                batch.clear()

            done += 1
            time.sleep(DELAY_SECONDS / MAX_WORKERS)

            if done % 500 == 0 or done == total:
                pct = 100 * done // total
                print(
                    f"[{pct:3d}%] {done}/{total} tasks | "
                    f"{inserted} rows inserted | "
                    f"{errors} errors"
                )

    # Flush remaining
    if batch:
        inserted += _flush(batch)

    print(f"\nDone. {inserted} rows inserted | {errors} errors.")