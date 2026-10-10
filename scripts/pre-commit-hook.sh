#!/usr/bin/env bash
# Standalone Git Pre-Commit Hook: Validates staged markdown task notes against schemas/task.schema.json.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# 1. Resolve Python executable
if [ -n "${VIRTUAL_ENV:-}" ] && [ -x "$VIRTUAL_ENV/bin/python" ]; then
  PYTHON="$VIRTUAL_ENV/bin/python"
elif [ -x "$REPO_ROOT/.venv/bin/python" ]; then
  PYTHON="$REPO_ROOT/.venv/bin/python"
elif [ -x ".venv/bin/python" ]; then
  PYTHON=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON="python"
else
  echo "[todolist-hook] ERROR: Python runtime not found." >&2
  exit 1
fi

export PYTHONPATH="${REPO_ROOT}:${PYTHONPATH:-}"

# 2. Collect candidate files to validate
FILES=()
if [ "$#" -gt 0 ]; then
  FILES=("$@")
else
  while IFS= read -r file; do
    [ -z "$file" ] && continue
    # Only consider .md files
    if [[ "$file" == *.md ]]; then
      # Validate if file is in templates/ or tasks/ or begins with YAML frontmatter containing an id: field
      if [[ "$file" == templates/* ]] || [[ "$file" == tasks/* ]]; then
        FILES+=("$file")
      elif [ -f "$file" ]; then
        if head -n 1 "$file" | grep -q '^---$'; then
          # Check if frontmatter contains an id or status property
          if sed -n '2,/^---$/p' "$file" | grep -q -E '^[[:space:]]*(id|status):'; then
            FILES+=("$file")
          fi
        fi
      fi
    fi
  done < <(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || true)
fi

if [ "${#FILES[@]}" -eq 0 ]; then
  exit 0
fi

echo "[todolist-hook] Inspecting ${#FILES[@]} markdown file(s) for schema compliance..."

FAILED=0
for target in "${FILES[@]}"; do
  if [ ! -f "$target" ]; then
    continue
  fi

  if ! "$PYTHON" -m todolist validate "$target"; then
    FAILED=1
  fi
done

if [ "$FAILED" -ne 0 ]; then
  echo "" >&2
  echo "[todolist-hook] Commit rejected: task schema validation errors found." >&2
  echo "[todolist-hook] Please resolve the errors above or fix frontmatter before committing." >&2
  exit 1
fi

echo "[todolist-hook] All staged task notes are valid."
exit 0
