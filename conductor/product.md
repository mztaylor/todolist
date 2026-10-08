# Product Definition: todolist

## Vision & Purpose
`todolist` is a decentralized, contract-first task tracking core designed to eliminate vendor lock-in and keep task definitions consistent across isolated environments. It serves as the single source of truth for task schemas, markdown templates, and validation logic across divergent client frontends.

## Target Use Cases & Environments
1. **Work Environment (Obsidian + GitHub):**
   - Air-gapped/isolated from personal notes.
   - Strictly contains corporate/work items.
   - Uses Git sync and Obsidian Dataview/Kanban workflows backed by these standard templates.
2. **Personal Environment (Pixel / Android Client - Future):**
   - Mobile-first capture and personal task management.
   - Validates against the same core task schema without commingling data with work repositories.
3. **Work Web Dashboard (Internal Web UI - Future):**
   - Lightweight browser client consuming tasks via Git or a local-first backend.
   - Form inputs and task states generated directly from the canonical schema.

## Core Boundaries & Responsibilities
- **In Scope:**
  - Canonical JSON Schema (`task.schema.json`) defining required fields (ID, title, status, priority, due dates, tags).
  - Standardized Markdown templates with strict YAML frontmatter.
  - CLI validation and linting tooling to ensure any task file adheres to the contract.
  - Safe sync tooling to distribute templates and configurations into client vaults/repos without sharing private task content.
- **Out of Scope:**
  - Storing actual user tasks, personal notes, or proprietary corporate data (this repo is purely an engine/configuration contract).
  - Hosting a centralized database or shared backend server that blends work and personal networks.

## Target Quality & Operating Principles
- **Schema-First:** Any frontend (Obsidian, Android, Web) must derive or validate its models against the canonical JSON Schema.
- **Offline & Local-First:** All tooling and validations must run offline and via CLI pre-commit hooks.
- **Strict Boundary Isolation:** Zero shared runtime state or credentials between work and personal targets.
