"""Tests for scripts/pre-commit-hook.sh git hook integration."""

import os
from pathlib import Path
import subprocess
import tempfile
import pytest

HOOK_PATH = Path(__file__).resolve().parent.parent / "scripts" / "pre-commit-hook.sh"
REPO_ROOT = Path(__file__).resolve().parent.parent

VALID_TASK = """---
id: TASK-999
title: "Valid Hook Test Task"
status: "ready"
priority: "p2"
depth: "deep"
scale: "daily"
time_estimate_minutes: 30
created_at: "2026-10-09"
tags: ["hook-test"]
---

# Objective
Valid task body for hook verification.
"""

INVALID_TASK = """---
id: "invalid_id_format"
title: ""
status: "invalid-status"
priority: "p9"
created_at: "not-a-date"
tags: []
---

# Objective
Invalid task body for hook verification.
"""


def test_hook_executable_exists():
    assert HOOK_PATH.exists()
    assert os.access(HOOK_PATH, os.X_OK)


def test_hook_direct_file_args_valid():
    with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False) as f:
        f.write(VALID_TASK)
        valid_path = Path(f.name)
    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(REPO_ROOT)
        result = subprocess.run(
            [str(HOOK_PATH), str(valid_path)],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
            env=env,
        )
        assert result.returncode == 0
        assert "PASSED" in result.stdout
        assert "All staged task notes are valid" in result.stdout
    finally:
        valid_path.unlink()


def test_hook_direct_file_args_invalid():
    with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False) as f:
        f.write(INVALID_TASK)
        invalid_path = Path(f.name)
    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(REPO_ROOT)
        result = subprocess.run(
            [str(HOOK_PATH), str(invalid_path)],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
            env=env,
        )
        assert result.returncode != 0
        assert "FAILED" in result.stdout or "FAILED" in result.stderr
        assert "Commit rejected" in result.stderr or "Commit rejected" in result.stdout
    finally:
        invalid_path.unlink()


def test_hook_git_diff_staged_detection():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_repo = Path(tmpdir)
        subprocess.run(["git", "init"], cwd=str(tmp_repo), check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=str(tmp_repo), check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=str(tmp_repo), check=True)

        env = os.environ.copy()
        env["PYTHONPATH"] = str(REPO_ROOT)
        result = subprocess.run(
            [str(HOOK_PATH)],
            capture_output=True,
            text=True,
            cwd=str(tmp_repo),
            env=env,
        )
        assert result.returncode == 0

        templates_dir = tmp_repo / "templates"
        templates_dir.mkdir()
        valid_file = templates_dir / "task.md"
        valid_file.write_text(VALID_TASK, encoding="utf-8")
        subprocess.run(["git", "add", "templates/task.md"], cwd=str(tmp_repo), check=True)

        result = subprocess.run(
            [str(HOOK_PATH)],
            capture_output=True,
            text=True,
            cwd=str(tmp_repo),
            env=env,
        )
        assert result.returncode == 0
        assert "All staged task notes are valid" in result.stdout

        invalid_file = templates_dir / "bad.md"
        invalid_file.write_text(INVALID_TASK, encoding="utf-8")
        subprocess.run(["git", "add", "templates/bad.md"], cwd=str(tmp_repo), check=True)

        result = subprocess.run(
            [str(HOOK_PATH)],
            capture_output=True,
            text=True,
            cwd=str(tmp_repo),
            env=env,
        )
        assert result.returncode != 0
        assert "Commit rejected" in result.stderr
