# Content Hashing

Content hashing types provide structures for content identification **without** requiring access to raw content.

## Overview

The hash core defines types for representing content via identifiers and fingerprints. This supports privacy-preserving analysis and interoperable APIs.

## Core Types

### HashId {#hashid}

Represents a typed, canonical content identifier.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class HashId:
    algo: str   # e.g., "sha256", "blake3", "opaque", "simhash64"
    value: str  # canonical string for that algo (e.g., lowercase hex)

```

**Fields:**
- **algo**: Hash algorithm type (e.g., "sha256", "opaque", "simhash")
- **value**: Canonicalized hash value (e.g., lowercase hex; simhash64 is 16 hex chars, no 0x).

**Usage:**
```python
from ci.transparency.sdk import HashId

# Opaque identifier (privacy-preserving)
hash_id = HashId("opaque", "h1")

# Cryptographic hash (lowercase hex)
crypto_hash = HashId("sha256", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")

# Similarity hash (64-bit, 16 hex chars)
sim64 = HashId("simhash64", "9f3a5c10aa55ee77")
```

Note: Multi-value fingerprints like MinHash are not represented as HashId.
They live in [Digests](digests.md).


### ContentHash

Wrapper for a `HashId`.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ContentHash:
    id: HashId

```

**Usage:**
```python
from ci.transparency.sdk import ContentHash, HashId

content = ContentHash(HashId("opaque", "content_123"))
```

### TopHash

Represents a content item (by `ContentHash`) with its frequency.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class TopHash:
    hash: ContentHash
    count: int

```

**Fields:**
- **hash**: Content identifier
- **count**: Frequency of this item in the dataset/window

**Usage:**
```python
from ci.transparency.sdk.types import TopHash, ContentHash, HashId

top_content = TopHash(
    hash=ContentHash(HashId("opaque", "popular_content")),
    count=42
)

```

## Design Principles

### Privacy-First
Content is represented by hashes and cluster keys, not raw text.

### Type Safety
Algorithms are explicitly labeled via `algo` to prevent mixing types.

### Frequency Tracking
`TopHash` couples a content identifier with counts for aggregation.

## Hash Types

### Opaque Hashes
Synthetic/testing identifiers (no content required):
```python
HashId("opaque", "h1")
HashId("opaque", "test_content_abc")
```

### Cryptographic Hashes
Standard one-way hashes:
```python
HashId("sha256", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
HashId("md5", "d41d8cd98f00b204e9800998ecf8427e")
```

### Similarity Hashes
Locality-sensitive single-value identifiers (64-bit SimHash):
```python
HashId("simhash", "9f3a5c10aa55ee77")
```

For MinHash (multi-value), see [Digests](digests.md).

## Usage Patterns

### Content Identification
```python
# Build a map from content id -> count
content_map = {}
for top in window.top_hashes:
    content_map[top.hash.id.value] = top.count
```

### Data Structure Creation
```python
from ci.transparency.sdk.types import TopHash, ContentHash, HashId

top_hashes = [
    TopHash(ContentHash(HashId("opaque", f"content_{i}")), count=10 - i)
    for i in range(5)
]
```

## Serialization

Content hashes serialize to nested JSON:

```json
{
  "hash": {
    "id": {
      "algo": "opaque",
      "value": "h1"
    }
  },
  "count": 8
}
```

## Related Types

- [WindowAgg](window_agg.md) - Contains lists of TopHash objects
- [Digests](digests.md) - Content fingerprinting with similarity hashes
- [I/O Schema](io_schema.md) - Serialization utilities

## Database Storage

Store `TopHash` inside JSON columns for flexibility:
- Preserves algorithm and canonical value
- Enables JSON extraction of fields for queries
- Keeps counts alongside identifiers

See [Schema Reference](../schema.md) for examples.
