# API Reference

## Table of Contents
- [Main Functions](#main-functions)
- [Alternative Function Names](#alternative-function-names)
- [Core Classes](#core-classes)
- [Exceptions](#exceptions)
- [Utility Functions](#utility-functions)
- [Constants](#constants)
- [Integration Examples](#integration-examples)
- [Advanced Usage Patterns](#advanced-usage-patterns)
- [See Also](#see-also)

## Main Functions

### autocsv_profiler.analyze()

Primary function for CSV analysis.

See the [CLI and API Architecture diagram](diagrams.md#cli-and-api-architecture) for the relationship between the API function and the internal analysis workflow.

```python
def analyze(
    csv_file_path: str,
    output_dir: Optional[str] = None,
    delimiter: Optional[str] = None,
    interactive: bool = False,
    chunk_size: int = 10000,
    memory_limit_gb: int = 1
) -> str
```

**Parameters:**
- `csv_file_path` (str) - Path to CSV file to analyze
- `output_dir` (Optional[str]) - Output directory. Defaults to `{csv_filename}_analysis/`
- `delimiter` (Optional[str]) - CSV delimiter. Auto-detected if None
- `interactive` (bool) - Enable interactive analysis mode
- `chunk_size` (int) - Chunk size for large file processing
- `memory_limit_gb` (int) - Memory limit in GB

**Returns:**
- `str` - Path to output directory containing analysis results

**Raises:**
- `FileNotFoundError` - CSV file does not exist
- `AutoCSVProfilerError` - Analysis processing error
- `ImportError` - Required dependencies missing

**Example:**
```python
import autocsv_profiler

# Basic analysis
result_path = autocsv_profiler.analyze('data.csv')
print(f"Analysis saved to: {result_path}")

# With custom settings
result_path = autocsv_profiler.analyze(
    csv_file_path='large_data.csv',
    output_dir='analysis_results/',
    delimiter=';',
    chunk_size=20000,
    memory_limit_gb=2
)
```

## Alternative Function Names

Legacy aliases for backward compatibility:

```python
# All equivalent to analyze()
autocsv_profiler.run_analysis('data.csv')
autocsv_profiler.auto_csv_main('data.csv')
autocsv_profiler.analyze_csv('data.csv')
```

## Core Classes

### BaseProfiler

Abstract base class for profiler implementations.

```python
from autocsv_profiler import ProfilerBase

class CustomProfiler(ProfilerBase):
    def analyze(self, data):
        # Implementation
        pass
```

### Settings

Configuration management singleton.

```python
from autocsv_profiler import Settings, settings

# Access current settings
current_settings = settings
memory_limit = settings.get('performance', 'memory_limit_gb')

# Reset settings (testing)
Settings.reset_instance()
```

## Exceptions

### AutoCSVProfilerError

Base exception class.

```python
from autocsv_profiler import AutoCSVProfilerError

try:
    autocsv_profiler.analyze('nonexistent.csv')
except AutoCSVProfilerError as e:
    print(f"Analysis failed: {e}")
```

### FileProcessingError

File-related processing errors.

```python
from autocsv_profiler import FileProcessingError

try:
    autocsv_profiler.analyze('corrupted.csv')
except FileProcessingError as e:
    print(f"File processing error: {e}")
```

### DelimiterDetectionError

Delimiter detection failures.

```python
from autocsv_profiler import DelimiterDetectionError

try:
    autocsv_profiler.analyze('weird_format.csv')
except DelimiterDetectionError as e:
    print(f"Could not detect delimiter: {e}")
```

### ReportGenerationError

Report generation failures.

```python
from autocsv_profiler import ReportGenerationError

try:
    autocsv_profiler.analyze('data.csv')
except ReportGenerationError as e:
    print(f"Report generation failed: {e}")
```

## Utility Functions

### Version Information

```python
from autocsv_profiler import (
    __version__,
    __version_info__,
    get_version_info,
    get_full_version_info,
    check_python_version
)

print(f"Version: {__version__}")
print(f"Version tuple: {__version_info__}")

# Detailed version info
version_details = get_full_version_info()
dependencies = get_dependency_versions()

# Python version check
if check_python_version((3, 8)):
    print("Python version compatible")
```

### Logging

```python
from autocsv_profiler import get_logger, log_print

# Get package logger
logger = get_logger('autocsv_profiler')
logger.info("Custom logging message")

# Rich console logging
log_print("Message with Rich formatting", level="INFO")
```

## Constants

```python
from autocsv_profiler import DEFAULT_CHUNK_SIZE, DEFAULT_MEMORY_LIMIT_GB

print(f"Default chunk size: {DEFAULT_CHUNK_SIZE}")
print(f"Default memory limit: {DEFAULT_MEMORY_LIMIT_GB}GB")
```

## Integration Examples

### Custom Error Handling

```python
import autocsv_profiler
from autocsv_profiler import (
    FileProcessingError,
    DelimiterDetectionError,
    ReportGenerationError
)

def safe_analysis(csv_path):
    try:
        return autocsv_profiler.analyze(csv_path)
    except FileProcessingError:
        print("File processing failed")
    except DelimiterDetectionError:
        print("Could not detect CSV delimiter")
    except ReportGenerationError:
        print("Report generation failed")
    except Exception as e:
        print(f"Unexpected error: {e}")
```

### Batch Processing

```python
import autocsv_profiler
from pathlib import Path

def batch_analyze(csv_directory):
    csv_files = Path(csv_directory).glob("*.csv")
    results = []

    for csv_file in csv_files:
        try:
            result = autocsv_profiler.analyze(
                str(csv_file),
                output_dir=f"results/{csv_file.stem}/",
                memory_limit_gb=2
            )
            results.append(result)
        except Exception as e:
            print(f"Failed to analyze {csv_file}: {e}")

    return results
```

## Advanced Usage Patterns

### Workflow Integration

Integrate AutoCSV Profiler into data processing workflows:

### Data Pipeline Integration

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
import autocsv_profiler

def analyze_daily_data(**context):
    """Airflow task to analyze daily CSV data."""
    data_date = context['ds']
    input_path = f"/data/daily_exports/{data_date}.csv"
    output_path = f"/data/analysis_results/{data_date}/"

    result = autocsv_profiler.analyze(
        csv_file_path=input_path,
        output_dir=output_path,
        memory_limit_gb=4,
        chunk_size=50000
    )

    context['task_instance'].xcom_push(
        key='analysis_result',
        value={'status': 'success', 'output_path': result}
    )

# DAG definition
dag = DAG(
    'daily_csv_analysis',
    schedule_interval='@daily',
    catchup=False
)

analyze_task = PythonOperator(
    task_id='analyze_daily_data',
    python_callable=analyze_daily_data,
    dag=dag
)
```

### Database Integration

```python
import sqlalchemy as sa
from sqlalchemy import create_engine

class DatabaseCSVAnalyzer:
    """Analyze CSV data stored in databases."""

    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)

    def analyze_table(self, table_name: str, output_dir: str, query: str = None) -> str:
        """Analyze database table as CSV data."""
        import tempfile

        if query:
            df = pd.read_sql(query, self.engine)
        else:
            df = pd.read_sql_table(table_name, self.engine)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            df.to_csv(temp_file.name, index=False)
            temp_csv_path = temp_file.name

        try:
            result = autocsv_profiler.analyze(
                csv_file_path=temp_csv_path,
                output_dir=output_dir
            )
            return result
        finally:
            os.remove(temp_csv_path)

# Usage
db_analyzer = DatabaseCSVAnalyzer('postgresql://user:pass@localhost/db')
result = db_analyzer.analyze_table('sales_data', '/analysis/sales/')
```

### Plugin System

```python
from abc import ABC, abstractmethod

class AnalysisPlugin(ABC):
    """Base class for analysis plugins."""

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def analyze(self, data: pd.DataFrame) -> dict:
        pass

class DataQualityPlugin(AnalysisPlugin):
    """Plugin for data quality assessment."""

    def get_name(self) -> str:
        return "data_quality"

    def analyze(self, data: pd.DataFrame) -> dict:
        """Assess data quality metrics."""
        quality_report = {}
        for column in data.columns:
            col_data = data[column]
            quality_report[column] = {
                'completeness': (col_data.notna().sum() / len(col_data)) * 100,
                'uniqueness': (col_data.nunique() / len(col_data)) * 100
            }
        return quality_report

class ExtendedAnalyzer:
    """Extended analyzer with plugin support."""

    def __init__(self):
        self.plugins = []

    def register_plugin(self, plugin: AnalysisPlugin):
        self.plugins.append(plugin)

    def analyze_with_plugins(self, csv_path: str, output_dir: str) -> dict:
        standard_result = autocsv_profiler.analyze(csv_path, output_dir=output_dir)
        data = pd.read_csv(csv_path)

        plugin_results = {}
        for plugin in self.plugins:
            plugin_results[plugin.get_name()] = plugin.analyze(data)

        return {
            'standard_analysis': standard_result,
            'plugin_results': plugin_results
        }

# Usage
analyzer = ExtendedAnalyzer()
analyzer.register_plugin(DataQualityPlugin())
results = analyzer.analyze_with_plugins('/path/to/data.csv', '/path/to/output/')
```

### REST API Wrapper

```python
from flask import Flask, request, jsonify
import autocsv_profiler
import tempfile
import uuid

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_csv_api():
    """REST API endpoint for CSV analysis."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    config = {
        'memory_limit_gb': float(request.form.get('memory_limit_gb', 1.0)),
        'chunk_size': int(request.form.get('chunk_size', 10000))
    }

    analysis_id = str(uuid.uuid4())

    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, file.filename)
        file.save(file_path)

        output_dir = os.path.join('/app/results', analysis_id)
        os.makedirs(output_dir, exist_ok=True)

        result = autocsv_profiler.analyze(
            csv_file_path=file_path,
            output_dir=output_dir,
            **config
        )

        return jsonify({
            'analysis_id': analysis_id,
            'status': 'completed',
            'output_directory': result
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## See Also

- [Documentation Index](index.md) - Complete documentation overview
- [User Guide](user-guide.md) - Installation and usage documentation
- [Configuration](configuration.md) - Settings and environment variables
- [Developer Guide](developer-guide.md) - Development documentation
- [Troubleshooting](troubleshooting.md) - Problem-solving guide
- [Architecture Diagrams](diagrams.md) - Visual system architecture

---

Version: 2.0.0 | Status: Beta | Python: 3.8-3.13

Copyright 2025 dhaneshbb | License: MIT | Homepage: https://github.com/dhaneshbb/autocsv-profiler
