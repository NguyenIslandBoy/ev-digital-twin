# ingestion/storage.py

import duckdb
import pandas as pd
from ingestion.config import DB_PATH


def get_connection() -> duckdb.DuckDBPyConnection:
    return duckdb.connect(str(DB_PATH))


def init_db() -> None:
    """Create tables if they don't exist."""
    with get_connection() as con:
        # Raw 30-min interval metering data
        con.execute("""
            CREATE TABLE IF NOT EXISTS metering_raw (
                meter_id  VARCHAR,
                datetime  TIMESTAMP,
                value     DOUBLE,
                PRIMARY KEY (meter_id, datetime)
            )
        """)

        # Checkpoint table — tracks which (meter_id, date) pairs are done
        con.execute("""
            CREATE TABLE IF NOT EXISTS scrape_checkpoint (
                meter_id  VARCHAR,
                date      DATE,
                status    VARCHAR,  -- 'ok' | 'empty' | 'error'
                PRIMARY KEY (meter_id, date)
            )
        """)

        # Charging sessions from supervisor CSV — loaded once
        con.execute("""
            CREATE TABLE IF NOT EXISTS charging_sessions (
                id                          VARCHAR PRIMARY KEY,
                session_start               TIMESTAMP,
                session_stop                TIMESTAMP,
                connector_type              VARCHAR,
                energy_kwh                  DOUBLE,
                auth_type                   VARCHAR,
                auth_id                     BIGINT,
                charger_id                  BIGINT,
                location_id                 BIGINT,
                duration_hrs                DOUBLE,
                time_based_util_rate        DOUBLE,
                month                       INTEGER,
                season                      VARCHAR,
                day                         VARCHAR,
                carbon_intensity_gco2_kwh   INTEGER,
                carbon_emissions_gco2       DOUBLE
            )
        """)
    print(f"Database initialised at {DB_PATH}")


def insert_metering_batch(df: pd.DataFrame) -> int:
    """Insert a batch of metering rows, ignoring duplicates. Returns rows inserted."""
    if df.empty:
        return 0
    with get_connection() as con:
        con.execute("""
            INSERT OR IGNORE INTO metering_raw (meter_id, datetime, value)
            SELECT meter_id, datetime, value FROM df
        """)
    return len(df)


def mark_checkpoint(meter_id: str, date: str, status: str) -> None:
    """Record that a (meter_id, date) pair has been attempted."""
    with get_connection() as con:
        con.execute("""
            INSERT OR REPLACE INTO scrape_checkpoint (meter_id, date, status)
            VALUES (?, ?, ?)
        """, [meter_id, date, status])


def get_completed_pairs() -> set[tuple]:
    """Return all (meter_id, date) pairs already scraped successfully."""
    with get_connection() as con:
        result = con.execute("""
            SELECT meter_id, CAST(date AS VARCHAR)
            FROM scrape_checkpoint
            WHERE status IN ('ok', 'empty')
        """).fetchall()
    return set(result)


def load_charging_sessions(csv_path: str) -> int:
    """Load supervisor CSV into charging_sessions table. Safe to call multiple times."""
    with get_connection() as con:
        existing = con.execute("SELECT COUNT(*) FROM charging_sessions").fetchone()[0]
        if existing > 0:
            print(f"charging_sessions already loaded ({existing} rows), skipping.")
            return existing
        con.execute(f"""
            INSERT INTO charging_sessions
            SELECT
                id,
                strptime(CAST(sessionStart AS VARCHAR), '%d/%m/%Y %H:%M')        AS session_start,
                strptime(CAST(sessionStop AS VARCHAR), '%d/%m/%Y %H:%M')        AS session_stop,
                connectorType                                    AS connector_type,
                "energy_consumption(kWh)"                       AS energy_kwh,
                authType                                         AS auth_type,
                authId                                           AS auth_id,
                chargerId                                        AS charger_id,
                locationId                                       AS location_id,
                duration_hrs,
                time_based_util_rate,
                Month                                            AS month,
                Season                                           AS season,
                day,
                "Carbon Intensity (gCO2/kWh)"                   AS carbon_intensity_gco2_kwh,
                "Carbon Emissions (gCO2)"                       AS carbon_emissions_gco2
            FROM read_csv_auto('{csv_path}', all_varchar=True)
        """)
        count = con.execute("SELECT COUNT(*) FROM charging_sessions").fetchone()[0]
    print(f"Loaded {count} charging sessions.")
    return count