# ID Management

ID management types provide consistent identifier schemes across the transparency simulation system.

## Overview

The ID management module defines standardized approaches for creating, validating, and using identifiers throughout the system. This ensures consistency and enables cross-referencing between different components.

## Core Types

### HashId

Basic hash identifier with type information.

```python
@dataclass
class HashId:
    type: str
    value: str
```

**Fields:**
- **type**: Hash algorithm or identifier type
- **value**: The actual identifier string

**Common Types:**
- `"opaque"`: Synthetic identifiers for testing
- `"sha256"`: SHA-256 cryptographic hashes
- `"md5"`: MD5 hashes (legacy support)
- `"simhash"`: SimHash signatures
- `"uuid"`: UUID identifiers

### WorldId

Identifier for simulation worlds.

```python
@dataclass
class WorldId:
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("World ID cannot be empty")
```

### TopicId

Identifier for **content clusters** without seeing content. A `TopicId` is a deterministic key derived from
content identifiers/fingerprints (e.g., SimHash/MinHash via LSH).

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class TopicId:
    algo: str   # e.g., "simhash64-lsh", "minhash-lsh", "sha256", "opaque-topic"
    value: str  # canonical cluster key for that algo

    def __str__(self) -> str:
        return f"{self.algo}:{self.value}"
```

Examples (strings stored in DB):

- simhash64-lsh:9f3a5c10aa55ee77
- minhash-lsh:AbC1_2xY... (base64url if not hex)
- opaque-topic:t_001

Note: TopicId is not a human-readable label.
TopicId is a stable, privacy-preserving cluster key.

## Usage Examples

### Basic Identifiers
```python
from ci.transparency.sdk import HashId, WorldId, TopicId

# Hash identifiers
content_hash = HashId("sha256", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
opaque_hash = HashId("opaque", "test_content_123")

# World and topic identifiers
world = WorldId("experiment_A")
topic = TopicId("simhash64-lsh")
```

### Identifier Validation
```python
def validate_hash_id(hash_id: HashId) -> bool:
    """Validate hash ID format."""
    if hash_id.type == "sha256":
        return len(hash_id.value) == 64 and all(c in "0123456789abcdef" for c in hash_id.value.lower())
    elif hash_id.type == "md5":
        return len(hash_id.value) == 32 and all(c in "0123456789abcdef" for c in hash_id.value.lower())
    elif hash_id.type == "opaque":
        return bool(hash_id.value)  # Any non-empty string
    return False
```

### Identifier Generation
```python
import hashlib
import uuid

def generate_content_hash(content: str) -> HashId:
    """Generate SHA-256 hash for content."""
    hash_value = hashlib.sha256(content.encode()).hexdigest()
    return HashId("sha256", hash_value)

def generate_world_id() -> WorldId:
    """Generate unique world identifier."""
    return WorldId(f"world_{uuid.uuid4().hex[:8]}")
```

## Identifier Patterns

### Hierarchical Naming
```python
# Use hierarchical patterns for organization
experiment_world = WorldId("exp2025_baseline_A")
topic_cluster = TopicId("election2024_policy_discussion")
```

### Timestamped Identifiers
```python
from datetime import datetime

def timestamped_world_id(prefix: str) -> WorldId:
    """Create timestamped world identifier."""
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    return WorldId(f"{prefix}_{timestamp}")
```

### Content-Based Identifiers
```python
def content_topic_id(content_sample: str) -> TopicId:
    """Generate topic ID based on content characteristics."""
    # Simplified example - in practice would use NLP
    keywords = content_sample.lower().split()[:3]
    return TopicId("_".join(keywords))
```

## Serialization

Identifiers serialize to simple string values or structured objects:

```json
{
  "hash_id": {
    "algo": "sha256",
    "value": "e3b0c44298fc..."
  },
  "world_id": "experiment_A",
  "topic_id": "9f3a5c10aa55ee77"
}
```

## Validation Utilities

### Format Checking
```python
class IdValidator:
    @staticmethod
    def is_valid_world_id(world_id: str) -> bool:
        """Check if world ID format is valid."""
        return bool(world_id and len(world_id) <= 64 and world_id.replace("_", "").replace("-", "").isalnum())

    @staticmethod
    def is_valid_topic_id(topic_id: str) -> bool:
        """Check if topic ID format is valid."""
        return bool(topic_id and len(topic_id) <= 128)
```

### Uniqueness Checking
```python
class IdRegistry:
    def __init__(self):
        self.used_world_ids = set()
        self.used_topic_ids = set()

    def register_world_id(self, world_id: WorldId) -> bool:
        """Register world ID and check uniqueness."""
        if world_id.value in self.used_world_ids:
            return False
        self.used_world_ids.add(world_id.value)
        return True
```

## Best Practices

### Naming Conventions
- Use descriptive prefixes for different identifier types
- Include version numbers for evolving experiments
- Use consistent separators (underscores recommended)
- Avoid spaces and special characters

### Collision Avoidance
- Include timestamps for time-sensitive identifiers
- Use random components for high-uniqueness requirements
- Validate uniqueness before using identifiers
- Maintain registries for active identifier spaces

### Documentation
- Document identifier schemes in experiment metadata
- Include identifier generation rules in configuration
- Provide examples of valid identifiers
- Explain identifier meaning and scope

## Related Types

- [ContentHash](hash_core.md) - Uses HashId for content identification
- [WindowAgg](window_agg.md) - Uses world_id and topic_id fields

## Database Storage

Identifiers map to database columns:
- Simple string storage for most identifier types
- JSON storage preserves type information for HashId
- Indexes on identifier columns for efficient queries

See [Schema Reference](../schema.md) for database identifier handling.
