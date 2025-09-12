# Civic Transparency Simulation Core

A foundational toolkit for generating synthetic transparency data and calculating metrics for research and education.

## Overview

This package provides the essential building blocks for transparency research without revealing detection methods or assessment criteria. It enables researchers to generate controlled datasets, calculate standard metrics, and build reproducible analysis pipelines.

## Key Features

**Standardized Data Types**: Core structures for temporal events, content fingerprints, and aggregated metrics that enable reproducible transparency research across different research groups.

**Synthetic Data Generation**: Create realistic datasets with organic activity patterns, content clustering, and temporal dynamics. Generate both baseline and influenced scenarios for A/B comparisons.

**Standard Metrics**: Calculate transparency metrics including duplicate rates, hash concentration (Herfindahl index), burst detection, and content type distributions.

**Database Integration**: Export data to JSONL format and load into DuckDB for SQL-based analysis and visualization.

**Cross-Platform CLI**: Simple command-line interface for data generation and conversion workflows.

## Quick Start

Install the package:

```bash
pip install civic-transparency-sim
```

Generate synthetic data:

```bash
ct-sdk generate --world A --topic-id baseline --out world_A.jsonl
ct-sdk convert --jsonl world_A.jsonl --duck world_A.duckdb --schema schema/schema.sql
```

## Use Cases

- **Academic Research**: Generate controlled datasets for studying information dynamics
- **Education**: Provide realistic data for analysis exercises and metric calculation practice  
- **Algorithm Development**: Create test datasets with known ground truth for developing transparency tools
- **Benchmarking**: Standard metrics and data formats enable comparison across research groups

## Security Model

This package provides building blocks for transparency research without revealing:
- Detection algorithms or thresholds
- Verification workflows or assessment criteria
- Specific patterns that trigger alerts

Detection logic and verification tools are maintained separately to prevent adversarial use while enabling legitimate research.

## Related Projects

- [Civic Transparency Spec](https://civic-interconnect.github.io/civic-transparency-spec/) - API specifications and standards
- [Civic Transparency Types](https://civic-interconnect.github.io/civic-transparency-types/) - Core type definitions and schemas
