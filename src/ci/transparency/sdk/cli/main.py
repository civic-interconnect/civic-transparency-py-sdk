"""
CLI for civic transparency simulation core.

Minimal interface for basic data generation and conversion utilities.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional


def cmd_generate_baseline(args: argparse.Namespace) -> None:
    """Generate world - automatically choose baseline or influenced based on parameters."""
    import subprocess

    # Check if any influence parameters are provided
    has_influence_params = any(
        [
            getattr(args, "dup_mult", None) is not None,
            getattr(args, "burst_minutes", None) is not None,
            getattr(args, "reply_nudge", None) is not None,
        ]
    )

    if has_influence_params:
        # Use the influenced world generator
        cmd = [
            sys.executable,
            "-m",
            "scripts_py.gen_world_b_light",
            "--topic-id",
            args.topic_id,
            "--windows",
            str(args.windows),
            "--step-minutes",
            str(args.step_minutes),
            "--out",
            args.out,
            "--seed",
            str(args.seed),
        ]
        if args.dup_mult:
            cmd.extend(["--dup-mult", str(args.dup_mult)])
        if args.burst_minutes:
            cmd.extend(["--burst-minutes", str(args.burst_minutes)])
        if args.reply_nudge:
            cmd.extend(["--reply-nudge", str(args.reply_nudge)])
    else:
        # Use baseline generator
        cmd = [
            sys.executable,
            "-m",
            "scripts_py.gen_empty_world",
            "--world",
            args.world,
            "--topic-id",
            args.topic_id,
            "--windows",
            str(args.windows),
            "--step-minutes",
            str(args.step_minutes),
            "--out",
            args.out,
            "--seed",
            str(args.seed),
        ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(result.stdout)


def cmd_convert(args: argparse.Namespace) -> None:
    """Convert JSONL to DuckDB - wrapper for jsonl_to_duckdb."""
    import subprocess

    cmd = [
        sys.executable,
        "-m",
        "scripts_py.jsonl_to_duckdb",
        "--jsonl",
        args.jsonl,
        "--duck",
        args.duck,
        "--schema",
        args.schema,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(result.stdout)


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser."""
    parser = argparse.ArgumentParser(
        prog="ct-sdk",
        description="Civic Transparency Simulation Core - Basic data generation utilities",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate world (baseline or influenced)
    gen_parser = subparsers.add_parser("generate", help="Generate synthetic world")
    gen_parser.add_argument("--world", required=True, help="World identifier")
    gen_parser.add_argument("--topic-id", required=True, help="Topic identifier")
    gen_parser.add_argument(
        "--windows", type=int, default=12, help="Number of time windows"
    )
    gen_parser.add_argument(
        "--step-minutes", type=int, default=10, help="Minutes per window"
    )
    gen_parser.add_argument("--out", required=True, help="Output JSONL file")
    gen_parser.add_argument("--seed", type=int, default=4242, help="Random seed")
    # Optional influence parameters
    gen_parser.add_argument(
        "--dup-mult", type=float, help="Duplicate multiplier for influence"
    )
    gen_parser.add_argument("--burst-minutes", type=int, help="Micro-burst duration")
    gen_parser.add_argument(
        "--reply-nudge", type=float, help="Reply proportion adjustment"
    )
    gen_parser.set_defaults(func=cmd_generate_baseline)

    # Convert JSONL to DuckDB
    convert_parser = subparsers.add_parser("convert", help="Convert JSONL to DuckDB")
    convert_parser.add_argument("--jsonl", required=True, help="Input JSONL file")
    convert_parser.add_argument("--duck", required=True, help="Output DuckDB file")
    convert_parser.add_argument("--schema", required=True, help="Schema SQL file")
    convert_parser.set_defaults(func=cmd_convert)

    return parser


def main(args: Optional[List[str]] = None) -> int:
    """Main CLI entry point."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        parser.print_help()
        return 1

    try:
        parsed_args.func(parsed_args)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
