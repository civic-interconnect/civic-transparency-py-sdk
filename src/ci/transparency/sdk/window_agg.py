"""
sdk/window_agg.py
Core data structures for windowed aggregation of content hashes.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Mapping, Optional, Sequence

from .digests import Digests
from .hash_core import ContentHash


@dataclass(frozen=True)
class TopHash:
    hash: ContentHash
    count: int


@dataclass(frozen=True)
class WindowAgg:
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
    digests: Optional[Digests] = None
