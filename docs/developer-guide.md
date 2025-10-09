# Developer Guide

## Table of Contents
- [Setup](#setup)
- [Development Commands](#development-commands)
- [Architecture Overview](#architecture-overview)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Build and Packaging](#build-and-packaging)
- [Technical Implementation](#technical-implementation)
- [Performance Considerations](#performance-considerations)
- [Release Process](#release-process)
- [See Also](#see-also)

## Setup

### Prerequisites

- Python 3.8+
- pip
- git

### Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/your-org/autocsv-profiler.git
cd autocsv-profiler
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e .[dev]
```

### Verification

```bash
# Verify installation
python -c "import autocsv_profiler; print('OK')"

# Check CLI
autocsv-profiler --help
```

## Development Commands

### Installation

```bash
# Development installation
pip install -e .

# With development dependencies
pip install -e .[dev]

# Update dependencies
pip install --upgrade -e .[dev]
```

### Code Quality

```bash
# Format code
black src/autocsv_profiler/ tests/

# Sort imports
isort src/autocsv_profiler/ tests/

# Type checking
mypy src/autocsv_profiler/

# Linting
flake8 src/autocsv_profiler/ tests/

# All quality checks
black src/autocsv_profiler/ tests/ && \
isort src/autocsv_profiler/ tests/ && \
mypy src/autocsv_profiler/ && \
flake8 src/autocsv_profiler/ tests/
```

### Pre-commit Hooks

```bash
# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black
```

## Architecture Overview

### Single-Environment Design

AutoCSV Profiler uses a unified single-environment architecture that eliminates the complexity of multi-environment conda setups.

The [Core Analysis Engine diagram](diagrams.md#core-analysis-engine) illustrates the unified single-environment architecture and component interactions.


### Package Structure

**Public API:**
- Main analysis function: `analyze()`
- Exception classes: `AutoCSVProfilerError`, `FileProcessingError`, `DelimiterDetectionError`, `ReportGenerationError`
- Configuration: `Settings`, `settings` singleton
- Logger utilities: `get_logger()`, `log_print()`
- Version information: `__version__`, version utility functions

**Entry Points:**
- Command-line: `autocsv-profiler` command
- Python module: `autocsv_profiler.cli`
- Python API: `autocsv_profiler.analyze()`

## Testing

### Test Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=autocsv_profiler

# Fast tests only (exclude slow tests)
pytest -m "not slow"

# Specific test categories
pytest -m unit              # Unit tests
pytest -m integration       # Integration tests
pytest -m performance       # Performance tests

# Parallel execution
pytest -n auto

# HTML coverage report
pytest --cov-report=html
```

### Test Structure

- `tests/unit/`: Component-level tests
- `tests/integration/`: Cross-component workflow tests
- `tests/performance/`: Memory and resource tests
- `tests/fixtures/`: Test data and utilities

### Test Markers

- `slow`: Tests that take longer than 5 seconds
- `unit`: Isolated component tests
- `integration`: Multi-component tests
- `performance`: Resource usage tests

### Quality Standards

- **Coverage**: Minimum 50% requirement
- **Line Length**: 88 characters (Black standard)
- **Type Checking**: Strict MyPy configuration
- **Import Sorting**: Black-compatible isort profile

## Code Quality

### Configuration

**Tool configurations:**
- **Black**: Configured in `pyproject.toml` (line length: 88, Python 3.8+ support)
- **isort**: Configured in `pyproject.toml` (Black profile for compatibility)
- **MyPy**: Configured in `mypy.ini` (Python 3.8 baseline for compatibility)
- **flake8**: Configured in `.flake8` file
- **pytest**: Configured in `pytest.ini` (includes test markers and coverage settings)
- **Coverage**: Configured in `pyproject.toml` (50% minimum coverage requirement)

### Development Workflow

1. Create feature branch
2. Make changes
3. Run tests: `pytest`
4. Check code quality: `pre-commit run --all-files`
5. Commit and push
6. Create pull request

## Build and Packaging

### Local Build

```bash
# Build package
python -m build

# Install built package
pip install dist/autocsv_profiler-2.0.0-py3-none-any.whl

# Clean build artifacts
rm -rf build/ dist/ *.egg-info/
```

## Technical Overview

Refer to the [Data Processing Flow diagram](diagrams.md#data-processing-flow) and [Configuration Flow diagram](diagrams.md#configuration-flow) for visual representations of the system architecture.

## Performance Considerations

- **Memory limits**: Configurable via `--memory-limit` or `AUTOCSV_PERFORMANCE_MEMORY_LIMIT_GB`
- **Chunked processing**: Large files processed in configurable chunks (default 10,000 rows)
- **Parallel visualization**: Plot generation uses multiprocessing for performance
- **Memory monitoring**: Real-time tracking prevents exceeding configured limits

## Release Process

### Version Management

1. Update version in `src/autocsv_profiler/version.py`
2. Update `CHANGELOG.md` with release notes
3. Create release commit and tag
4. Build and upload to PyPI

### Release Commands

```bash
# Tag release
git tag v2.0.0
git push origin v2.0.0

# Build for PyPI
python -m build

# Upload to PyPI (requires credentials)
twine upload dist/*
```

### CLI Testing

```bash
# Test CLI with sample data
autocsv-profiler tests/fixtures/sample.csv

# Test interactive mode
autocsv-profiler

# Test API usage
python -c "import autocsv_profiler; autocsv_profiler.analyze('test.csv')"
```

### Debugging

```bash
# Enable debug mode
autocsv-profiler --debug test.csv

# Check logs
tail -f autocsv_profiler.log

# Verify Python version
python --version

# Check package installation
pip list | grep autocsv
```

### Development Standards

- Follow single-environment development patterns
- Preserve Rich UI styling exactly as implemented
- Use direct imports for better performance
- Implement graceful degradation for missing dependencies
- Never use emojis or icons anywhere in code or documentation

## See Also

- [Documentation Index](index.md) - Complete documentation overview
- [User Guide](user-guide.md) - Installation and usage documentation
- [API Reference](api-reference.md) - Python API documentation
- [Configuration](configuration.md) - Settings and environment variables
- [Troubleshooting](troubleshooting.md) - Problem-solving guide
- [Architecture Diagrams](diagrams.md) - Visual system architecture


---

Version: 2.0.0 | Status: Beta | Python: 3.8-3.13

Copyright 2025 dhaneshbb | License: MIT | Homepage: https://github.com/dhaneshbb/autocsv-profiler
