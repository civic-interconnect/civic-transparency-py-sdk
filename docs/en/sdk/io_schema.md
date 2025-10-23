# I/O Schema

I/O schema types handle serialization, deserialization, and data format conversion for transparency simulation data.

## Overview

The I/O schema module provides functions and utilities for converting between internal Python objects and external formats (JSON, JSONL, database records). This enables data persistence, cross-platform compatibility, and integration with analysis tools.

## Core Functions

### JSON Serialization

**windowagg_to_json()**
```python
def windowagg_to_json(window: WindowAgg) -> dict[str, Any]:
    """Convert WindowAgg to JSON-serializable dictionary."""
```

Converts a WindowAgg object to a dictionary suitable for JSON serialization. Handles:
- Datetime objects → ISO timestamp strings
- Complex nested objects → nested dictionaries
- Optional fields → null values where appropriate

**windowagg_from_json()**
```python
def windowagg_from_json(data: dict[str, Any]) -> WindowAgg:
    """Convert JSON dictionary back to WindowAgg object."""
```

Reconstructs a WindowAgg object from JSON data. Performs:
- ISO timestamp parsing → datetime objects
- Type validation and conversion
- Optional field handling
- Nested object reconstruction

### Binary Serialization

**dumps()**
```python
def dumps(obj: Any) -> bytes:
    """Serialize object to compact binary format."""
```

Serializes objects to binary format using orjson for efficiency and compactness.

**loads()**
```python
def loads(data: bytes) -> Any:
    """Deserialize binary data back to object."""
```

Deserializes binary data back to Python objects.

## Usage Examples

### Basic Serialization
```python
from ci.transparency.sdk import WindowAgg, windowagg_to_json, windowagg_from_json, dumps, loads

# Create window data
window = WindowAgg(...)

# Convert to JSON
json_data = windowagg_to_json(window)

# Serialize to binary
binary_data = dumps(json_data)

# Round-trip conversion
restored_json = loads(binary_data)
restored_window = windowagg_from_json(restored_json)

assert window == restored_window
```

### JSONL File Operations
```python
def write_windows_jsonl(windows: List[WindowAgg], filepath: str):
    """Write windows to JSONL file."""
    with open(filepath, 'wb') as f:
        for window in windows:
            json_data = windowagg_to_json(window)
            f.write(dumps(json_data))
            f.write(b'\n')

def read_windows_jsonl(filepath: str) -> List[WindowAgg]:
    """Read windows from JSONL file."""
    windows = []
    with open(filepath, 'rb') as f:
        for line in f:
            if line.strip():
                json_data = loads(line.strip())
                windows.append(windowagg_from_json(json_data))
    return windows
```

### Database Integration
```python
def window_to_db_params(window: WindowAgg) -> tuple:
    """Convert WindowAgg to database parameters."""
    json_data = windowagg_to_json(window)

    return (
        json_data['world_id'],
        json_data['topic_id'],
        datetime.fromisoformat(json_data['window_start']),
        datetime.fromisoformat(json_data['window_end']),
        json_data['n_messages'],
        json_data['n_unique_hashes'],
        json_data['dup_rate'],
        dumps(json_data['top_hashes']),  # Store as binary JSON
        json_data['hash_concentration'],
        json_data['burst_score'],
        json_data['type_mix']['post'],
        json_data['type_mix']['reply'],
        json_data['type_mix']['retweet'],
        dumps(json_data['time_histogram'])
    )
```

## JSON Schema

### WindowAgg JSON Format
```json
{
  "world_id": "A",
  "topic_id": "baseline",
  "window_start": "2025-09-10T14:00:00Z",
  "window_end": "2025-09-10T14:10:00Z",
  "n_messages": 214,
  "n_unique_hashes": 183,
  "dup_rate": 0.14485981308411214,
  "top_hashes": [
    {
      "hash": {
        "id": {
          "algo": "opaque",
          "value": "h1"
        }
      },
      "count": 8
    }
  ],
  "hash_concentration": 0.15,
  "burst_score": 0.8,
  "type_mix": {
    "post": 0.51,
    "reply": 0.32,
    "retweet": 0.17
  },
  "time_histogram": [12, 9, 7, 5, 3, 2, 1, 0, 0, 0],
  "digests": {
    "simhash64": {
      "bits": "0x9F3A5C10AA55EE77"
    },
    "minhash": {
      "k": 4,
      "sig": [1, 2, 3, 4]
    }
  }
}
```

## Error Handling

### Validation
```python
def validate_json_schema(data: dict[str, Any]) -> list[str]:
    """Validate JSON data against expected schema."""
    errors = []

    required_fields = ['world_id', 'topic_id', 'window_start', 'window_end']
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    # Type validation
    if 'dup_rate' in data and not isinstance(data['dup_rate'], (int, float)):
        errors.append("dup_rate must be numeric")

    return errors
```

### Error Recovery
```python
def safe_windowagg_from_json(data: dict[str, Any]) -> Optional[WindowAgg]:
    """Safely convert JSON to WindowAgg with error handling."""
    try:
        return windowagg_from_json(data)
    except (KeyError, ValueError, TypeError) as e:
        logger.warning(f"Failed to parse WindowAgg: {e}")
        return None
```

## Performance Considerations

### Memory Efficiency
- Use streaming for large datasets
- Process JSONL files line by line
- Avoid loading entire datasets into memory

### Speed Optimization
- orjson provides faster JSON serialization than standard library
- Binary format reduces file size and I/O time
- Batch database operations for better performance

### Compatibility
-
