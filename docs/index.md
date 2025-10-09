# AutoCSV Profiler Documentation

## Table of Contents
- [Overview](#overview)
- [Documentation Structure](#documentation-structure)
- [Quick Start](#quick-start)
- [Documentation Links](#documentation-links)

## Overview

AutoCSV Profiler is a Python toolkit for automated CSV data analysis with statistical profiling and visualization. This documentation provides complete coverage of installation, usage, API reference, configuration, and examples.

## Documentation Structure

### User Documentation
- **[User Guide](user-guide.md)** - Complete installation, CLI usage, and examples
- **[Configuration](configuration.md)** - Environment variables and settings
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions

### Developer Documentation
- **[API Reference](api-reference.md)** - Python API functions, classes, and advanced patterns
- **[Developer Guide](developer-guide.md)** - Development workflow, architecture, and testing
- **[Architecture Diagrams](diagrams.md)** - Visual system architecture and data flow diagrams

## Quick Start

### Installation
```bash
pip install autocsv-profiler
```

### Basic Usage
```bash
# Interactive mode (recommended for first-time users)
autocsv-profiler

# Direct analysis
autocsv-profiler data.csv

# Custom output directory
autocsv-profiler data.csv --output results/
```

### Python API
```python
import autocsv_profiler

# Simple analysis
result_dir = autocsv_profiler.analyze('data.csv')
print(f"Analysis saved to: {result_dir}")

# Custom configuration
result_dir = autocsv_profiler.analyze(
    csv_file_path='data.csv',
    output_dir='analysis_output/',
    memory_limit_gb=2,
    chunk_size=15000
)
```

## Documentation Links

### User Documentation
- [User Guide](user-guide.md) - Installation, CLI usage, Python API, and examples
- [Configuration](configuration.md) - Settings and environment variables
- [Troubleshooting](troubleshooting.md) - Problem-solving guide

### Developer Documentation
- [API Reference](api-reference.md) - Python API documentation and advanced patterns
- [Developer Guide](developer-guide.md) - Development workflow and architecture
- [Architecture Diagrams](diagrams.md) - Visual system architecture and data flow diagrams

### Visual Assets
- [Screenshots](png/) - CLI help, interactive mode, and output examples
- [Demos](gif/) - Animated demonstrations of key features

---

Version: 2.0.0 | Status: Beta | Python: 3.8-3.13

Copyright 2025 dhaneshbb | License: MIT | Homepage: https://github.com/dhaneshbb/autocsv-profiler
