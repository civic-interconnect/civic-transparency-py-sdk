"""
sdk/ids.py
Identifiers for events, content hashes, estimated topics, and worlds.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class EventId:
    value: str


@dataclass(frozen=True)
class HashId:
    algo: str  # e.g., "opaque", "sha256", "blake3", "simhash64"
    value: str  # canonicalized string for that algo

    def __str__(self) -> str:
        return f"{self.algo}:{self.value}"


@dataclass(frozen=True)
class TopicId:
    """
    Deterministic cluster identifier derived from content identifiers/fingerprints.
    Store as 'algo:value' (same canonicalization discipline as HashId).
    """

    algo: str  # e.g., "simhash64-lsh", "minhash-lsh", "sha256", "opaque-topic", "x-<vendor>"
    value: str  # canonical cluster key for that algo (hex or base64url per algo spec)

    def __str__(self) -> str:
        return f"{self.algo}:{self.value}"


@dataclass(frozen=True)
class WorldId:
    value: str
