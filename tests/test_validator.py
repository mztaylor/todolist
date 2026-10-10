import tempfile
from pathlib import Path
import pytest

from todolist.validator import (
    extract_frontmatter,
    validate_task_data,
    validate_task_file,
    ValidationResult
)

VALID_MD_CONTENT = """---
id: TASK-200
title: "Configure Task Environment"
status: "ready"
priority: "p1"
depth: "deep"
scale: "daily"
time_estimate_minutes: 30
created_at: "2026-10-07"
tags: ["setup", "core"]
---

# Details
This is the task body.
"""

INVALID_MD_CONTENT = """---
id: "bad-id"
title: "Bad Task"
status: "invalid-status"
priority: "p1"
created_at: "2026-10-07"
tags: []
---

Task body.
"""

NO_FRONTMATTER_MD = """# No Frontmatter
Just markdown content.
"""

MALFORMED_YAML_MD = """---
id: [unclosed list
title: broken
---
Body.
"""

def test_extract_frontmatter_valid():
    with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False) as f:
        f.write(VALID_MD_CONTENT)
        path = Path(f.name)
    try:
        data = extract_frontmatter(path)
        assert data["id"] == "TASK-200"
        assert data["depth"] == "deep"
        assert data["time_estimate_minutes"] == 30
    finally:
        path.unlink()

def test_extract_frontmatter_none():
    with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False) as f:
        f.write(NO_FRONTMATTER_MD)
        path = Path(f.name)
    try:
        result = validate_task_file(path)
        assert not result.is_valid
        assert any("frontmatter" in err.lower() for err in result.errors)
    finally:
        path.unlink()

def test_extract_frontmatter_malformed():
    with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False) as f:
        f.write(MALFORMED_YAML_MD)
        path = Path(f.name)
    try:
        result = validate_task_file(path)
        assert not result.is_valid
        assert any("yaml" in err.lower() for err in result.errors)
    finally:
        path.unlink()

def test_validate_task_file_valid():
    with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False) as f:
        f.write(VALID_MD_CONTENT)
        path = Path(f.name)
    try:
        result = validate_task_file(path)
        assert isinstance(result, ValidationResult)
        assert result.is_valid
        assert len(result.errors) == 0
    finally:
        path.unlink()

def test_validate_task_file_invalid():
    with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False) as f:
        f.write(INVALID_MD_CONTENT)
        path = Path(f.name)
    try:
        result = validate_task_file(path)
        assert not result.is_valid
        assert len(result.errors) > 0
    finally:
        path.unlink()


def test_all_provided_templates_are_valid():
    templates_dir = Path(__file__).resolve().parent.parent / "templates"
    template_files = list(templates_dir.glob("*.md"))
    assert len(template_files) >= 3
    for template_file in template_files:
        result = validate_task_file(template_file)
        assert result.is_valid, f"Template {template_file.name} failed validation: {result.errors}"

