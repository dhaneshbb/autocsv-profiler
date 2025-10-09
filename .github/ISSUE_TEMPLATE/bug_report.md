---
name: Bug Report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description

A clear and concise description of what the bug is.

## Environment

**System Information:**
- OS: [e.g., Windows 10, macOS 12.0, Ubuntu 20.04]
- Python Version: [e.g., 3.9.7]
- AutoCSV Profiler Version: [e.g., 2.0.0]

**Installation Method:**
- [ ] PyPI (`pip install autocsv-profiler`)
- [ ] Source installation (`pip install -e .`)
- [ ] Development installation (`pip install -e .[dev]`)

**Dependencies:**
```
# Output of: pip list | grep -E "(pandas|numpy|scipy|matplotlib|seaborn|rich)"
```

## Reproduction Steps

Steps to reproduce the behavior:

1. Create CSV file with the following structure:
   ```csv
   column1,column2,column3
   value1,value2,value3
   ```

2. Run command:
   ```bash
   autocsv-profiler data.csv --option value
   ```

3. Observe error/unexpected behavior

## Expected Behavior

A clear and concise description of what you expected to happen.

## Actual Behavior

A clear and concise description of what actually happened.

## Error Output

```
# Full error message and stack trace
```

## Sample Data

**Data Characteristics:**
- File size: [e.g., 100KB, 10MB, 1GB]
- Number of rows: [e.g., 1000]
- Number of columns: [e.g., 15]
- Column types: [e.g., 5 numeric, 10 text]
- Delimiter: [e.g., comma, semicolon, tab]

**Sample Data** (if possible to share):
```csv
# First few rows of your CSV file
# Remove any sensitive information
```

## Configuration

**Command Used:**
```bash
autocsv-profiler [command and options]
```

**Environment Variables:**
```bash
# Any AUTOCSV_* environment variables set
export AUTOCSV_MEMORY_LIMIT_GB=2
```

**Configuration File** (if applicable):
```yaml
# Configuration file contents
```

## Debug Information

**Debug Output** (run with `--debug` flag):
```
# Output from running with --debug option
```

**Log File Contents:**
```
# Contents of autocsv_profiler.log (if available)
```

## Workaround

If you found a workaround for the issue, please describe it here.

## Additional Context

Add any other context about the problem here:
- Does this happen with all CSV files or specific ones?
- Did this work in a previous version?
- Any recent system or environment changes?
- Related issues or discussions?

For additional troubleshooting help, see [Troubleshooting Guide](../../docs/troubleshooting.md).

## Screenshots

If applicable, add screenshots to help explain your problem.

## Checklist

- [ ] I have searched for existing issues before creating this one
- [ ] I have provided all requested information
- [ ] I have tested with the latest version
- [ ] I have included sample data or a minimal reproduction case
- [ ] I have removed any sensitive information from logs and data samples