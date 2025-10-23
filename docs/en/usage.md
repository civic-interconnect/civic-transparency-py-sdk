# Usage Guide

This guide covers the basic workflows for generating synthetic transparency data and converting it for analysis.

---

## Installation

```bash
pip install civic-transparency-py-sdk
```

---

## Basic Workflow

### 1. Generate Synthetic Data

**Baseline (Organic) World:**
```bash
ct-sdk generate --world A --topic-id baseline --out world_A.jsonl
```

**Influenced World with Parameters:**
```bash
ct-sdk generate --world B --topic-id influenced --out world_B.jsonl \
  --seed 4343 --dup-mult 1.35 --burst-minutes 3 --reply-nudge -0.10
```

---

### 2. Convert to Database

```bash
ct-sdk convert --jsonl world_A.jsonl --duck world_A.duckdb --schema schema/schema.sql
ct-sdk convert --jsonl world_B.jsonl --duck world_B.duckdb --schema schema/schema.sql
```

---

### 3. Analyze with Direct Scripts

```bash
# Individual world analysis
python -m scripts_py.plot_quick --duck world_A.duckdb --outdir plots/world_A

# Comparative analysis
python -m scripts_py.plot_compare_ducks --ducks world_A.duckdb world_B.duckdb --outdir plots/compare_AB
```

---

## Generation Parameters

### Core Parameters

- `--world`: World identifier (e.g., "A", "B", "baseline")
- `--topic-id`: Topic identifier for content clustering
- `--out`: Output JSONL file path
- `--windows`: Number of time windows (default: 12)
- `--step-minutes`: Minutes per window (default: 10)
- `--seed`: Random seed for reproducibility (default: 4242)

### Influence Parameters

Optional parameters that modify generation behavior:

- `--dup-mult`: Duplicate multiplier (amplifies content duplication)
- `--burst-minutes`: Micro-burst duration (coordinated activity spikes)
- `--reply-nudge`: Reply proportion adjustment (positive/negative shift)

When any influence parameters are provided, the system automatically uses the influenced generation algorithm.

---

## Data Format

Generated JSONL files contain **window aggregation records** with:

- **Temporal data**: Window start/end times
- **Activity metrics**: Message counts, unique hashes, duplicate rates
- **Content fingerprints**: sdkHash and MinHash signatures
- **Clustering data**: Top hash frequencies, concentration measures
- **Behavioral patterns**: Type mix (post/reply/retweet), burst scores

---

## Database Schema

The DuckDB schema includes:

- Primary table: `events` with window-level aggregations
- Columns for all core metrics and metadata
- JSON columns for complex data (`top_hashes`, `time_histogram`)
- Proper typing for timestamps and numeric values

---

## Reproducibility

All generation is deterministic:

- **Seed-based**: Same seed produces identical output
- **Version tracking**: Metadata includes package versions
- **Parameter logging**: All settings preserved in output
- **Schema versioning**: Database structures documented

---

## Example Seeds

Standard seeds for common scenarios:

- Baseline organic: `4242`
- Light influence: `4343`
- Custom scenarios: Use any integer

---

## Programmatic Usage

```python
from ci.transparency.sdk import WindowAgg
from ci.transparency.sdk.metrics import herfindahl, cv_of_bins

# Load and analyze data programmatically
# (See Type Reference for detailed API documentation)
```
