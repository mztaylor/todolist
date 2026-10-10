# todolist

> Canonical contract engine, Obsidian templates, and validation CLI for local-first, Newport-aligned task workflows.

`todolist` implements the core contract specification for personal task management aligned with Cal Newport's productivity methodology (*Capture-Configure-Control*, *Multi-Scale Planning*, and *Deep vs. Shallow Work*). It provides a strict JSON Schema Draft 2020-12, Obsidian note templates, visual CSS snippets, a Python CLI validator, and a standalone Git pre-commit hook to maintain contract integrity.

---

## Features

- **Canonical JSON Schema (Draft 2020-12):** Enforces strict types and constraints for task notes (`schemas/task.schema.json`).
  - Required fields: `id` (e.g., `TASK-101`), `title`, `status`, `priority`, `created_at`, `tags`.
  - Newport attributes: `depth` (`deep` vs. `shallow`), `scale` (`daily`, `weekly`, `strategic`), `waiting_on` (for blocked tasks), and `time_estimate_minutes` (`multipleOf: 15`).
- **Python CLI Validator:** High-performance local validator inspecting single notes or recursively scanning vaults.
  - Pinpoints line/field violations with actionable diagnostics.
  - Machine-readable `--json` output and silent CI mode (`--quiet`).
- **Newport-Aligned Obsidian Templates:**
  - `templates/task.md`: Tactical task notes with Dataview-ready checklists.
  - `templates/weekly-plan.md`: Multi-scale planning template with strategic alignment and task pooling.
  - `templates/daily-timeblock.md`: Dual-column layout pairing a Task Queue / Capture pool with a 30-minute Time-Block schedule.
- **Obsidian Styling Snippet:** `obsidian/snippets/task-cards.css` providing visual styling for status pills, priority badges, depth indicators, and timeblock containers.
- **Git Pre-Commit Hook:** Fail-fast script (`scripts/pre-commit-hook.sh`) preventing malformed task notes from entering Git history.

---

## Quickstart & Installation

### Requirements
- Python 3.10+
- Git

### Setup
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies and local package
pip install -r requirements.txt
pip install -e .
```

---

## CLI Usage

Validate a single Markdown task note:
```bash
python -m todolist validate templates/task.md
```

Recursively scan a directory (e.g., templates or Obsidian vault):
```bash
python -m todolist validate templates/
```

### Options & Output Formats

- **Quiet Mode (`--quiet`):** Suppresses output; returns exit code `0` on success and `1` on failure.
  ```bash
  python -m todolist validate templates/ --quiet
  ```

- **JSON Output (`--json`):** Formats results as JSON for pipeline consumption.
  ```bash
  python -m todolist validate templates/ --json
  ```

---

## Obsidian Integration

### 1. Templates
Copy the templates from `templates/` into your Obsidian vault's template folder (e.g., `Templates/`):
- `task.md`: Standard single-task note.
- `weekly-plan.md`: Weekly review and task backlog configuration.
- `daily-timeblock.md`: Daily timeblock planning with dual-column grid.

### 2. CSS Snippets
Copy `obsidian/snippets/task-cards.css` to `.obsidian/snippets/task-cards.css` in your Obsidian vault, then enable it under **Settings > Appearance > CSS snippets**.

---

## Git Pre-Commit Hook

Install the standalone pre-commit hook in your local Git repository:
```bash
# Symlink or copy the hook into .git/hooks
ln -sf ../../scripts/pre-commit-hook.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Whenever you stage `.md` task notes, the hook validates them against `schemas/task.schema.json`. Commits with schema violations will be blocked immediately with actionable feedback.

---

## Testing & Quality Gates

Run the automated test suite with coverage reporting:
```bash
pytest --cov=todolist -v
```

All contributions must maintain >80% test coverage and follow the project style guides in `conductor/code_styleguides/`.
