# Civic Transparency Software Development Kit (SDK)

[![Docs](https://img.shields.io/badge/docs-mkdocs--material-blue)](https://civic-interconnect.github.io/civic-transparency-py-sdk/)
[![PyPI](https://img.shields.io/pypi/v/civic-transparency-sdk.svg)](https://pypi.org/project/civic-transparency-sdk/)
[![Python versions](https://img.shields.io/pypi/pyversions/civic-transparency-sdk.svg)](https://pypi.org/project/civic-transparency-sdk/)
[![CI Status](https://github.com/civic-interconnect/civic-transparency-py-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/civic-interconnect/civic-transparency-py-sdk/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

Synthetic data generation toolkit for civic transparency research and testing.


## Installation

```pwsh
pip install civic-transparency-sdk
```

## What This Package Provides

- **Synthetic Data Generation**: Create realistic transparency data for testing and research without requiring real user data. Generate controlled datasets with reproducible seeds for studying information dynamics.
- **Internal Data Structures**: Simulation-specific types (`WindowAgg`, `ContentHash`, `TopHash`) for generating and manipulating synthetic transparency data.
- **Database Integration**: Convert generated data to DuckDB/SQL databases for analysis with ready-to-use schemas and indexing patterns.
- **CLI Tools**: Command-line utilities for generating worlds, converting formats, and managing synthetic datasets.

> **Note**: This SDK generates synthetic data for research/testing. For implementing the PTag API specification, see **civic-transparency-ptag-types**, which provides the official API response types.


## Quick Start

Generate synthetic data:

```bash
# Activate environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Generate baseline world
ct-sdk generate --world A --topic-id aa55ee77 --out world_A.jsonl

# Convert to database
ct-sdk convert --jsonl world_A.jsonl --duck world_A.duckdb --schema schema/schema.sql
```

The generated DuckDB files are ready for analysis with any SQL-compatible tools or custom analysis scripts.
---

## Use Cases

- **Academic Research**: Generate controlled datasets with known parameters for studying information dynamics, coordination patterns, and transparency system behaviors.
- **Algorithm Development**: Build and test transparency tools using synthetic data that mimics real-world patterns without privacy concerns.
- **Testing & Validation**: Create reproducible test datasets for developing transparency systems without requiring real user data.
- **Education**: Provide realistic datasets for teaching transparency concepts, data analysis, and system design.

---

## Reproducibility

All generation is deterministic:

- **Seed-based randomization**: Same seed produces identical datasets
- **Version tracking**: Metadata includes package versions
- **Parameter logging**: All generation settings preserved in output
- **Schema versioning**: Database structures fully documented

**Example seeds:**

- World A (baseline): `4242`
- World B (influenced): `8484`

---
## Package Structure

```
ci.transparency.sdk/
├── cli/            # Command-line interface (ct-sdk)
├── digests.py      # Content fingerprinting (SimHash64, MinHashSig)
├── hash_core.py    # Content identification (HashId, ContentHash, TopHash)
├── ids.py          # ID management (WorldId, TopicId)
├── io_schema.py    # JSON serialization utilities
└── window_agg.py   # Window aggregation structure (WindowAgg)
```

---

## Related Projects

- **Civic Transparency PTag Spec** - Official API specification
- **Civic Transparency PTag Types** - Python types for PTag API responses (use this for API implementation)
- **Civic Transparency Verify** - Statistical verification tools (private)

---

## Security Model

This package provides synthetic data generation for research and testing.
It does **not** include:

- Detection algorithms or thresholds
- Verification workflows or assessment criteria
- Operational patterns or alerting rules

These are maintained separately to prevent adversarial reverse-engineering while enabling legitimate transparency research.

---

## Documentation

Full documentation at:
[civic-interconnect.github.io/civic-transparency-py-sdk/](https://civic-interconnect.github.io/civic-transparency-py-sdk/)

- **Usage Guide** - Getting started and common workflows
- **CLI Reference** - Command-line interface details
- **SDK Reference** - Core Python APIs
- **Schema Reference** - Database schemas and integration

---

### Development

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development setup and guidelines.

## Versioning

This specification follows semantic versioning.
See [CHANGELOG.md](./CHANGELOG.md) for version history.

## License

MIT © [Civic Interconnect](https://github.com/civic-interconnect)
