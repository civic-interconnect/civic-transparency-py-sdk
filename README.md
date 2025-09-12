# Civic Transparency Software Development Kit (SDK)

[![Docs](https://img.shields.io/badge/docs-mkdocs--material-blue)](https://civic-interconnect.github.io/civic-transparency-sdk/)
[![PyPI](https://img.shields.io/pypi/v/civic-transparency-sdk.svg)](https://pypi.org/project/civic-transparency-sdk/)
[![Python versions](https://img.shields.io/pypi/pyversions/civic-transparency-sdk.svg)](https://pypi.org/project/civic-transparency-sdk/)
[![CI Status](https://github.com/civic-interconnect/civic-transparency-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/civic-interconnect/civic-transparency-sdk/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

A software development kit for civic transparency applications.

## Installation

```pwsh
pip install civic-transparency-sdk
```

## What This Package Provides

**Core Data Types**: Standardized structures for transparency APIs including WindowAgg aggregations, ContentHash identifiers, and content fingerprinting that enable consistent data exchange.

**Implementation Support**: Essential utilities for platforms implementing transparency APIs, including JSON serialization, database schemas, and validation helpers.

**Research Tools**: Synthetic data generation capabilities for testing transparency implementations and conducting research without exposing real user data.

**Database Integration**: Ready-to-use schemas and conversion utilities for storing transparency data in SQL databases with proper indexing and query patterns.

## Quick Start

Generate synthetic data:

```pwsh
ct-sdk generate --world A --topic-id aa55ee77 --out world_A.jsonl

ct-sdk convert --jsonl world_A.jsonl --duck world_A.duckdb --schema schema/schema.sql
```

## Use Generated Data

The generated DuckDB files are ready for analysis with any SQL-compatible tools or custom analysis scripts.

## Reproducibility

All generation is deterministic and includes:
- **Seed-based randomization**: Reproduce exact datasets
- **Version tracking**: Metadata includes package versions
- **Parameter logging**: All generation settings preserved
- **Schema versioning**: Database structures documented

**Example Seeds:**
- World A (baseline): `4242`

## Use Cases

- **Platform Implementation**: Implement transparency APIs with standardized data structures and serialization utilities.

- **Academic Research**: Generate controlled datasets for studying information dynamics with known parameters.

- **Education**: Provide realistic data for analysis exercises and transparency system understanding.

- **Testing & Validation**: Create test datasets for transparency system development without requiring real user data.

- **Algorithm Development**: Build transparency tools using standard data formats and proven utilities.

## Package Structure

```
ci.transparency.sdk/
├── cli/            # Command-line interfaces
├── digests.py      # Content fingerprinting (SimHash64, MinHashSig, Digests)
├── hash_core.py    # Content identification (HashId, ContentHash, TopHash)
├── ids.py          # ID management (WorldId, TopicId, HashId)
├── io_schema.py    # Serialization utilities (JSON conversion, dumps, loads)
└── window_agg.py   # Window aggregation data structure (WindowAgg)
```

## Security Model

This package provides foundational building blocks for transparency applications.
It does not include:
- Detection algorithms or thresholds
- Verification workflows or assessment criteria  
- Specific patterns that trigger alerts

Detection logic and verification tools are maintained separately to prevent adversarial use while enabling legitimate transparency system development.

## Documentation

Comprehensive docs are published with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/):

- **[Home](https://civic-interconnect.github.io/civic-transparency-sdk/)** – project overview and installation instructions  
- **[Usage Guide](https://civic-interconnect.github.io/civic-transparency-sdk/usage/)** – quick-start workflow and common tasks  
- **[CLI Reference](https://civic-interconnect.github.io/civic-transparency-sdk/cli/)** – full command-line interface details  
- **[SDK Reference](https://civic-interconnect.github.io/civic-transparency-sdk/sdk/overview/)** – core Python APIs  
  - [Window Aggregation](https://civic-interconnect.github.io/civic-transparency-sdk/sdk/window_agg/)  
  - [Content Hashing](https://civic-interconnect.github.io/civic-transparency-sdk/sdk/hash_core/)  
  - [Content Digests](https://civic-interconnect.github.io/civic-transparency-sdk/sdk/digests/)  
  - [ID Management](https://civic-interconnect.github.io/civic-transparency-sdk/sdk/ids/)  
  - [I/O Schema](https://civic-interconnect.github.io/civic-transparency-sdk/sdk/io_schema/)  
- **[Schema Reference](https://civic-interconnect.github.io/civic-transparency-sdk/schema/)** – database schema and integration notes  
- **Related Projects**  
  - [Civic Transparency Spec](https://civic-interconnect.github.io/civic-transparency-spec/)  
  - [Civic Transparency Types](https://civic-interconnect.github.io/civic-transparency-types/)


## License

See LICENSE file for details.