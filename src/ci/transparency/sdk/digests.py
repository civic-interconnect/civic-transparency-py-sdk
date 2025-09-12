"""
sdk/digests.py
Optional similarity digests for content hashes.
"""

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class SimHash64:
    bits: int  # store as Python int (0..2^64-1)


@dataclass(frozen=True)
class MinHashSig:
    k: int
    sig: Tuple[int, ...]  # immutable tuple


@dataclass(frozen=True)
class Digests:
    """Optional similarity digests; any field may be None."""

    simhash64: Optional[SimHash64] = None
    minhash: Optional[MinHashSig] = None
