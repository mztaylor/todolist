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

## Phase 2: Python Frontmatter Extractor & CLI Validator
- [ ] Task: Write Frontmatter & CLI Tests (TDD Red)
  - [ ] Write unit tests in `tests/test_validator.py` for extracting YAML frontmatter and validating against schema
  - [ ] Write CLI tests in `tests/test_cli.py` testing `--quiet`, `--json`, exit codes, single files, and directories
- [ ] Task: Implement `todolist` Core Package and CLI (TDD Green)
  - [ ] Implement `todolist/__init__.py` and `todolist/validator.py` using `python-frontmatter` / `pyyaml` and `jsonschema`
  - [ ] Implement `todolist/cli.py` with argument parsing and actionable error formatting
  - [ ] Configure `pyproject.toml` or `requirements.txt` for clean installation
- [ ] Task: Verify Test Coverage & Quality Gates
  - [ ] Run `pytest --cov=todolist` and confirm coverage exceeds 80%
  - [ ] Verify compliance with `conductor/code_styleguides/python.md`
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)

## Phase 3: Newport-Aligned Obsidian Templates & CSS Snippets
- [ ] Task: Author Tactical Task Template
  - [ ] Create `templates/task.md` with schema-compliant YAML frontmatter and Dataview checklist sections
- [ ] Task: Author Multi-Scale Planning Templates
  - [ ] Create `templates/weekly-plan.md` for weekly reviews, strategic objectives, and active task pooling
  - [ ] Create `templates/daily-timeblock.md` with dual-column layout (Task Queue / Timeblock Grid)
- [ ] Task: Implement Obsidian Styling Snippets
  - [ ] Create `obsidian/snippets/task-cards.css` styling status pills, priority markers, and deep/shallow badges
- [ ] Task: Validate Templates via CLI Validator
  - [ ] Run `python -m todolist validate templates/` to verify zero schema violations in provided templates
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)

## Phase 4: Standalone Pre-Commit Hook & End-to-End Verification
- [ ] Task: Implement Git Pre-Commit Hook
  - [ ] Create `scripts/pre-commit-hook.sh` inspecting staged `.md` files
  - [ ] Add execution permissions and fail-fast validation logic
- [ ] Task: End-to-End Verification & Documentation
  - [ ] Test pre-commit script against staged valid and invalid markdown files
  - [ ] Verify all test suites pass and documentation reflects CLI and template usage
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)
