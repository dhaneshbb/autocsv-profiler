# Configuration

## Table of Contents
- [Environment Variables](#environment-variables)
- [Configuration Format](#configuration-format)
- [Programmatic Configuration](#programmatic-configuration)
- [Default Configuration](#default-configuration)
- [Configuration Examples](#configuration-examples)
- [Configuration Precedence](#configuration-precedence)
- [Validation Rules](#validation-rules)
- [See Also](#see-also)

## Environment Variables

Configure AutoCSV Profiler behavior using environment variables with the `AUTOCSV_` prefix.

### Performance Settings

#### Memory Limit
```bash
export AUTOCSV_PERFORMANCE_MEMORY_LIMIT_GB=2
```
- Default: `1`
- Sets memory limit in GB for analysis processing

#### Chunk Size
```bash
export AUTOCSV_PERFORMANCE_CHUNK_SIZE=20000
```
- Default: `10000`
- Number of rows to process in each chunk for large files

### Logging Configuration

#### Log Level
```bash
export AUTOCSV_LOGGING_LEVEL=DEBUG
```
- Default: `INFO`
- Valid values: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

#### Console Logging
```bash
export AUTOCSV_LOGGING_CONSOLE_ENABLED=true
export AUTOCSV_LOGGING_CONSOLE_LEVEL=INFO
```

#### File Logging
```bash
export AUTOCSV_LOGGING_FILE_ENABLED=true
export AUTOCSV_LOGGING_FILE_FILENAME=custom_log.log
export AUTOCSV_LOGGING_FILE_LEVEL=DEBUG
```

### Analysis Settings

#### Delimiter Detection
```bash
export AUTOCSV_DELIMITER_DETECTION_CONFIDENCE_THRESHOLD=0.8
```
- Default: `0.6`
- Confidence threshold for automatic delimiter detection

#### Cardinality Analysis
```bash
export AUTOCSV_ANALYSIS_HIGH_CARDINALITY_THRESHOLD=50
```
- Default: `50`
- Threshold for identifying high-cardinality categorical columns

## Configuration Format

Environment variables follow the pattern:
```
AUTOCSV_<SECTION>_<SUBSECTION>_<KEY>
```

Examples:
- `AUTOCSV_PERFORMANCE_MEMORY_LIMIT_GB`
- `AUTOCSV_LOGGING_CONSOLE_LEVEL`
- `AUTOCSV_ANALYSIS_HIGH_CARDINALITY_THRESHOLD`

## Programmatic Configuration

For the complete configuration loading process, see the [Configuration Flow diagram](diagrams.md#configuration-flow).

### Settings Access

```python
from autocsv_profiler import settings

# Get memory limit
memory_limit = settings.get('performance', 'memory_limit_gb')

# Get logging configuration
log_level = settings.get('logging', 'level')
console_enabled = settings.get('logging', 'console', 'enabled')
```

### Configuration Validation

Settings are automatically validated:
- Memory limit must be positive
- Chunk size must be greater than 0
- Log levels must be valid Python logging levels
- Confidence thresholds must be between 0.0 and 1.0

### Reset Settings (Testing)

```python
from autocsv_profiler import Settings

# Reset to defaults (useful for testing)
Settings.reset_instance()
```

## Default Configuration

```yaml
project:
  name: "AutoCSV Profiler"
  version: "2.0.0"
  description: "CSV data analysis toolkit with statistical profiling and visualization"

performance:
  chunk_size: 10000
  memory_limit_gb: 1

logging:
  level: "INFO"
  console:
    enabled: true
    level: "INFO"
    format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file:
    enabled: true
    level: "DEBUG"
    filename: "autocsv_profiler.log"
    max_bytes: 10485760  # 10MB
    backup_count: 5
    format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  app:
    structured_debug: false

delimiter_detection:
  confidence_threshold: 0.6

analysis:
  high_cardinality_threshold: 50
```

## Configuration Examples

### High-Performance Setup
```bash
export AUTOCSV_PERFORMANCE_MEMORY_LIMIT_GB=4
export AUTOCSV_PERFORMANCE_CHUNK_SIZE=50000
export AUTOCSV_LOGGING_LEVEL=WARNING
```

### Debug Configuration
```bash
export AUTOCSV_LOGGING_LEVEL=DEBUG
export AUTOCSV_LOGGING_APP_STRUCTURED_DEBUG=true
export AUTOCSV_LOGGING_CONSOLE_LEVEL=DEBUG
```

### Batch Processing Setup
```bash
export AUTOCSV_LOGGING_CONSOLE_ENABLED=false
export AUTOCSV_LOGGING_FILE_ENABLED=true
export AUTOCSV_PERFORMANCE_MEMORY_LIMIT_GB=8
```

### Custom Delimiter Detection
```bash
export AUTOCSV_DELIMITER_DETECTION_CONFIDENCE_THRESHOLD=0.9
```

## Configuration Precedence

1. Environment variables (highest priority)
2. Default configuration values

The [Configuration Flow diagram](diagrams.md#configuration-flow) visualizes how configuration precedence works with environment variables overriding defaults.

Environment variables override default settings when present.

## Validation Rules

- `memory_limit_gb`: Must be > 0
- `chunk_size`: Must be > 0
- `confidence_threshold`: Must be between 0.0 and 1.0
- `high_cardinality_threshold`: Must be >= 0
- `log_level`: Must be valid Python logging level

Invalid configuration values raise `ConfigValidationError`.

## See Also

- [Documentation Index](index.md) - Complete documentation overview
- [User Guide](user-guide.md) - Command-line interface options and examples
- [API Reference](api-reference.md) - Python API configuration
- [Developer Guide](developer-guide.md) - Development configuration
- [Troubleshooting](troubleshooting.md) - Problem-solving guide
- [Architecture Diagrams](diagrams.md) - Visual system architecture

---

Version: 2.0.0 | Status: Beta | Python: 3.8-3.13

Copyright 2025 dhaneshbb | License: MIT | Homepage: https://github.com/dhaneshbb/autocsv-profiler
