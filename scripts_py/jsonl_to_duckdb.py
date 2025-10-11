# scripts_py/jsonl_to_duckdb.py
"""Load a JSONL file of window aggregation results into a DuckDB database.

Usage:
  py -m scripts_py.jsonl_to_duckdb --jsonl world_A.jsonl --duck world_A.duckdb --schema schema/schema.sql
"""

import argparse
from datetime import datetime
import json
from pathlib import Path
from typing import Any

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
    """Checks if a table with the specified name exists in the 'main' schema of the DuckDB database.

    Args:
        con (duckdb.DuckDBPyConnection): The DuckDB database connection.
        name (str): The name of the table to check for existence.

    Returns:
        bool: True if the table exists, False otherwise.
    """
    row = con.execute(
        "SELECT 1 FROM information_schema.tables WHERE table_schema = 'main' AND table_name = ? LIMIT 1",
        [name],
    ).fetchone()
    return row is not None


def load_jsonl_rows(jsonl_path: Path) -> list[dict[str, Any]]:
    """Load rows from a JSON Lines (JSONL) file.

    Each line in the file is expected to be a valid JSON object. Blank lines are ignored.

    Args:
        jsonl_path (Path): Path to the JSONL file.

    Returns:
        list[dict]: A list of dictionaries, each representing a JSON object from a line in the file.
    """
    rows: list[dict[str, Any]] = []
    with jsonl_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def parse_ts(s: str) -> datetime:
    """Parses an ISO 8601 formatted timestamp string and returns a datetime object.

    Args:
        s (str): The timestamp string to parse. Expected to be in ISO 8601 format, optionally ending with 'Z'.

    Returns:
        datetime: A datetime object representing the parsed timestamp.

    Raises:
        ValueError: If the input string is not a valid ISO 8601 format.
    """
    return datetime.fromisoformat(s.rstrip("Z"))


from typing import Any


def to_params(row: dict[str, Any]) -> list[Any]:
    tmix: dict[str, Any] = row["type_mix"]
    return [
        row.get("world_id", ""),
        row.get("topic_id", ""),  # type: ignore
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
    """Main entry point for loading JSONL data into a DuckDB database.

    This function performs the following steps:
    1. Parses command-line arguments for input JSONL file, schema SQL file, and DuckDB database path.
    2. Checks for existence of the JSONL and schema files.
    3. Ensures the parent directory for the DuckDB database exists.
    4. Loads rows from the JSONL file.
    5. Connects to the DuckDB database.
    6. Creates the events table if it does not exist, using the provided schema.
    7. Truncates the events table.
    8. Inserts all loaded rows into the events table.
    9. Closes the database connection.
    10. Prints the number of rows loaded.

    Raises:
        FileNotFoundError: If the JSONL or schema file does not exist.
    """
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
        con.executemany(insert_sql, [to_params(r) for r in rows])  # type: ignore

    finally:
        con.close()

    print(f"Loaded {len(rows)} rows into {args.duck}")


if __name__ == "__main__":
    main()
