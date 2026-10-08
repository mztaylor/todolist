import json
import tempfile
from pathlib import Path
import pytest
from todolist.cli import main

VALID_MD = """---
id: TASK-301
title: "CLI Test Task"
status: "in-progress"
priority: "p2"
created_at: "2026-10-07"
tags: ["cli"]
---
Body content.
"""

INVALID_MD = """---
id: "bad_format"
title: ""
status: "not-a-status"
priority: "p4"
created_at: "not-a-date"
tags: "not-a-list"
---
Body content.
"""

def test_cli_valid_single_file(capsys):
    with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False) as f:
        f.write(VALID_MD)
        path = Path(f.name)
    try:
        exit_code = main(["validate", str(path)])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert "PASSED" in captured.out
    finally:
        path.unlink()

def test_cli_invalid_single_file(capsys):
    with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False) as f:
        f.write(INVALID_MD)
        path = Path(f.name)
    try:
        exit_code = main(["validate", str(path)])
        captured = capsys.readouterr()
        assert exit_code == 1
        assert "FAILED" in captured.out or "FAILED" in captured.err
    finally:
        path.unlink()

def test_cli_directory_scan(capsys):
    with tempfile.TemporaryDirectory() as tmpdir:
        dir_path = Path(tmpdir)
        (dir_path / "valid1.md").write_text(VALID_MD, encoding="utf-8")
        (dir_path / "invalid1.md").write_text(INVALID_MD, encoding="utf-8")

        exit_code = main(["validate", str(dir_path)])
        captured = capsys.readouterr()
        assert exit_code == 1
        assert "valid1.md" in captured.out or "valid1.md" in captured.err
        assert "invalid1.md" in captured.out or "invalid1.md" in captured.err

def test_cli_json_output(capsys):
    with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False) as f:
        f.write(VALID_MD)
        path = Path(f.name)
    try:
        exit_code = main(["validate", str(path), "--json"])
        captured = capsys.readouterr()
        assert exit_code == 0
        data = json.loads(captured.out)
        assert data["summary"]["passed"] == 1
        assert data["summary"]["failed"] == 0
    finally:
        path.unlink()

def test_cli_quiet_flag(capsys):
    with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False) as f:
        f.write(VALID_MD)
        path = Path(f.name)
    try:
        exit_code = main(["validate", str(path), "--quiet"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == ""
    finally:
        path.unlink()

def test_cli_nonexistent_path(capsys):
    exit_code = main(["validate", "/path/does/not/exist/ever.md"])
    captured = capsys.readouterr()
    assert exit_code == 2

def test_cli_no_subcommand(capsys):
    exit_code = main([])
    assert exit_code == 2

def test_cli_empty_directory(capsys):
    with tempfile.TemporaryDirectory() as tmpdir:
        exit_code = main(["validate", tmpdir])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert "No markdown" in captured.out

