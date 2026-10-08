# Product Guidelines: todolist

## 1. Schema & Data Integrity Standards
- **Contract as Source of Truth:** All frontmatter fields must map directly to `schemas/task.schema.json`. No client may introduce ad-hoc frontmatter keys without updating the canonical schema first.
- **Strict Typing & Enums:** Statuses, priorities, and system tags must use strict string enums (e.g., `status: [backlog, ready, in-progress, review, done]`, `priority: [p1, p2, p3]`). Freeform strings are restricted to descriptions, sub-checklists, and user tags.
- **Deterministic Identifiers:** Every task must require an immutable, machine-readable identifier format (e.g., `^[A-Z]+-[0-9]+$` like `TASK-101` or `WORK-204`).
- **ISO Standard Dates:** All timestamps and scheduling dates (`created_at`, `due`, `completed_at`) must follow ISO 8601 / standard date formatting (`YYYY-MM-DD`).

## 2. Template Architecture & Obsidian Compatibility
- **Frontmatter Cleanliness:** Templates must separate machine-readable metadata in YAML frontmatter (`---`) from human-readable Markdown body text.
- **Dataview & Tasks Plugin Ergonomics:** Structure task body formats and status tags so they are immediately queryable via Dataview (`WHERE status != "done"`) and render cleanly in Obsidian Kanban boards.
- **Zero Platform Lock-in:** Templates must remain valid, legible CommonMark even if opened in a standard terminal pager, raw text editor, or non-Obsidian viewer.

## 3. Environment & Security Boundaries
- **Zero Content Leakage:** The `todolist` repository must NEVER track actual work or personal task files—only schemas, templates, linting scripts, and documentation.
- **Config Distribution Safety:** Sync scripts must push or pull templates destructively only into designated template directories (e.g., `Templates/`), never overwriting user task notes or `.obsidian/workspace.json`.
- **Credential Isolation:** Tooling must rely solely on standard Git environment authentication (SSH keys or local credential helpers); no API tokens or enterprise secrets may be baked into scripts or configurations.

## 4. Tooling & CLI Design Rules
- **Fast Local Validation:** The CLI linter must execute rapidly offline (e.g., sub-second run time) so it functions seamlessly as a Git pre-commit hook.
- **Actionable Error Reporting:** Linting failures must pinpoint the exact file path, offending line, and schema violation rule with clear guidance on how to fix it.
- **Cross-Platform Portability:** Scripts should minimize external dependencies, running cleanly on macOS and Linux environments using standard Python or shell primitives.
