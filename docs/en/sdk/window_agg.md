# Window Aggregation

The `WindowAgg` type represents a time window of aggregated activity data. This is the primary data structure for temporal analysis of content patterns.

## Overview

A window aggregation captures all relevant metrics for a specific time period, typically 10-15 minutes. It includes activity counts, content clustering data, temporal patterns, and content fingerprints.

## Type Definition

```python
@dataclass
class WindowAgg:
    world_id: str
    topic_id: str
    window_start: datetime
    window_end: datetime
    n_messages: int
    n_unique_hashes: int
    dup_rate: float
    top_hashes: list[TopHash]
    hash_concentration: float
    burst_score: float
    type_mix: dict[str, float]
    time_histogram: list[int]
    digests: Optional[Digests] = None
```

## Fields

### Identifiers
- **world_id**: Identifier for the simulation world (e.g., "A", "B")
- **topic_id**: Topic cluster identifier for content grouping

### Temporal
- **window_start**: Start timestamp of the aggregation window
- **window_end**: End timestamp of the aggregation window

### Activity Metrics
- **n_messages**: Total number of messages in the window
- **n_unique_hashes**: Number of distinct content hashes
- **dup_rate**: Duplication rate (1.0 - unique_rate), range [0.0, 1.0]

### Content Clustering
- **top_hashes**: list of most frequent content clusters with counts
- **hash_concentration**: Herfindahl index measuring content concentration

### Temporal Patterns
- **burst_score**: Coefficient of variation for minute-level activity
- **time_histogram**: Message counts for each minute in the window

### Content Analysis
- **type_mix**: Proportions of content types (post/reply/retweet)
- **digests**: Optional content fingerprints (SimHash, MinHash)

## Usage Examples

### Creating a WindowAgg

```python
from datetime import datetime, timedelta
from ci.transparency.sdk import WindowAgg, TopHash, ContentHash, HashId

start = datetime(2025, 9, 10, 14, 0, 0)
end = start + timedelta(minutes=10)

window = WindowAgg(
    world_id="A",
    topic_id="baseline",
    window_start=start,
    window_end=end,
    n_messages=214,
    n_unique_hashes=183,
    dup_rate=1 - 183 / 214,
    top_hashes=[
        TopHash(ContentHash(HashId("opaque", "h1")), count=8),
        TopHash(ContentHash(HashId("opaque", "h2")), count=6),
    ],
    hash_concentration=0.15,
    burst_score=0.8,
    type_mix={"post": 0.51, "reply": 0.32, "retweet": 0.17},
    time_histogram=[12, 9, 7, 5, 3, 2, 1, 0, 0, 0],
)
```

### Serialization

```python
from ci.transparency.sdk import windowagg_to_json, windowagg_from_json

# Convert to JSON-serializable dict
json_data = windowagg_to_json(window)

# Convert back to WindowAgg
restored = windowagg_from_json(json_data)
```

### Metrics Calculation

```python
from ci.transparency.sim.metrics import herfindahl, cv_of_bins

# Calculate hash concentration
hhi = herfindahl([hash.count for hash in window.top_hashes])

# Calculate burst score from time series
burst = cv_of_bins(window.time_histogram)
```

## Design Considerations

### Immutability
WindowAgg instances are immutable to ensure consistency across analysis pipelines. Create new instances for modifications.

### Time Resolution
Windows typically span 10-15 minutes with minute-level granularity in the time histogram. This balance captures burst patterns without excessive noise.

### Content Representation
Content is represented through hashes rather than actual text to maintain privacy and enable cross-platform analysis.

### Optional Fields
The `digests` field is optional to support scenarios where content fingerprinting is not needed or available.

## Related Types

- [TopHash](hash_core.md#tophash) – Individual content cluster data
- [ContentHash](hash_core.md#contenthash) – Content identification
- [Digests](digests.md) – Content fingerprinting data


## Database Storage

WindowAgg data maps to the `events` table in DuckDB:
- JSON serialization for complex fields (top_hashes, time_histogram)
- Proper timestamp handling for temporal fields
- Separate columns for scalar metrics

See [Schema Reference](../schema.md) for complete database mapping details.
