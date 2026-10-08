# Specification: Task Core MVP (Schemas, Validator CLI, and Newport-Aligned Obsidian Templates)

## 1. Overview
The goal of this track is to implement the core contract engine of `todolist`, aligned with Cal Newport's productivity philosophy (*Capture-Configure-Control*, *Multi-Scale Planning*, and *Deep vs. Shallow Work*). This includes the canonical JSON Schema (Draft 2020-12) defining structured tasks, a Python package and CLI validator for Markdown frontmatter, Newport-tailored Obsidian templates (tactical tasks, weekly planning, and daily time-blocking), visual CSS snippets for status and depth pills, and a standalone Git pre-commit hook enforcing schema integrity.

## 2. Functional Requirements

### 2.1 Canonical Task Schema (`schemas/task.schema.json`)
- Implemented as JSON Schema Draft 2020-12.
- Defines required and optional frontmatter fields:
  - `id`: String matching regex `^[A-Z]+-[0-9]+$` (e.g., `TASK-101`, `WORK-204`). Required.
  - `title`: Non-empty string. Required.
  - `status`: String enum `['inbox', 'backlog', 'ready', 'in-progress', 'waiting', 'review', 'done']`. Required.
    - `'inbox'` supports raw capture before triage/configuration.
    - `'waiting'` captures tasks blocked on external entities or delegation.
  - `priority`: String enum `['p1', 'p2', 'p3']`. Required.
  - `depth`: String enum `['deep', 'shallow']`. Optional. Enables batching administrative shallow tasks vs. scheduling dedicated deep focus blocks.
  - `scale`: String enum `['daily', 'weekly', 'strategic']`. Optional (defaults to `'daily'`). Maps to multi-scale planning horizon.
  - `waiting_on`: String. Optional. Specifies the person, ticket, or external dependency blocking progress when `status: 'waiting'`.
  - `time_estimate_minutes`: Integer, multiple of 15 (e.g., 15, 30, 45, 60, 90). Optional. Facilitates realistic daily time-block planning.
  - `created_at`: String formatted as ISO 8601 date (`YYYY-MM-DD`). Required.
  - `due`: String formatted as ISO 8601 date (`YYYY-MM-DD`). Optional/Nullable.
  - `completed_at`: String formatted as ISO 8601 date (`YYYY-MM-DD`). Optional/Nullable.
  - `tags`: Array of strings. Required (can be empty).
- Rejects additional undeclared top-level properties unless namespaced.

### 2.2 Python Validation Engine & CLI (`todolist/`)
- Package structure:
  - `todolist/__init__.py`
  - `todolist/validator.py`: Frontmatter extraction (YAML) and validation against `schemas/task.schema.json` using `jsonschema`.
  - `todolist/cli.py`: CLI entry point (`python -m todolist validate <path>`).
- Features:
  - Validates a single `.md` file or recursively scans directories.
  - Validates Newport attributes (`depth`, `scale`, `multipleOf: 15` constraints, and `waiting_on` logic).
  - Pinpoints offending file, line/field, and schema constraint on failure with non-zero exit code.
  - Supports `--quiet` and `--json` output formats.

### 2.3 Templates & Obsidian Artifacts
- `templates/task.md`:
  - Standard tactical task template adhering to `task.schema.json` (frontmatter with depth, scale, time estimates, Dataview-compatible checklist body).
- `templates/weekly-plan.md`:
  - Weekly review & multi-scale configuration template: reviewing strategic objectives, selecting the week's active task pool, and capacity planning.
- `templates/daily-timeblock.md`:
  - Daily time-blocking template: dual-column layout with Task Queue / Capture pool on the left and a 30-minute/hour Time-Block Grid on the right.
- `obsidian/snippets/task-cards.css`:
  - Visual styling for status pills, priority badges, and distinct deep vs. shallow badges in Obsidian Reading and Kanban views.

### 2.4 Pre-Commit Hook Integration (`scripts/pre-commit-hook.sh`)
- Executable POSIX shell script.
- Scans `git diff --cached --name-only --diff-filter=ACM` for staged markdown files in task directories.
- Executes `python -m todolist validate` on each staged file.
- Aborts commits with clear diagnostics if any note violates the schema.

## 3. Non-Functional Requirements
- **Performance:** Sub-second execution (<100ms for single files; <1s for directories) for seamless pre-commit hook runs.
- **Offline / Local-First:** 100% offline, zero network requests, zero telemetry.
- **Code Quality:** PEP 8 compliance, explicit type hints, and >80% test coverage via `pytest`.

## 4. Acceptance Criteria
- [ ] `schemas/task.schema.json` correctly validates Newport fields (`depth`, `scale`, `status: inbox/waiting`, `waiting_on`, `time_estimate_minutes` with `multipleOf: 15`).
- [ ] CLI validator accurately reports passes and actionable schema errors for markdown task notes.
- [ ] `templates/task.md`, `templates/weekly-plan.md`, and `templates/daily-timeblock.md` are created and conform to guidelines.
- [ ] `obsidian/snippets/task-cards.css` renders status pills and deep/shallow badges cleanly.
- [ ] `scripts/pre-commit-hook.sh` blocks git commits on invalid staged markdown tasks.
- [ ] Unit tests pass with >80% code coverage.

## 5. Out of Scope
- Direct vault synchronization scripts (deferred to future tracks).
- Automated timeblock scheduling algorithms.
- Proprietary or production task note storage.
