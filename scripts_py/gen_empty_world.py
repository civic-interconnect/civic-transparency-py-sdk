# scripts_py/gen_empty_world.py
"""Generate a synthetic organic world JSONL for smoke tests.

Usage:
  py -m scripts_py.gen_empty_world ^
     --world A ^
     --topic-id aa55ee77 ^
     --windows 12 ^
     --step-minutes 10 ^
     --out data/jsonl/world_A.jsonl ^
     --seed 4242
"""

import argparse
from datetime import UTC, datetime, timedelta
from math import sqrt
from pathlib import Path
import random
import secrets

from ci.transparency.sdk import (
    ContentHash,
    Digests,
    HashId,
    MinHashSig,
    SimHash64,
    TopHash,
    WindowAgg,
    dumps,
    windowagg_to_json,
)


def herfindahl(counts: list[int]) -> float:
    """Herfindahl-Hirschman Index: sum of squares of market shares."""
    total = sum(counts) or 1
    return sum((c / total) ** 2 for c in counts)


def cv_of_bins(bins: list[int]) -> float:
    """Coefficient of variation (stddev/mean) of a histogram."""
    n = len(bins) or 1
    mean = sum(bins) / n
    if mean == 0:
        return 0.0
    var = sum((x - mean) ** 2 for x in bins) / n
    return sqrt(var) / mean


def make_window(
    i: int,
    *,
    world: str,
    topic_id: str,
    windows: int,
    step_minutes: int,
    seed_rng: random.Random,
    t0: datetime,
) -> WindowAgg:
    """Build one WindowAgg for window index i."""
    start = t0 + timedelta(minutes=int(i * step_minutes))
    end = start + timedelta(minutes=step_minutes)

    phase = i / max(1, windows - 1)
    base = 50 + int(150 * (1 - (2 * phase - 1) ** 2))  # bell-ish 50..200

    top = [
        TopHash(hash=ContentHash(HashId("opaque", "h1")), count=8 + (i % 3)),
        TopHash(hash=ContentHash(HashId("opaque", "h2")), count=6 + ((i + 1) % 3)),
        TopHash(hash=ContentHash(HashId("opaque", "h3")), count=4 + ((i + 2) % 2)),
    ]
    n_top = sum(t.count for t in top)
    n_messages = base + seed_rng.randint(-10, 10)
    n_unique = max(1, n_messages - n_top - seed_rng.randint(0, 5))
    dup_rate = 1.0 - (n_unique / float(n_messages))
    hhi = herfindahl([t.count for t in top])

    minutes = step_minutes
    series = [max(0, int((n_messages / minutes) + seed_rng.randint(-2, 2))) for _ in range(minutes)]
    burst = cv_of_bins(series)

    dig = Digests(
        simhash64=SimHash64(bits=0x9F3A5C10AA55EE77 ^ i),
        minhash=MinHashSig(k=4, sig=tuple((j + 1) * (i + 1) for j in range(4))),
    )

    return WindowAgg(
        world_id=world,
        topic_id=topic_id,
        window_start=start,
        window_end=end,
        n_messages=n_messages,
        n_unique_hashes=n_unique,
        dup_rate=dup_rate,
        top_hashes=top,
        hash_concentration=hhi,
        burst_score=burst,
        type_mix={"post": 0.52, "reply": 0.30, "retweet": 0.18},
        time_histogram=series,
        digests=dig,
    )


def main() -> None:
    """Parse arguments and generate a synthetic organic world JSONL file for smoke tests."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--world", required=True)
    ap.add_argument("--topic-id", required=True)
    ap.add_argument("--windows", type=int, default=12)
    ap.add_argument("--step-minutes", type=int, default=10)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--seed", type=int, default=4242)
    args = ap.parse_args()

    # ensure parent folder exists
    args.out.parent.mkdir(parents=True, exist_ok=True)

    rng = secrets.SystemRandom()
    t0 = datetime.now(UTC).replace(microsecond=0)

    rows: list[WindowAgg] = [
        make_window(
            i,
            world=args.world,
            topic_id=args.topic_id,
            windows=args.windows,
            step_minutes=args.step_minutes,
            seed_rng=rng,
            t0=t0,
        )
        for i in range(args.windows)
    ]

    with args.out.open("wb") as f:
        for r in rows:
            f.write(dumps(windowagg_to_json(r)))
            f.write(b"\n")

    print(f"Wrote {len(rows)} windows to {args.out}")


if __name__ == "__main__":
    main()
