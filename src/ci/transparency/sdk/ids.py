"""Identifiers for events, content hashes, estimated topics, and worlds.

sdk/ids.py
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class EventId:
    """Represents a unique identifier for an event.

    Attributes:
        value (str): The string value of the event identifier.
    """

    value: str


@dataclass(frozen=True)
class HashId:
    """Represents a hash identifier consisting of an algorithm and its corresponding value.

    Attributes:
        algo (str): The name of the hashing algorithm (e.g., "opaque", "sha256", "blake3", "simhash64").
        value (str): The canonicalized string value produced by the specified algorithm.

    Methods:
        __str__(): Returns a string representation of the HashId in the format "<algo>:<value>".
    """

    algo: str  # e.g., "opaque", "sha256", "blake3", "simhash64"
    value: str  # canonicalized string for that algo

    def __str__(self) -> str:
        """Return a string representation of the object in the format '<algo>:<value>'.

        Returns:
            str: The string representation of the object.
        """
        return f"{self.algo}:{self.value}"


@dataclass(frozen=True)
class TopicId:
    """Deterministic cluster identifier derived from content identifiers/fingerprints.

    Store as 'algo:value' (same canonicalization discipline as HashId).
    """

    algo: str  # e.g., "simhash64-lsh", "minhash-lsh", "sha256", "opaque-topic", "x-<vendor>"
    value: str  # canonical cluster key for that algo (hex or base64url per algo spec)

    def __str__(self) -> str:
        """Return a string representation of the object in the format '<algo>:<value>'.

        Returns:
            str: The algorithm and value separated by a colon.
        """
        return f"{self.algo}:{self.value}"


@dataclass(frozen=True)
class WorldId:
    """Represents a unique identifier for a world entity.

    Attributes:
        value (str): The string value of the world identifier.
    """

    value: str
