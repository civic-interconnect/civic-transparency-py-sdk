# Schema Reference

This document describes the database schema used for storing transparency simulation data in DuckDB.

## Privacy

This schema stores only `aggregated metrics` and `hash-based identifiers`.
Hashes are one-way digests and cannot be reversed to original content.
No raw user data or message text is recorded.

## Events Table

The primary table `events` stores window-level aggregations of activity data.

### Schema Definition

```sql
CREATE TABLE events (
    world_id TEXT,
    topic_id TEXT,
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    n_messages INTEGER,
    n_unique_hashes INTEGER,
    dup_rate REAL,
    top_hashes TEXT,  -- JSON array
    hash_concentration REAL,
    burst_score REAL,
    type_post REAL,
    type_reply REAL,
    type_retweet REAL,
    time_histogram TEXT  -- JSON array
);
```

### Column Descriptions

**Identifiers:**
- `world_id`: World identifier (e.g., "A", "B")
- `topic_id`: Topic/content cluster identifier

**Temporal:**
- `window_start`: Window start timestamp (ISO format)
- `window_end`: Window end timestamp (ISO format)

**Activity Metrics:**
- `n_messages`: Total messages in window
- `n_unique_hashes`: Number of unique content hashes
- `dup_rate`: Duplication rate (0.0 to 1.0)

**Content Analysis:**
- `top_hashes`: JSON array of top content clusters with counts
- `hash_concentration`: Herfindahl index of hash distribution

**Temporal Patterns:**
- `burst_score`: Coefficient of variation for minute-level activity
- `time_histogram`: JSON array of message counts per minute

**Content Types:**
- `type_post`: Proportion of original posts (0.0 to 1.0)
- `type_reply`: Proportion of replies (0.0 to 1.0)
- `type_retweet`: Proportion of retweets/shares (0.0 to 1.0)

### JSON Column Formats

**top_hashes** contains an array of objects:
```json
[
  {
    "hash": {
      "id": {
        "algo": "opaque",
        "value": "h1"
      }
    },
    "count": 8
  }
]
```

**time_histogram** contains minute-level counts:
```json
[12, 9, 7, 5, 3, 2, 1, 0, 0, 0]
```

## Schema Variants

### Student Schema (`schema.sql`)
Basic schema for educational use with essential columns and clear documentation.

## Loading Data

Data is loaded via the conversion utility:

```bash
ct-sdk convert --jsonl data.jsonl --duck data.duckdb --schema schema/schema.sql
```

The loader:
1. Creates the table if it doesn't exist
2. Clears existing data
3. Inserts new records with proper type conversion
4. Validates JSON column formats

## Query Examples

**Basic aggregations:**
```sql
SELECT
    world_id,
    AVG(dup_rate) as avg_dup_rate,
    AVG(hash_concentration) as avg_concentration,
    AVG(burst_score) as avg_burst_score
FROM events
GROUP BY world_id;
```

**Time series analysis:**
```sql
SELECT
    window_start,
    n_messages,
    dup_rate,
    burst_score
FROM events
WHERE world_id = 'A'
ORDER BY window_start;
```

**Content type analysis:**
```sql
SELECT
    world_id,
    AVG(type_post) as avg_post_share,
    AVG(type_reply) as avg_reply_share,
    AVG(type_retweet) as avg_retweet_share
FROM events
GROUP BY world_id;
```

**JSON data extraction:**
```sql
-- Extract top hash information (DuckDB JSON functions)
SELECT
    world_id,
    topic_id,
    json_extract_string(top_hashes, '$[0].hash.id.value') as top_hash_id,
    json_extract(top_hashes, '$[0].count') as top_hash_count
FROM events;
```

## Data Types and Constraints

**Timestamps**: Stored as TIMESTAMP, typically UTC
**Rates**: REAL values between 0.0 and 1.0
**Counts**: Non-negative INTEGER values
**JSON**: Valid JSON strings for complex data
**Identifiers**: TEXT with application-specific formats

## Performance Considerations

**Indexing**: Consider indexes on `world_id`, `topic_id`, and `window_start` for common queries.

**JSON Processing**: DuckDB provides efficient JSON functions for extracting specific fields from JSON columns.

**Time Series**: Window-based partitioning can improve performance for time series queries.

**Aggregations**: Pre-computed aggregations are stored at the window level to optimize analysis queries.
