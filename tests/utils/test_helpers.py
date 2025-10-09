"""
Test helper utilities for AutoCSV Profiler.

Provides common functions and utilities used across multiple test modules.
"""

import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

try:
    import psutil

    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


def create_test_csv(
    file_path: Path,
    data: Optional[Dict[str, List]] = None,
    delimiter: str = ",",
    encoding: str = "utf-8",
    include_header: bool = True,
) -> Path:
    """Create a test CSV file with specified parameters."""
    if data is None:
        # Default test data
        data = {
            "id": [1, 2, 3, 4, 5],
            "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
            "value": [10.5, 20.3, 15.7, 30.2, 25.1],
        }

    df = pd.DataFrame(data)
    df.to_csv(
        file_path, sep=delimiter, index=False, encoding=encoding, header=include_header
    )
    return file_path


def validate_csv_structure(
    file_path: Path,
    expected_columns: Optional[List[str]] = None,
    expected_rows: Optional[int] = None,
    delimiter: Optional[str] = None,
) -> bool:
    """Validate the structure of a CSV file."""
    try:
        # Try to read the CSV
        if delimiter:
            df = pd.read_csv(file_path, sep=delimiter)
        else:
            df = pd.read_csv(file_path)

        # Check columns if specified
        if expected_columns is not None:
            if list(df.columns) != expected_columns:
                return False

        # Check row count if specified
        if expected_rows is not None:
            if len(df) != expected_rows:
                return False

        return True

    except Exception:
        return False


def get_file_size_mb(file_path: Path) -> float:
    """Get file size in megabytes."""
    if file_path.exists():
        return file_path.stat().st_size / (1024 * 1024)
    return 0.0


def create_temp_csv_file(
    data: Optional[Dict[str, List]] = None,
    suffix: str = ".csv",
    delimiter: str = ",",
) -> Path:
    """Create a temporary CSV file for testing."""
    temp_file = Path(tempfile.mktemp(suffix=suffix))
    return create_test_csv(temp_file, data, delimiter)


def cleanup_test_file(file_path: Path) -> bool:
    """Clean up a test file safely."""
    try:
        if file_path.exists():
            file_path.unlink()
        return True
    except Exception:
        return False


def create_large_test_csv(
    file_path: Path,
    num_rows: int = 1000,
    num_columns: int = 5,
    delimiter: str = ",",
) -> Path:
    """Create a larger test CSV file for performance testing."""
    import random
    import string

    data = {}

    # Generate column names
    for i in range(num_columns):
        col_name = f"column_{i}"
        if i == 0:
            # ID column
            data[col_name] = list(range(1, num_rows + 1))
        elif i == 1:
            # String column
            data[col_name] = [
                "".join(random.choices(string.ascii_letters, k=10))
                for _ in range(num_rows)
            ]
        else:
            # Numeric columns
            data[col_name] = [round(random.uniform(0, 100), 2) for _ in range(num_rows)]

    return create_test_csv(file_path, data, delimiter)


class MemoryTracker:
    """Track memory usage during test execution."""

    def __init__(self):
        self.initial_memory = 0.0
        self.peak_memory = 0.0
        self.current_memory = 0.0
        self.available = HAS_PSUTIL

    def start(self):
        """Start memory tracking."""
        if HAS_PSUTIL:
            process = psutil.Process()
            self.initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            self.peak_memory = self.initial_memory
            self.current_memory = self.initial_memory

    def start_tracking(self):
        """Alias for start() method for backward compatibility."""
        self.start()

    def update(self):
        """Update current memory usage."""
        if HAS_PSUTIL:
            process = psutil.Process()
            self.current_memory = process.memory_info().rss / 1024 / 1024  # MB
            if self.current_memory > self.peak_memory:
                self.peak_memory = self.current_memory

    def get_peak_usage_mb(self) -> float:
        """Get peak memory usage in MB."""
        return self.peak_memory

    def get_current_usage_mb(self) -> float:
        """Get current memory usage in MB."""
        self.update()
        return self.current_memory

    def get_memory_increase_mb(self) -> float:
        """Get memory increase since tracking started."""
        return self.current_memory - self.initial_memory

    def update_peak(self):
        """Update peak memory usage - alias for update()."""
        self.update()

    def get_memory_usage_mb(self) -> float:
        """Get current memory usage in MB - alias for get_current_usage_mb()."""
        return self.get_current_usage_mb()


def clean_test_outputs(output_dir: Path) -> bool:
    """Clean up test output directories and files."""
    try:
        if output_dir.exists():
            if output_dir.is_dir():
                shutil.rmtree(output_dir)
            else:
                output_dir.unlink()
        return True
    except Exception:
        return False


def create_test_output_dir(base_dir: Optional[Path] = None) -> Path:
    """Create a temporary test output directory."""
    if base_dir is None:
        base_dir = Path(tempfile.gettempdir())

    test_dir = base_dir / f"autocsv_test_{tempfile.mktemp()[-6:]}"
    test_dir.mkdir(parents=True, exist_ok=True)
    return test_dir


def assert_file_exists_and_not_empty(file_path: Path, min_size_bytes: int = 1) -> bool:
    """Assert that a file exists and is not empty."""
    if not file_path.exists():
        return False

    if file_path.stat().st_size < min_size_bytes:
        return False

    return True


def create_sample_data_dict(num_rows: int = 100) -> Dict[str, List]:
    """Create sample data dictionary for testing."""
    import random
    import string

    return {
        "id": list(range(1, num_rows + 1)),
        "name": [
            "".join(random.choices(string.ascii_letters, k=8)) for _ in range(num_rows)
        ],
        "value": [round(random.uniform(0, 100), 2) for _ in range(num_rows)],
        "category": [random.choice(["A", "B", "C", "D"]) for _ in range(num_rows)],
    }


def assert_valid_csv_file(
    file_path: Path, min_rows: int = 1, min_cols: int = 1
) -> bool:
    """Assert that a CSV file is valid and has minimum rows/columns."""
    try:
        if not file_path.exists():
            return False

        df = pd.read_csv(file_path)

        if len(df) < min_rows:
            return False

        if len(df.columns) < min_cols:
            return False

        return True

    except Exception:
        return False
