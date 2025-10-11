# Content Digests

Content digests provide fingerprinting data structures for content analysis and research.

## Overview

Digest types implement content fingerprinting that can be used in transparency research. These data structures store signature information without implementing analysis algorithms.

## Core Types

### SimHash64

64-bit SimHash signature storage.

```python
@dataclass(frozen=True)
class SimHash64:
    bits: int
```

**Fields:**
- **bits**: 64-bit integer representing the SimHash signature

**Usage:**
```python
from ci.transparency.sdk import SimHash64

# Create SimHash
sim_hash = SimHash64(bits=0x9F3A5C10AA55EE77)
```

### MinHashSig

MinHash signature for set-based fingerprinting.

```python
@dataclass(frozen=True)
class MinHashSig:
    k: int
    sig: Tuple[int, ...]
```

**Fields:**
- **k**: Signature size (number of hash functions)
- **sig**: Tuple of k hash values

**Usage:**
```python
from ci.transparency.sdk import MinHashSig

# Create MinHash signature
min_hash = MinHashSig(k=4, sig=(0x1, 0x2, 0x3, 0x4))
```

### Digests

Container for multiple digest types.

```python
@dataclass(frozen=True)
class Digests:
    simhash64: Optional[SimHash64] = None
    minhash: Optional[MinHashSig] = None
```

**Usage:**
```python
from ci.transparency.sdk import Digests, SimHash64, MinHashSig

digests = Digests(
    simhash64=SimHash64(bits=0x9F3A5C10AA55EE77),
    minhash=MinHashSig(k=4, sig=(0x1, 0x2, 0x3, 0x4))
)
```

## Algorithms

### SimHash
SimHash creates fingerprints for content:

- **Storage Format**: 64-bit integer representation
- **Applications**: Content fingerprinting and data analysis

### MinHash
MinHash provides signature-based fingerprinting:

- **Signature Format**: Tuple of k integers
- **Applications**: Set-based content analysis

## Usage Patterns

### Basic Data Creation
```python
# Create content fingerprints
content_digest = Digests(
    simhash64=SimHash64(bits=computed_simhash_value),
    minhash=MinHashSig(k=128, sig=computed_minhash_signature)
)
```

### Data Access
```python
# Access digest components
if digests.simhash64:
    bits_value = digests.simhash64.bits

if digests.minhash:
    signature_size = digests.minhash.k
    signature_data = digests.minhash.sig
```

## Performance Considerations

### SimHash
- **Memory Efficient**: 64-bit storage regardless of content size
- **Simple Structure**: Direct integer storage

### MinHash
- **Configurable Size**: k parameter controls signature length
- **Tuple Storage**: Immutable sequence of integers

## Serialization

Digests serialize to structured JSON:

```json
{
  "simhash64": {
    "bits": "0x9F3A5C10AA55EE77"
  },
  "minhash": {
    "k": 4,
    "sig": [1, 2, 3, 4]
  }
}
```

## Related Types

- [WindowAgg](window_agg.md) - Contains optional digest data
- [ContentHash](hash_core.md) - Content identification
- [I/O Schema](io_schema.md) - Serialization utilities

## Database Storage

Digest data is stored as JSON in database fields:
- Compact representation preserves all signature data
- Optional fields support partial fingerprinting
- JSON format enables flexible querying

See [Schema Reference](../schema.md) for storage details.
