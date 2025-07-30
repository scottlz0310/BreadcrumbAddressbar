# Project Structure

## Directory Organization

```
BreadcrumbAddressbar/
├── breadcrumb_addressbar/          # Main library package
│   ├── __init__.py                # Package exports and version info
│   ├── core.py                    # BreadcrumbAddressBar main widget
│   ├── widgets.py                 # BreadcrumbItem and helper widgets
│   ├── popup.py                   # FolderSelectionPopup implementation
│   ├── themes.py                  # ThemeManager and theme integration
│   └── logger_setup.py            # Logging configuration utilities
├── tests/                         # Test suite
│   ├── __init__.py
│   └── test_core.py              # Core functionality tests
├── examples/                      # Usage examples and demos
│   ├── basic_example.py          # Simple integration example
│   ├── qt_theme_demo.py          # Theme integration demo
│   ├── phase2_example.py         # Advanced features demo
│   └── dropdown_test*.py         # WSL2 compatibility tests
├── docs/                         # Documentation
│   └── BreadcrumbAddressBar.md   # Detailed specification
├── .kiro/                        # Kiro AI assistant configuration
│   └── steering/                 # AI guidance documents
└── venv*/                        # Virtual environments (gitignored)
```

## Code Organization Principles

### Module Responsibilities
- **core.py**: Main BreadcrumbAddressBar widget, path handling, display logic
- **widgets.py**: Individual breadcrumb button components (BreadcrumbItem)
- **popup.py**: Folder selection popup functionality
- **themes.py**: Theme management and qt-theme-manager integration
- **logger_setup.py**: Centralized logging configuration

### Import Structure
```python
# Standard library imports first
import os
from typing import Any, Dict, List, Optional

# Third-party imports second
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget

# Local imports last
from .logger_setup import get_logger
from .widgets import BreadcrumbItem
```

## Naming Conventions

### Files and Directories
- **snake_case**: All file and directory names
- **Descriptive names**: Clear purpose indication (e.g., `logger_setup.py`)

### Code Elements
- **Classes**: PascalCase (e.g., `BreadcrumbAddressBar`, `FolderSelectionPopup`)
- **Methods/Functions**: camelCase for public API, snake_case for internal
- **Variables**: camelCase for local, snake_case with underscore prefix for private
- **Constants**: UPPER_SNAKE_CASE

### Temporary/Debug Code
- **Debug functions**: `_debug_` prefix (must be removed before PR)
- **Temporary variables**: `_temp_` prefix with clear cleanup plan

## Configuration Files

### Package Configuration
- **pyproject.toml**: Modern Python project metadata and tool configuration
- **setup.py**: Legacy compatibility and package building
- **requirements.txt**: Runtime dependencies only

### Development Configuration
- **.cursorrules**: Project-specific development guidelines
- **.gitignore**: Version control exclusions
- **pytest configuration**: In pyproject.toml under `[tool.pytest.ini_options]`

## Testing Structure
- **Unit tests**: `tests/test_*.py` pattern
- **Test classes**: Mirror main class structure (`TestBreadcrumbAddressBar`)
- **Fixtures**: Qt application setup in `setup()` method
- **Test naming**: Descriptive test method names (`test_path_changed_signal`)

## Documentation Structure
- **README.md**: User-facing documentation with examples
- **USAGE.md**: Detailed usage instructions and troubleshooting
- **docs/**: Technical specifications and design documents
- **CHANGELOG.md**: Version history and changes

## Build Artifacts (Gitignored)
- **venv/**, **venv_windows/**: Virtual environments
- **__pycache__/**: Python bytecode cache
- **.mypy_cache/**: Type checking cache
- **breadcrumb_addressbar.egg-info/**: Package metadata
- **build/**, **dist/**: Package build outputs