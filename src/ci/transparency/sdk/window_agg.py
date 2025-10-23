"""Core data structures for windowed aggregation of content hashes."""
# sdk/window_agg.py

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime

from .digests import Digests
from .hash_core import ContentHash


@dataclass(frozen=True)
class TopHash:
    """Represents a top content hash and its occurrence count within a window.

    Attributes
    ----------
    hash : ContentHash
        The content hash value.
    count : int
        The number of times this hash appears.
    """

    hash: ContentHash
    count: int


@dataclass(frozen=True)
class WindowAgg:
    """Aggregated statistics and metadata for a window of content hashes.

    Attributes
    ----------
    world_id : str
        Identifier for the world/context.
    topic_id : str
        Identifier for the topic.
    window_start : datetime
        Start time of the aggregation window.
    window_end : datetime
        End time of the aggregation window.
    n_messages : int
        Number of messages in the window.
    n_unique_hashes : int
        Number of unique content hashes.
    dup_rate : float
        Duplicate rate of content hashes.
    top_hashes : Sequence[TopHash]
        List of top content hashes and their counts.
    hash_concentration : float
        Concentration metric of hashes.
    burst_score : float
        Burstiness score for the window.
    type_mix : Mapping[str, float]
        Distribution of message types (e.g., post, reply, retweet).
    time_histogram : Sequence[int]
        Histogram of message counts over time bins.
    digests : Digests | None
        Optional digests for the window.
    """

    # minimal API-shaped record (students/consumers see this)
    world_id: str
    topic_id: str
    window_start: datetime
    window_end: datetime
    n_messages: int
    n_unique_hashes: int
    dup_rate: float
    top_hashes: Sequence[TopHash]
    hash_concentration: float
    burst_score: float
    type_mix: Mapping[str, float]  # {"post":.5,"reply":.3,"retweet":.2}
    time_histogram: Sequence[int]
    digests: Digests | None = None
