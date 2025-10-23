# Civic Transparency Simulation Toolkit

A foundational toolkit for generating **synthetic transparency data** and calculating **metrics** for research, testing, and education.

---

## Overview

This package provides the essential building blocks for transparency research without revealing detection methods or assessment criteria.
It enables researchers and educators to:

- Generate controlled datasets with reproducible seeds
- Calculate standard transparency metrics
- Build reproducible analysis and teaching pipelines

---

## Key Features

- **Standardized Data Types**: Core structures for temporal events, content fingerprints, and aggregated metrics that enable reproducible research across different groups.
- **Synthetic Data Generation**: Create realistic datasets with organic activity patterns, content clustering, and temporal dynamics. Generate both baseline and influenced scenarios for A/B comparisons.
- **Standard Metrics**: Calculate metrics including duplicate rates, hash concentration (Herfindahl index), burst detection, and content type distributions.
- **Database Integration**: Export data to JSONL and load into DuckDB for SQL-based analysis and visualization.
- **Cross-Platform CLI**: Command-line interface for data generation and conversion workflows.

---

## Quick Start

Install the package:

```bash
pip install civic-transparency-sdk
```

Generate synthetic data:

```bash
# Generate baseline world
ct-sim generate --world A --topic-id baseline --out world_A.jsonl

# Convert JSONL to DuckDB
ct-sim convert --jsonl world_A.jsonl --duck world_A.duckdb --schema schema/schema.sql
```

---

## Use Cases

- **Academic Research**: Generate controlled datasets for studying information dynamics
- **Education**: Provide realistic datasets for analysis exercises and metric calculation practice
- **Algorithm Development**: Create test datasets with known ground truth for tool development
- **Benchmarking**: Use standard metrics and data formats to enable cross-group comparisons

---

## Security Model

This package provides **building blocks** for transparency research.
It does **not** include:

- Detection algorithms or thresholds
- Verification workflows or assessment criteria
- Operational rules or alerting logic

These remain separate to prevent adversarial misuse while enabling legitimate transparency research.


---

## Documentation Index

- [CLI Reference](./cli.md)
- [SDK API Reference](./sdk/overview.md)
- [Schema Reference](./schema.md)


---

## Related Projects

- Civic Transparency PTag Spec
- Civic Transparency PTag Types
- Civic Transparency Verify (research)
