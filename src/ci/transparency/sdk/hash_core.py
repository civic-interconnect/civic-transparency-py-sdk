"""Core data structures for content hashes."""

from dataclasses import dataclass

from .ids import HashId


@dataclass(frozen=True)
class ContentHash:
    """Opaque identifier for a latent message family (no text)."""

    id: HashId
