"""CLI entry point for task schema validation."""

import argparse
import json
from pathlib import Path
import sys
from typing import List, Optional

from todolist.validator import ValidationResult, validate_task_file


def collect_target_files(target: Path) -> List[Path]:
    """Collects markdown files from a file or directory path.

    Args:
        target: Target file or directory path.

    Returns:
        List of Path objects representing markdown files.
    """
    if target.is_file():
        return [target] if target.suffix.lower() == ".md" else []
    if target.is_dir():
        return sorted([p for p in target.rglob("*.md") if p.is_file()])
    return []


def run_validation(
    paths: List[Path], schema_path: Optional[Path] = None
) -> List[ValidationResult]:
    """Runs validation on a list of markdown file paths.

    Args:
        paths: List of file paths to validate.
        schema_path: Optional custom schema path.

    Returns:
        List of ValidationResult objects.
    """
    return [validate_task_file(p, schema_path=schema_path) for p in paths]


def format_text_output(results: List[ValidationResult]) -> str:
    """Formats validation results as human-readable text.

    Args:
        results: List of ValidationResult objects.

    Returns:
        Formatted multi-line string.
    """
    lines: List[str] = []
    for r in results:
        status_tag = "PASSED" if r.is_valid else "FAILED"
        lines.append(f"[{status_tag}] {r.file_path}")
        if not r.is_valid:
            for err in r.errors:
                lines.append(f"  - {err}")
    total = len(results)
    passed = sum(1 for r in results if r.is_valid)
    failed = total - passed
    lines.append("-" * 40)
    lines.append(f"Summary: {total} files inspected | {passed} passed | {failed} failed")
    return "\n".join(lines)


def format_json_output(results: List[ValidationResult]) -> str:
    """Formats validation results as structured JSON string.

    Args:
        results: List of ValidationResult objects.

    Returns:
        JSON-encoded string.
    """
    total = len(results)
    passed = sum(1 for r in results if r.is_valid)
    failed = total - passed

    payload = {
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "all_valid": failed == 0,
        },
        "results": [
            {
                "file": str(r.file_path),
                "valid": r.is_valid,
                "errors": r.errors,
            }
            for r in results
        ],
    }
    return json.dumps(payload, indent=2)


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI execution entry point.

    Args:
        argv: Optional list of command line arguments. Defaults to sys.argv[1:].

    Returns:
        Exit code: 0 for all valid, 1 for validation failures, 2 for bad arguments.
    """
    parser = argparse.ArgumentParser(
        prog="todolist",
        description="Local-first task schema validator and contract engine.",
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Available commands")

    validate_parser = subparsers.add_parser(
        "validate", help="Validate task markdown files against canonical schema"
    )
    validate_parser.add_argument(
        "target",
        type=str,
        help="Path to a markdown file or directory to validate",
    )
    validate_parser.add_argument(
        "--schema",
        type=str,
        default=None,
        help="Optional path to custom JSON schema file",
    )
    validate_parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress output unless errors are detected",
    )
    validate_parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Format output as JSON",
    )

    args = parser.parse_args(argv)

    if args.subcommand != "validate":
        parser.print_help()
        return 2

    target_path = Path(args.target)
    if not target_path.exists():
        sys.stderr.write(f"Error: Target path does not exist: {target_path}\n")
        return 2

    files_to_validate = collect_target_files(target_path)
    if not files_to_validate:
        if not args.quiet:
            sys.stdout.write(f"No markdown (.md) files found at {target_path}\n")
        return 0

    schema_override = Path(args.schema) if args.schema else None
    results = run_validation(files_to_validate, schema_path=schema_override)
    all_passed = all(r.is_valid for r in results)

    if args.json_output:
        sys.stdout.write(format_json_output(results) + "\n")
    elif not args.quiet or not all_passed:
        output = format_text_output(results)
        if all_passed:
            sys.stdout.write(output + "\n")
        else:
            sys.stdout.write(output + "\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
