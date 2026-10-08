import json
from pathlib import Path
import pytest
import jsonschema
from jsonschema import validate, Draft202012Validator

SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "task.schema.json"
FIXTURES_DIR = Path(__file__).parent / "fixtures"

@pytest.fixture(scope="session")
def task_schema():
    assert SCHEMA_PATH.exists(), f"Schema file not found at {SCHEMA_PATH}"
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)
    Draft202012Validator.check_schema(schema)
    return schema

def test_schema_file_exists():
    assert SCHEMA_PATH.exists()

@pytest.mark.parametrize("fixture_file", list((FIXTURES_DIR / "valid").glob("*.json")))
def test_valid_fixtures(task_schema, fixture_file):
    with open(fixture_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    validator = Draft202012Validator(task_schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    assert not errors, f"Expected {fixture_file.name} to be valid, but got errors: {[e.message for e in errors]}"

@pytest.mark.parametrize("fixture_file", list((FIXTURES_DIR / "invalid").glob("*.json")))
def test_invalid_fixtures(task_schema, fixture_file):
    with open(fixture_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    validator = Draft202012Validator(task_schema)
    errors = list(validator.iter_errors(data))
    assert len(errors) > 0, f"Expected {fixture_file.name} to fail validation, but it passed."

def test_status_pipeline_enums(task_schema):
    base_task = {
        "id": "TASK-100",
        "title": "Pipeline test",
        "priority": "p1",
        "created_at": "2026-10-07",
        "tags": []
    }
    allowed_statuses = ["inbox", "backlog", "ready", "in-progress", "waiting", "review", "done"]
    validator = Draft202012Validator(task_schema)
    for status in allowed_statuses:
        task = {**base_task, "status": status}
        assert validator.is_valid(task), f"Status {status} should be valid"
    
    assert not validator.is_valid({**base_task, "status": "completed"})

def test_depth_enum(task_schema):
    base_task = {
        "id": "TASK-100",
        "title": "Depth test",
        "status": "ready",
        "priority": "p1",
        "created_at": "2026-10-07",
        "tags": []
    }
    validator = Draft202012Validator(task_schema)
    assert validator.is_valid({**base_task, "depth": "deep"})
    assert validator.is_valid({**base_task, "depth": "shallow"})
    assert not validator.is_valid({**base_task, "depth": "medium"})

def test_time_estimate_multiples_of_15(task_schema):
    base_task = {
        "id": "TASK-100",
        "title": "Time estimate test",
        "status": "ready",
        "priority": "p1",
        "created_at": "2026-10-07",
        "tags": []
    }
    validator = Draft202012Validator(task_schema)
    assert validator.is_valid({**base_task, "time_estimate_minutes": 15})
    assert validator.is_valid({**base_task, "time_estimate_minutes": 60})
    assert not validator.is_valid({**base_task, "time_estimate_minutes": 10})
    assert not validator.is_valid({**base_task, "time_estimate_minutes": -15})
