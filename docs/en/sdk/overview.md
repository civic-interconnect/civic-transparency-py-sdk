# Type Reference Overview

The civic transparency simulation core provides a structured type system for representing temporal activity patterns, content fingerprints, and aggregated metrics. This type system enables reproducible research and standardized analysis across different transparency studies.

## Core Concepts

### Window Aggregation
The fundamental unit of analysis is a time window containing aggregated activity data. Each window represents a slice of time (typically 10-15 minutes) with calculated metrics and content fingerprints.

### Content Clustering
Content is identified through hash-based clustering. Similar content gets grouped under topic identifiers, enabling analysis of how specific topics or themes spread through systems.

### Fingerprinting
Content fingerprints use multiple techniques:
- **SimHash**: Locality-sensitive hashing for near-duplicate detection
- **MinHash**: Set similarity estimation for clustering analysis

### Temporal Patterns
Activity patterns are captured through:
- Time-series data within windows
- Cross-window trend analysis
- Burst detection and anomaly scoring

## Type Categories

### Core Types
Essential data structures for window-based analysis:

- **WindowAgg**: Complete window aggregation with all metrics
- **ContentHash**: Hash-based content identification
- **Digests**: Content fingerprinting data structures

### Configuration Types
Control structures for generation and analysis:

- **EventConfig**: Configuration for temporal events and scenarios

### Utility Types
Supporting structures for data handling:

- **ID Management**: Consistent identifier schemes
- **I/O Schema**: Serialization and database integration
- **Registry**: Type registration and discovery

## Design Principles

**Immutability**: Core data structures are immutable to ensure consistency across analysis pipelines.

**Composability**: Types can be combined and extended for different research scenarios.

**Serialization**: All types support JSON serialization for cross-platform compatibility.

**Validation**: Built-in validation ensures data integrity throughout the analysis pipeline.

**Documentation**: Comprehensive docstrings and type hints support IDE integration and static analysis.

## Import Patterns

```python
# Core analysis types
from ci.transparency.sdk import WindowAgg, ContentHash, TopHash

# Content fingerprinting
from ci.transparency.sdk import Digests, SimHash64, MinHashSig

# I/O and serialization
from ci.transparency.sdk import windowagg_to_json, windowagg_from_json

# Utility functions
from ci.transparency.sim.metrics import herfindahl, cv_of_bins
```

## Next Steps

- [Window Aggregation](window_agg.md) - Core analysis data structure
- [Content Hashing](hash_core.md) - Content identification and clustering
- [I/O Schema](io_schema.md) - Serialization and database integration
