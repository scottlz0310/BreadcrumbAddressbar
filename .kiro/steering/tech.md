# Technology Stack

## Core Technologies
- **Python**: 3.8+ (supports 3.8, 3.9, 3.10, 3.11, 3.12)
- **PySide6**: Primary Qt binding (6.0.0+)
- **qt-theme-manager**: Theme integration (0.2.0+ or 1.0.0+)

## Build System
- **setuptools**: Package building and distribution
- **pyproject.toml**: Modern Python project configuration
- **setup.py**: Legacy compatibility for package metadata

## Development Dependencies
- **pytest**: Testing framework (6.0+)
- **pytest-qt**: Qt-specific testing utilities (4.0+)
- **black**: Code formatting (22.0+)
- **flake8**: Linting (4.0+)
- **isort**: Import sorting

## Common Commands

### Development Setup
```bash
# Clone and setup development environment
git clone <repo-url>
cd BreadcrumbAddressbar
python -m venv venv
venv\Scripts\activate  # Windows
pip install -e ".[dev]"
```

### Testing
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_core.py
```

### Code Quality
```bash
# Format code
black .
isort .

# Lint code
flake8 breadcrumb_addressbar/ tests/ examples/
```

### Package Building
```bash
# Build package
python -m build

# Install in development mode
pip install -e .
```

### Running Examples
```bash
# Basic example
python examples/basic_example.py

# Theme demo
python examples/qt_theme_demo.py

# Phase 2 features demo
python examples/phase2_example.py
```

## Architecture Patterns
- **Qt Signal/Slot**: Primary communication mechanism
- **Widget Composition**: BreadcrumbAddressBar contains BreadcrumbItem widgets
- **Theme Manager Integration**: Pluggable theme system via qt-theme-manager
- **Logging**: Structured logging via Python logging module (no print statements)

## Platform Considerations
- **Path Handling**: Cross-platform path normalization (/ vs \\)
- **Qt Compatibility**: PySide6 primary, designed for future PyQt6 compatibility
- **WSL2 Limitations**: Known QComboBox dropdown issues in WSL2 environment