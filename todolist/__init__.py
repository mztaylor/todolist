"""Core task contract validation package for todolist."""

from todolist.validator import (
    ValidationResult,
    extract_frontmatter,
    validate_task_data,
    validate_task_file,
)

__version__ = "0.1.0"

__all__ = [
    "ValidationResult",
    "extract_frontmatter",
    "validate_task_data",
    "validate_task_file",
    "__version__",
]
