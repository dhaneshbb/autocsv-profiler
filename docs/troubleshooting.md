# Troubleshooting Guide

## Table of Contents
- [Memory Issues](#memory-issues)
- [File Processing Problems](#file-processing-problems)
- [Delimiter Detection Failures](#delimiter-detection-failures)
- [Encoding Problems](#encoding-problems)
- [Performance Issues](#performance-issues)
- [Installation Problems](#installation-problems)
- [Visualization Errors](#visualization-errors)
- [Configuration Issues](#configuration-issues)
- [Getting Help](#getting-help)
- [See Also](#see-also)

## Memory Issues

### Memory Limit Exceeded

**Symptom**: Analysis fails with memory errors or system becomes unresponsive.

**Causes**:
- File size exceeds available memory
- Default memory limit (1GB) too restrictive
- Insufficient system memory

**Solutions**:

1. **Increase memory limit**:
```bash
# CLI option
autocsv-profiler large_file.csv --memory-limit 4.0

# Environment variable
export AUTOCSV_PERFORMANCE_MEMORY_LIMIT_GB=4
autocsv-profiler large_file.csv

# Python API
autocsv_profiler.analyze('large_file.csv', memory_limit_gb=4)
```

2. **Reduce chunk size for large files**:
```bash
# Smaller chunks use less memory
autocsv-profiler large_file.csv --chunk-size 5000

# Environment variable
export AUTOCSV_PERFORMANCE_CHUNK_SIZE=5000
```

3. **Monitor memory usage**:
```python
import psutil

def check_memory():
    memory = psutil.virtual_memory()
    print(f"Available: {memory.available / (1024**3):.2f} GB")
    print(f"Used: {memory.used / (1024**3):.2f} GB")
    print(f"Percentage: {memory.percent}%")

check_memory()
```

### Out of Memory During Analysis

**Symptom**: Process killed or MemoryError exception.

**Diagnostic Steps**:
```bash
# Check file size
ls -lh data.csv

# Check available memory
free -h  # Linux
wmic OS get TotalVisibleMemorySize,FreePhysicalMemory  # Windows

# Test with smaller file first
head -1000 large_file.csv > test_sample.csv
autocsv-profiler test_sample.csv
```

**Solutions**:
```bash
# Conservative memory settings
autocsv-profiler large_file.csv \
    --memory-limit 0.5 \
    --chunk-size 1000 \
    --non-interactive
```

### Memory Leaks

**Symptom**: Memory usage increases over time during batch processing.

**Prevention**:
```python
import gc

def batch_process_with_cleanup(file_list):
    for csv_file in file_list:
        try:
            autocsv_profiler.analyze(csv_file)
        finally:
            # Force garbage collection
            gc.collect()
```

## File Processing Problems

### File Not Found

**Symptom**: `FileNotFoundError` or "File not found" message.

**Diagnostic Steps**:
```bash
# Check file exists
ls -la data.csv

# Check permissions
ls -l data.csv

# Check file path
realpath data.csv  # Linux/macOS
```

**Solutions**:
```bash
# Use absolute path
autocsv-profiler /full/path/to/data.csv

# Check current directory
pwd
ls *.csv

# Fix permissions
chmod 644 data.csv  # Linux/macOS
```

### Empty or Corrupted Files

**Symptom**: "CSV file is empty" or parsing errors.

**Diagnostic Steps**:
```bash
# Check file size
wc -l data.csv
file data.csv

# View first few lines
head data.csv

# Check for binary content
file data.csv
```

**Solutions**:
```bash
# Validate CSV format
csvlint data.csv  # If available

# Try with different encoding
autocsv-profiler data.csv --debug

# Clean data first
sed 's/\r$//' data.csv > cleaned.csv  # Remove Windows line endings
```

### Permission Denied

**Symptom**: Permission errors when reading files or writing output.

**Solutions**:
```bash
# Fix file permissions
chmod 644 input.csv  # Linux/macOS

# Fix directory permissions
chmod 755 output_directory/

# Run with different user
sudo autocsv-profiler data.csv  # Not recommended

# Use accessible directory
autocsv-profiler data.csv --output ~/results/
```

## Delimiter Detection Failures

### Cannot Detect Delimiter

**Symptom**: "Could not determine delimiter" error.

**Diagnostic Steps**:
```bash
# Examine file structure
head -5 data.csv
hexdump -C data.csv | head  # Show exact characters

# Check for unusual delimiters
grep -o '[^a-zA-Z0-9 ]' data.csv | sort | uniq -c
```

**Solutions**:

1. **Specify delimiter explicitly**:
```bash
# Common delimiters
autocsv-profiler data.csv --delimiter ","
autocsv-profiler data.csv --delimiter ";"
autocsv-profiler data.csv --delimiter $'\t'  # Tab
autocsv-profiler data.csv --delimiter "|"
```

2. **Handle unusual delimiters**:
```bash
# Multiple characters
autocsv-profiler data.csv --delimiter "::"

# Special characters
autocsv-profiler data.csv --delimiter "~"
```

3. **Debug delimiter detection**:
```python
import autocsv_profiler

# Enable debug mode
autocsv_profiler.analyze('data.csv', debug=True)
```

### Inconsistent Delimiters

**Symptom**: Some rows parse correctly, others fail.

**Solutions**:
```bash
# Clean data first
sed 's/;;/;/g' data.csv > cleaned.csv  # Remove double delimiters

# Use more flexible parser
autocsv-profiler data.csv --delimiter "," --debug
```

## Encoding Problems

### Character Encoding Errors

**Symptom**: UnicodeDecodeError or garbled characters in output.

**Diagnostic Steps**:
```bash
# Detect encoding
file -i data.csv  # Linux/macOS
chardet data.csv  # If chardet installed

# Check for BOM
hexdump -C data.csv | head -1
```

**Solutions**:

1. **Convert encoding first**:
```bash
# Convert to UTF-8
iconv -f iso-8859-1 -t utf-8 data.csv > data_utf8.csv

# Remove BOM
sed '1s/^\xEF\xBB\xBF//' data.csv > data_nobom.csv
```

2. **Handle encoding in Python**:
```python
import pandas as pd

# Try different encodings
encodings = ['utf-8', 'iso-8859-1', 'cp1252', 'utf-16']

for encoding in encodings:
    try:
        df = pd.read_csv('data.csv', encoding=encoding)
        print(f"Success with encoding: {encoding}")
        break
    except UnicodeDecodeError:
        continue
```

### International Characters

**Symptom**: Non-ASCII characters display incorrectly.

**Solutions**:
```bash
# Ensure UTF-8 locale
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

# Check terminal encoding
locale
```

## Performance Issues

### Slow Analysis

**Symptom**: Analysis takes much longer than expected.

**Diagnostic Steps**:
```bash
# Check system resources
top
htop  # If available

# Check I/O wait
iostat 1  # Linux

# Profile analysis
time autocsv-profiler data.csv
```

**Solutions**:

1. **Optimize settings**:
```bash
# Increase chunk size for large files
autocsv-profiler data.csv --chunk-size 50000

# Increase memory limit
autocsv-profiler data.csv --memory-limit 4.0

# Skip interactive mode
autocsv-profiler data.csv --non-interactive
```

2. **System optimization**:
```bash
# Close other applications
# Use SSD storage for better I/O
# Ensure sufficient RAM available
```

### High CPU Usage

**Symptom**: Analysis consumes excessive CPU resources.

**Solutions**:
```python
# Limit multiprocessing
import os
os.environ['AUTOCSV_MAX_WORKERS'] = '2'

# Monitor CPU usage
import psutil
print(f"CPU cores: {psutil.cpu_count()}")
print(f"CPU usage: {psutil.cpu_percent()}%")
```

### Disk Space Issues

**Symptom**: "No space left on device" or analysis fails during output generation.

**Solutions**:
```bash
# Check disk space
df -h

# Clean temporary files
rm -rf /tmp/autocsv_*

# Use different output directory
autocsv-profiler data.csv --output /path/with/space/
```

## Installation Problems

### Import Errors

**Symptom**: "ModuleNotFoundError" or import failures.

**Diagnostic Steps**:
```bash
# Check installation
pip list | grep autocsv-profiler

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Verify installation
python -c "import autocsv_profiler; print('OK')"
```

**Solutions**:
```bash
# Reinstall package
pip uninstall autocsv-profiler
pip install autocsv-profiler

# Install in development mode
pip install -e .

# Fix virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### Dependency Conflicts

**Symptom**: Version conflicts or missing dependencies.

**Solutions**:
```bash
# Check for conflicts
pip check

# Update dependencies
pip install --upgrade autocsv-profiler

# Use clean environment
python -m venv clean_env
source clean_env/bin/activate
pip install autocsv-profiler
```

### CLI Not Found

**Symptom**: "autocsv-profiler: command not found".

**Solutions**:
```bash
# Check PATH
echo $PATH

# Use full path
python -m autocsv_profiler.cli data.csv

# Reinstall with scripts
pip install --force-reinstall autocsv-profiler

# Check installation location
pip show -f autocsv-profiler
```

## Visualization Errors

### Plot Generation Failures

**Symptom**: "Failed to generate plots" or missing visualization files.

**Solutions**:

1. **Check matplotlib backend**:
```python
import matplotlib
print(f"Backend: {matplotlib.get_backend()}")

# Force Agg backend
import matplotlib
matplotlib.use('Agg')
```

2. **Install visualization dependencies**:
```bash
pip install matplotlib seaborn

# Fix GUI dependencies (if needed)
sudo apt-get install python3-tk  # Linux
```

3. **Check output permissions**:
```bash
# Ensure output directory is writable
ls -ld output_directory/
chmod 755 output_directory/
```

### Font Issues

**Symptom**: Warning about fonts or plot text rendering issues.

**Solutions**:
```python
# Clear matplotlib cache
import matplotlib
matplotlib.font_manager._rebuild()

# Use default fonts
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'DejaVu Sans'
```

## Configuration Issues

### Environment Variables Not Working

**Symptom**: Settings not applied from environment variables.

**Diagnostic Steps**:
```bash
# Check environment variables
env | grep AUTOCSV_

# Verify format
echo $AUTOCSV_PERFORMANCE_MEMORY_LIMIT_GB
```

**Solutions**:
```bash
# Correct format
export AUTOCSV_PERFORMANCE_MEMORY_LIMIT_GB=2
export AUTOCSV_PERFORMANCE_CHUNK_SIZE=20000

# Verify settings
python -c "from autocsv_profiler import settings; print(settings.get('performance'))"
```

### Invalid Configuration

**Symptom**: "ConfigValidationError" when starting analysis.

**Solutions**:
```bash
# Check valid values
export AUTOCSV_PERFORMANCE_MEMORY_LIMIT_GB=1.0  # Must be > 0
export AUTOCSV_PERFORMANCE_CHUNK_SIZE=10000     # Must be > 0
export AUTOCSV_LOGGING_LEVEL=INFO              # Valid log level

# Reset configuration
unset AUTOCSV_PERFORMANCE_MEMORY_LIMIT_GB
```

## Getting Help

### Debug Mode

Enable debug mode for detailed error information:
```bash
autocsv-profiler data.csv --debug
```

### Log Files

Check log files for detailed information:
```bash
# Default log location
cat autocsv_profiler.log

# Custom log location
export AUTOCSV_LOGGING_FILE_FILENAME=debug.log
```

### System Information

Collect system information for support:
```python
import autocsv_profiler
import sys
import platform

print(f"AutoCSV Profiler: {autocsv_profiler.__version__}")
print(f"Python: {sys.version}")
print(f"Platform: {platform.platform()}")
print(f"Dependencies: {autocsv_profiler.get_dependency_versions()}")
```

### Report Issues

When reporting issues, include:
- Error message or symptom
- Command or code that failed
- System information (OS, Python version)
- Sample data (if possible)
- Debug output

## See Also

- [Documentation Index](index.md) - Complete documentation overview
- [User Guide](user-guide.md) - Setup and requirements
- [API Reference](api-reference.md) - Python API documentation
- [Configuration](configuration.md) - Settings and environment variables
- [Developer Guide](developer-guide.md) - Implementation details
- [Architecture Diagrams](diagrams.md) - Visual system architecture

---

Version: 2.0.0 | Status: Beta | Python: 3.8-3.13

Copyright 2025 dhaneshbb | License: MIT | Homepage: https://github.com/dhaneshbb/autocsv-profiler
