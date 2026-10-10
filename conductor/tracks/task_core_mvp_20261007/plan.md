# Implementation Plan: Task Core MVP (Schemas, Validator CLI, and Newport-Aligned Obsidian Templates)

## Phase 1: Canonical Task Schema & Test Fixtures [checkpoint: cfd04e6]
- [x] Task: Write Schema Validation Tests & Test Fixtures (TDD Red) de056cc
  - [x] Set up Python environment dependencies (`jsonschema`, `pyyaml`, `pytest`, `pytest-cov`)
  - [x] Create test fixtures for valid tasks (standard, Newport deep/shallow, waiting_on, time estimates)
  - [x] Create test fixtures for invalid tasks (malformed IDs, invalid enums, non-multipleOf 15 estimates)
  - [x] Write pytest suite in `tests/test_schema.py` asserting schema validation behavior
- [x] Task: Implement Canonical JSON Schema (TDD Green) 0bccd4f
  - [x] Create `schemas/task.schema.json` using JSON Schema Draft 2020-12
  - [x] Define required fields (`id`, `title`, `status`, `priority`, `created_at`, `tags`)
  - [x] Define Newport fields (`depth`, `scale`, `waiting_on`, `time_estimate_minutes`)
  - [x] Ensure strict constraints (`additionalProperties: false`, regex patterns, integer multiples)
- [x] Task: Refactor and Verify Schema Tests cfd04e6
  - [x] Verify 100% of schema test fixtures pass
- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md) cfd04e6

## Phase 2: Python Frontmatter Extractor & CLI Validator [checkpoint: 2c551d8]
- [x] Task: Write Frontmatter & CLI Tests (TDD Red) 0894862
  - [x] Write unit tests in `tests/test_validator.py` for extracting YAML frontmatter and validating against schema
  - [x] Write CLI tests in `tests/test_cli.py` testing `--quiet`, `--json`, exit codes, single files, and directories
- [x] Task: Implement `todolist` Core Package and CLI (TDD Green) 6771e9a
  - [x] Implement `todolist/__init__.py` and `todolist/validator.py` using `python-frontmatter` / `pyyaml` and `jsonschema`
  - [x] Implement `todolist/cli.py` with argument parsing and actionable error formatting
  - [x] Configure `pyproject.toml` or `requirements.txt` for clean installation
- [x] Task: Verify Test Coverage & Quality Gates 2c551d8
  - [x] Run `pytest --cov=todolist` and confirm coverage exceeds 80%
  - [x] Verify compliance with `conductor/code_styleguides/python.md`
- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md) 2c551d8

## Phase 3: Newport-Aligned Obsidian Templates & CSS Snippets [checkpoint: a9a6cc7]
- [x] Task: Author Tactical Task Template ee4ad42
  - [x] Create `templates/task.md` with schema-compliant YAML frontmatter and Dataview checklist sections
- [x] Task: Author Multi-Scale Planning Templates 8fb9d2e
  - [x] Create `templates/weekly-plan.md` for weekly reviews, strategic objectives, and active task pooling
  - [x] Create `templates/daily-timeblock.md` with dual-column layout (Task Queue / Timeblock Grid)
- [x] Task: Implement Obsidian Styling Snippets 6f437f9
  - [x] Create `obsidian/snippets/task-cards.css` styling status pills, priority markers, and deep/shallow badges
- [x] Task: Validate Templates via CLI Validator 65eb363
  - [x] Run `python -m todolist validate templates/` to verify zero schema violations in provided templates
- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md) a9a6cc7

## Phase 4: Standalone Pre-Commit Hook & End-to-End Verification [checkpoint: f961d03]
- [x] Task: Implement Git Pre-Commit Hook 677c616
  - [x] Create `scripts/pre-commit-hook.sh` inspecting staged `.md` files
  - [x] Add execution permissions and fail-fast validation logic
- [x] Task: End-to-End Verification & Documentation f961d03
  - [x] Test pre-commit script against staged valid and invalid markdown files
  - [x] Verify all test suites pass and documentation reflects CLI and template usage
- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md) f961d03
