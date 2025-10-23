"""CLI for civic transparency simulation core."""

from pathlib import Path
import subprocess
import sys
from typing import Annotated

import typer

app = typer.Typer(
    name="ct-sdk",
    help="Civic Transparency Simulation Core - Basic data generation utilities",
    no_args_is_help=True,
)


@app.command()
def generate(
    world: Annotated[str, typer.Option(help="World identifier")],
    topic_id: Annotated[str, typer.Option("--topic-id", help="Topic identifier")],
    out: Annotated[Path, typer.Option(help="Output JSONL file")],
    windows: Annotated[int, typer.Option(help="Number of time windows")] = 12,
    step_minutes: Annotated[int, typer.Option("--step-minutes", help="Minutes per window")] = 10,
    seed: Annotated[int, typer.Option(help="Random seed")] = 4242,
    # Optional influence parameters
    dup_mult: Annotated[
        float | None, typer.Option("--dup-mult", help="Duplicate multiplier for influence")
    ] = None,
    burst_minutes: Annotated[
        int | None, typer.Option("--burst-minutes", help="Micro-burst duration")
    ] = None,
    reply_nudge: Annotated[
        float | None, typer.Option("--reply-nudge", help="Reply proportion adjustment")
    ] = None,
) -> None:
    """Generate synthetic world (baseline or influenced based on parameters)."""
    # Check if any influence parameters are provided
    has_influence = any([dup_mult, burst_minutes, reply_nudge])

    if has_influence:
        # Use the influenced world generator
        cmd = [
            sys.executable,
            "-m",
            "scripts_py.gen_world_b_light",
            "--topic-id",
            topic_id,
            "--windows",
            str(windows),
            "--step-minutes",
            str(step_minutes),
            "--out",
            str(out),
            "--seed",
            str(seed),
        ]
        if dup_mult:
            cmd.extend(["--dup-mult", str(dup_mult)])
        if burst_minutes:
            cmd.extend(["--burst-minutes", str(burst_minutes)])
        if reply_nudge:
            cmd.extend(["--reply-nudge", str(reply_nudge)])
    else:
        # Use baseline generator
        cmd = [
            sys.executable,
            "-m",
            "scripts_py.gen_empty_world",
            "--world",
            world,
            "--topic-id",
            topic_id,
            "--windows",
            str(windows),
            "--step-minutes",
            str(step_minutes),
            "--out",
            str(out),
            "--seed",
            str(seed),
        ]

    result = subprocess.run(cmd, capture_output=True, text=True)  # noqa: S603
    if result.returncode != 0:
        typer.echo(f"Error: {result.stderr}", err=True)
        raise typer.Exit(code=1)
    typer.echo(result.stdout)


@app.command()
def convert(
    jsonl: Annotated[Path, typer.Option(help="Input JSONL file")],
    duck: Annotated[Path, typer.Option(help="Output DuckDB file")],
    schema: Annotated[Path, typer.Option(help="Schema SQL file")],
) -> None:
    """Convert JSONL to DuckDB."""
    cmd = [
        sys.executable,
        "-m",
        "scripts_py.jsonl_to_duckdb",
        "--jsonl",
        str(jsonl),
        "--duck",
        str(duck),
        "--schema",
        str(schema),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)  # noqa: S603
    if result.returncode != 0:
        typer.echo(f"Error: {result.stderr}", err=True)
        raise typer.Exit(code=1)
    typer.echo(result.stdout)


def main() -> None:
    """Return the main CLI entry point."""
    app()


if __name__ == "__main__":
    main()
