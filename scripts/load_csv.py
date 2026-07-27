#!/usr/bin/env python3
"""Create the tasks table and load rows from data/tasks.csv."""

import csv
import os
import sys
import time
from pathlib import Path

import psycopg

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://app:app@localhost:5432/appdb"
)
CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "tasks.csv"
MAX_ATTEMPTS = 30
RETRY_SECONDS = 2


def wait_for_db() -> psycopg.Connection:
    last_error: Exception | None = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            conn = psycopg.connect(DATABASE_URL)
            conn.execute("SELECT 1")
            print(f"Connected to PostgreSQL (attempt {attempt})")
            return conn
        except Exception as exc:  # noqa: BLE001 - retry until ready
            last_error = exc
            print(f"Waiting for PostgreSQL ({attempt}/{MAX_ATTEMPTS}): {exc}")
            time.sleep(RETRY_SECONDS)
    raise RuntimeError(f"PostgreSQL not ready after {MAX_ATTEMPTS} attempts") from last_error


def load_csv(conn: psycopg.Connection) -> int:
    with CSV_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = [
            (row["title"].strip(), row["done"].strip().lower() in {"true", "1", "yes"})
            for row in reader
        ]

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT FALSE
            )
            """
        )
        cur.execute("TRUNCATE TABLE tasks RESTART IDENTITY")
        cur.executemany(
            "INSERT INTO tasks (title, done) VALUES (%s, %s)",
            rows,
        )
    conn.commit()
    return len(rows)


def main() -> int:
    if not CSV_PATH.is_file():
        print(f"CSV not found: {CSV_PATH}", file=sys.stderr)
        return 1

    with wait_for_db() as conn:
        count = load_csv(conn)
        print(f"Loaded {count} row(s) from {CSV_PATH.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
