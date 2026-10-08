"""Validator module for extracting and validating task frontmatter."""

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import frontmatter
import jsonschema
from jsonschema import Draft202012Validator
import yaml

DEFAULT_SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "task.schema.json"
_CACHED_SCHEMA: Optional[Dict[str, Any]] = None
_CACHED_VALIDATOR: Optional[Draft202012Validator] = None


@dataclass
class ValidationResult:
    """Represents the outcome of validating a task file.

    Attributes:
        file_path: Path to the task file.
        is_valid: Boolean indicating whether validation passed.
        errors: List of human-readable error descriptions.
        data: Extracted task metadata if extraction succeeded.
    """

    file_path: Path
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    data: Optional[Dict[str, Any]] = None


def get_validator(schema_path: Optional[Path] = None) -> Draft202012Validator:
    """Loads and caches the JSON Schema Draft 2020-12 validator.

    Args:
        schema_path: Optional path to schema file. Defaults to DEFAULT_SCHEMA_PATH.

    Returns:
        A compiled Draft202012Validator instance.

    Raises:
        FileNotFoundError: If the schema file does not exist.
        json.JSONDecodeError: If the schema file contains invalid JSON.
    """
    global _CACHED_SCHEMA, _CACHED_VALIDATOR
    target_path = schema_path or DEFAULT_SCHEMA_PATH
    if not target_path.exists():
        raise FileNotFoundError(f"Schema file not found at: {target_path}")

    if schema_path is None and _CACHED_VALIDATOR is not None:
        return _CACHED_VALIDATOR

    with open(target_path, "r", encoding="utf-8") as f:
        schema_data = json.load(f)

    validator = Draft202012Validator(schema_data)
    if schema_path is None:
        _CACHED_SCHEMA = schema_data
        _CACHED_VALIDATOR = validator
    return validator


def extract_frontmatter(file_path: Path) -> Dict[str, Any]:
    """Extracts YAML frontmatter from a CommonMark markdown file.

    Args:
        file_path: Path to the markdown file.

    Returns:
        Dictionary containing extracted metadata.

    Raises:
        ValueError: If file lacks YAML frontmatter or frontmatter is empty.
        yaml.YAMLError: If YAML syntax is invalid.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)
    except yaml.YAMLError as exc:
        raise ValueError(f"YAML parsing error in {file_path}: {exc}") from exc

    if not post.metadata:
        raise ValueError(f"No YAML frontmatter found in {file_path}")

    return dict(post.metadata)


def validate_task_data(
    data: Dict[str, Any], schema_path: Optional[Path] = None
) -> List[str]:
    """Validates raw task dictionary against the schema.

    Args:
        data: Task metadata dictionary.
        schema_path: Optional path to custom schema file.

    Returns:
        List of formatted error messages (empty if valid).
    """
    validator = get_validator(schema_path)
    errors: List[str] = []
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        loc = ".".join(str(p) for p in err.path) if err.path else "root"
        errors.append(f"[{loc}] {err.message}")
    return errors


def validate_task_file(
    file_path: Path, schema_path: Optional[Path] = None
) -> ValidationResult:
    """Validates a single markdown task file against the canonical schema.

    Args:
        file_path: Path to the markdown file.
        schema_path: Optional custom schema path.

    Returns:
        ValidationResult containing validation status, errors, and metadata.
    """
    try:
        data = extract_frontmatter(file_path)
    except (ValueError, yaml.YAMLError) as err:
        return ValidationResult(
            file_path=file_path,
            is_valid=False,
            errors=[str(err)],
            data=None,
        )

    errors = validate_task_data(data, schema_path=schema_path)
    return ValidationResult(
        file_path=file_path,
        is_valid=len(errors) == 0,
        errors=errors,
        data=data,
    )
