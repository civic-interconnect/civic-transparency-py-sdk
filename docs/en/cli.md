# CLI Reference

The `ct-sdk` command-line interface provides simple workflows for data generation and conversion.

## Installation

After installing the package, the CLI is available as `ct-sdk`:

```bash
pip install civic-transparency-sdk
ct-sdk --help
```

## Commands

### generate

Generate synthetic transparency data.

```bash
ct-sdk generate [OPTIONS]
```

**Required Arguments:**
- `--world TEXT`: World identifier (e.g., "A", "B", "baseline")
- `--topic-id TEXT`: Topic identifier for content clustering
- `--out TEXT`: Output JSONL file path

**Optional Arguments:**
- `--windows INTEGER`: Number of time windows [default: 12]
- `--step-minutes INTEGER`: Minutes per window [default: 10]
- `--seed INTEGER`: Random seed for reproducibility [default: 4242]

**Influence Parameters** (optional):
- `--dup-mult FLOAT`: Duplicate multiplier for amplified content sharing
- `--burst-minutes INTEGER`: Micro-burst duration for coordinated activity
- `--reply-nudge FLOAT`: Reply proportion adjustment (+/- shift)

**Examples:**

Baseline organic generation:
```bash
ct-sdk generate --world A --topic-id baseline --out world_A.jsonl
```

Influenced generation:
```bash
ct-sdk generate --world B --topic-id influenced --out world_B.jsonl \
  --seed 4343 --dup-mult 1.35 --burst-minutes 3 --reply-nudge -0.10
```

**Behavior:**
When any influence parameters are provided, the system automatically switches to influenced generation mode. Without influence parameters, it generates baseline organic patterns.

### convert

Convert JSONL data to DuckDB format for analysis.

```bash
ct-sdk convert [OPTIONS]
```

**Required Arguments:**
- `--jsonl TEXT`: Input JSONL file path
- `--duck TEXT`: Output DuckDB file path
- `--schema TEXT`: Schema SQL file path

**Example:**
```bash
ct-sdk convert --jsonl world_A.jsonl --duck world_A.duckdb --schema schema/schema.sql
```

**Behavior:**
- Creates the database file if it doesn't exist
- Creates the events table using the provided schema
- Clears existing data and loads new records
- Reports the number of rows loaded

## Advanced Usage

### Direct Script Access

For advanced users who need more control, the underlying scripts can be called directly:

```bash
# Direct generation with all parameters
python -m scripts_py.gen_empty_world --world A --topic-id baseline --out world_A.jsonl

# Influenced generation with full parameter control
python -m scripts_py.gen_world_b_light --topic-id influenced --out world_B.jsonl \
  --windows 12 --step-minutes 10 --seed 4343 --dup-mult 1.35 --burst-minutes 3 --reply-nudge -0.10

# Database conversion with mode options
python -m scripts_py.jsonl_to_duckdb --jsonl world_A.jsonl --duck world_A.duckdb --schema schema/schema.sql

# Analysis and plotting
python -m scripts_py.plot_quick --duck world_A.duckdb --outdir plots/world_A
python -m scripts_py.plot_compare_ducks --ducks world_A.duckdb world_B.duckdb --outdir plots/compare_AB
```

### Typical Workflow

1. **Generate baseline data**:
   ```bash
   ct-sdk generate --world A --topic-id baseline --out world_A.jsonl
   ```

2. **Generate comparison data**:
   ```bash
   ct-sdk generate --world B --topic-id influenced --out world_B.jsonl --dup-mult 1.35
   ```

3. **Convert to databases**:
   ```bash
   ct-sdk convert --jsonl world_A.jsonl --duck world_A.duckdb --schema schema/schema.sql
   ct-sdk convert --jsonl world_B.jsonl --duck world_B.duckdb --schema schema/schema.sql
   ```

4. **Analyze with external tools** or direct script access for plotting.

## Error Handling

The CLI provides clear error messages for common issues:
- Missing required arguments
- File not found errors
- Invalid parameter values
- Schema application failures

All errors include context and suggested fixes where possible.
