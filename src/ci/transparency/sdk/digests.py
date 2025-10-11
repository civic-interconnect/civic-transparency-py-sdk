"""Optional similarity digests for content hashes.

sdk/digests.py
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SimHash64:
    """A 64-bit SimHash similarity digest.

    Attributes
    ----------
    bits : int
        The 64-bit hash value stored as a Python integer (0..2^64-1).
    """

    bits: int  # store as Python int (0..2^64-1)


@dataclass(frozen=True)
class MinHashSig:
    """A MinHash signature for similarity estimation.

    Attributes
    ----------
    k : int
        The number of hash functions used in the MinHash signature.
    sig : tuple[int, ...]
        The immutable tuple containing the MinHash values.
    """

    k: int
    sig: tuple[int, ...]  # immutable tuple


@dataclass(frozen=True)
class Digests:
    """Optional similarity digests; any field may be None."""

    simhash64: SimHash64 | None = None
    minhash: MinHashSig | None = None
