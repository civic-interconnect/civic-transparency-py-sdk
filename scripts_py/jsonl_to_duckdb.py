# scripts_py/jsonl_to_duckdb.py
"""
Load a JSONL file of window aggregation results into a DuckDB database.

Usage:
  py -m scripts_py.jsonl_to_duckdb --jsonl world_A.jsonl --duck world_A.duckdb --schema schema/schema.sql
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import duckdb

EVENTS_TABLE = "events"


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Load JSONL into DuckDB.")
    ap.add_argument("--jsonl", required=True, type=Path)
    ap.add_argument("--duck", required=True, type=Path)
    ap.add_argument(
        "--schema",
        required=True,
        type=Path,
        help="SQL to create the 'events' table (used only if missing).",
    )
    return ap.parse_args()


def table_exists(con: duckdb.DuckDBPyConnection, name: str) -> bool:
    row = con.execute(
        "SELECT 1 FROM information_schema.tables WHERE table_schema = 'main' AND table_name = ? LIMIT 1",
        [name],
    ).fetchone()
    return row is not None


def load_jsonl_rows(jsonl_path: Path) -> List[Dict]:
    rows: List[Dict] = []
    with jsonl_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def parse_ts(s: str) -> datetime:
    return datetime.fromisoformat(s.rstrip("Z"))


def to_params(row: Dict) -> list:
    tmix = row["type_mix"]
    return [
        row.get("world_id", ""),
        row.get("topic_id", ""),
        parse_ts(row["window_start"]),
        parse_ts(row["window_end"]),
        int(row["n_messages"]),
        int(row["n_unique_hashes"]),
        float(row["dup_rate"]),
        json.dumps(row["top_hashes"]),
        float(row["hash_concentration"]),
        float(row["burst_score"]),
        float(tmix["post"]),
        float(tmix["reply"]),
        float(tmix["retweet"]),
        json.dumps(row["time_histogram"]),
    ]


def main() -> None:
    args = parse_args()

    if not args.jsonl.exists():
        raise FileNotFoundError(f"JSONL not found: {args.jsonl}")
    if not args.schema.exists():
        raise FileNotFoundError(f"Schema SQL not found: {args.schema}")

    args.duck.parent.mkdir(parents=True, exist_ok=True)

    rows = load_jsonl_rows(args.jsonl)
    if not rows:
        print(f"No rows found in {args.jsonl}; nothing to load.")
        return

    con = duckdb.connect(str(args.duck))
    try:
        # Create table if missing
        if not table_exists(con, EVENTS_TABLE):
            with args.schema.open("r", encoding="utf-8") as f:
                con.execute(f.read())

        # Simple truncate and insert
        con.execute(f"DELETE FROM {EVENTS_TABLE}")

        # Insert all rows
        insert_sql = f"""
        INSERT INTO {EVENTS_TABLE}(
          world_id, topic_id, window_start, window_end,
          n_messages, n_unique_hashes, dup_rate, top_hashes,
          hash_concentration, burst_score, type_post, type_reply,
          type_retweet, time_histogram
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        con.executemany(insert_sql, [to_params(r) for r in rows])

    finally:
        con.close()

    print(f"Loaded {len(rows)} rows into {args.duck}")


if __name__ == "__main__":
    main()
