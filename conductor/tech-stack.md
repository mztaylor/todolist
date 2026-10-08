# Tech Stack & Architecture: todolist

## 1. Core Data Contract & Schemas
- **Specification:** JSON Schema (Draft 2020-12)
- **Role:** Single source of truth for all task attributes, types, enums, and required fields across all clients.
- **Location:** `schemas/task.schema.json`

## 2. Validation & Tooling Engine
- **Runtime:** Python 3.10+ (macOS & Linux compatible)
- **Dependencies:**
  - `jsonschema` (Draft 2020-12 validation engine)
  - `python-frontmatter` (YAML frontmatter and CommonMark parsing)
  - `pyyaml` (Underlying YAML parser)
- **Packaging / Execution:** Standard virtual environment (`venv`) with `requirements.txt` or lightweight `pyproject.toml`.
- **Git Hooks:** Standalone shell pre-commit hook (`scripts/pre-commit-hook.sh`) executing the Python validator with fast fail-fast exits.

## 3. Template & Sync Formats
- **Note Formatting:** CommonMark with YAML frontmatter.
- **Client Integrations:**
  - **Obsidian Work Vault:** Obsidian Dataview, Tasks plugin, and Kanban plugin compatibility.
  - **Vault Sync Tool:** Bash/POSIX shell script (`scripts/sync_to_vault.sh`) leveraging Git sparse-checkout or direct file copy to push/pull templates into target vaults without touching active task notes.

## 4. Downstream Target Clients (Future Interop Contracts)
- **Work Web Dashboard:**
  - Target model consumption via JSON Schema-to-Zod / Pydantic generators.
- **Pixel / Android Client:**
  - Target model consumption via JSON Schema-to-Kotlin data classes (`kotlinx.serialization`).
