# Python In Enterprise Lab 1 - Data Analyzer

## Author: Swan Htet Aung Phyo

A Python application for analyzing JSON data records with status and value fields. The application filters records based on status and threshold values, then calculates statistics for valid records.

## Features

- **JSON Data Processing**: Load and parse JSON files containing records with status and value fields
- **Flexible Filtering**: Filter records by status (OK/bad/error) and numeric threshold values
- **Statistical Analysis**: Calculate count, total, and average for valid numeric values
- **Command Line Interface**: Easy-to-use CLI with configurable parameters
- **Robust Error Handling**: Graceful handling of missing files, invalid JSON, and malformed data
- **Comprehensive Testing**: Full test suite with unit tests for all components

## Project Structure

```
lab-1/
├── README.md
├── run_tests.py              # Test runner script
├── setup.py                  # Package installation configuration
├── sample_100.json           # Sample data file
└── src/
    ├── cli/
    │   └── main.py           # Command line interface
    ├── config/
    │   └── settings.py       # Configuration management
    ├── core/
    │   ├── calculator.py     # Statistics calculation
    │   └── filters.py        # Record filtering logic
    ├── data_io/
    │   └── data_loader.py    # JSON data loading
    ├── models/
    │   └── records.py        # Data models
    ├── tests/                # Test suite
    │   ├── __init__.py
    │   ├── test_calculator.py
    │   ├── test_cli.py
    │   ├── test_data_loader.py
    │   ├── test_filters.py
    │   └── test_models.py
    └── utils/
        └── logger.py         # Logging utilities
```

## Installation

1. **Clone or download the project**
2. **Install the package in development mode:**
   ```bash
   cd lab-1
   pip install -e .
   ```

## Usage

### Command Line Interface

The application provides a command-line interface with the following options:

```bash
analyze-data [OPTIONS]
```

**Options:**
- `--file PATH`: Path to input JSON file (default: uses settings configuration)
- `--thres FLOAT`: Threshold value for filtering records (default: 0)
- `--all`: Include all records regardless of status (default: only OK status)

### Examples

1. **Analyze sample data with default settings:**
   ```bash
   analyze-data --file sample_100.json
   ```

2. **Set a threshold value:**
   ```bash
   analyze-data --file sample_100.json --thres 50
   ```

3. **Include all records regardless of status:**
   ```bash
   analyze-data --file sample_100.json --all
   ```

4. **Combine options:**
   ```bash
   analyze-data --file sample_100.json --thres 25 --all
   ```

### Expected Output

The application outputs a summary in the following format:
```
[YYYY/MM/DD-HH:MM:SS] ok_count=N total_value=X.XX avg=Y.YY
```

Example:
```
[2024/10/23-14:30:15] ok_count=15 total_value=847.23 avg=56.48
```

## Data Format

The application expects JSON files containing arrays of records with the following structure:

```json
[
  {
    "status": "ok",
    "value": 88.72
  },
  {
    "status": "bad", 
    "value": 82.1
  },
  {
    "status": "OK",
    "value": "86"
  }
]
```

**Field Details:**
- `status`: Record status (case-insensitive). Accepts "ok", "OK", "bad", "Bad", "error", etc.
- `value`: Numeric value (can be number, string number, or null)

**Alternative field names:**
- `STATUS` can be used instead of `status`
- Missing fields default to "unknown" status and 0 value

## Filtering Logic

### Default Mode (OK only)
- Only includes records with status "ok" or "OK" (case-insensitive)
- Records must have valid numeric values
- Values must be >= threshold

### All Mode (--all flag)
- Includes records with any status
- Records must have valid numeric values
- Threshold filtering still applies

## Testing

The project includes comprehensive unit tests covering all components.

### Run All Tests
```bash
python run_tests.py
```

### Run Specific Test Module
```bash
python run_tests.py models
python run_tests.py calculator
python run_tests.py filters
python run_tests.py data_loader
python run_tests.py cli
```

### Test Coverage
- **Models**: Record validation, numeric conversion, status normalization
- **Calculator**: Statistics computation with various data types
- **Filters**: Record filtering logic with different modes and thresholds
- **Data Loader**: JSON parsing, error handling, fallback data
- **CLI**: Argument parsing, integration testing

## Architecture

### Core Components

1. **Models (`models/records.py`)**
   - `Record`: Data class for individual records
   - `AnalysisResult`: Data class for statistical results

2. **Data Loading (`data_io/data_loader.py`)**
   - `DataLoader`: Handles JSON file loading and parsing
   - Provides fallback data when files are missing or invalid

3. **Filtering (`core/filters.py`)**
   - `RecordFilter`: Filters records based on status and threshold
   - Supports different filtering modes

4. **Statistics (`core/calculator.py`)**
   - `StatisticsCalculator`: Computes count, total, and average
   - Handles various numeric data types

5. **Configuration (`config/settings.py`)**
   - `Settings`: Manages application configuration
   - Supports file-based and argument-based updates

6. **CLI (`cli/main.py`)**
   - Command-line argument parsing
   - Orchestrates the data processing pipeline

### Design Patterns

- **Singleton Pattern**: Used for filter and calculator instances
- **Data Classes**: Used for structured data representation
- **Dependency Injection**: Components are loosely coupled
- **Error Handling**: Graceful degradation with fallback mechanisms

## Error Handling

The application handles various error conditions gracefully:

- **Missing Files**: Uses fallback data when JSON files are not found
- **Invalid JSON**: Falls back to default data on parsing errors
- **Invalid Values**: Skips records with non-numeric values
- **Missing Fields**: Uses default values for missing status/value fields

## Configuration

Default settings can be modified in `src/config/settings.py`:

```python
class Settings:
    def __init__(self):
        self.data_path = Path("data/sample.json")
        self.encoding = 'utf-8'
        self.default_threshold = 0
        self.filter_mode = 'OK'
```

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## Development

### Adding New Features

1. **Add new functionality** in appropriate modules
2. **Write unit tests** in the `tests/` directory
3. **Update documentation** as needed
4. **Run tests** to ensure compatibility

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Include docstrings for public methods
- Maintain test coverage for new code

## License

This project is part of the Python In Enterprise coursework.