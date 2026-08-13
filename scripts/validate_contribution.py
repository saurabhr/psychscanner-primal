#!/usr/bin/env python3
"""Validate a contributed Hub environment folder before opening a PR.

A contribution is a self-contained folder under `environments/<task_name>/`
containing everything needed to run and score the task: the verifiers
Environment module, its pyproject.toml, a README, and the task JSON data
file(s) it depends on — see `environments/psychscanner_nback/` for
a worked example. This script checks that shape locally, before a human
reviewer or the Hub has to.

Usage: python scripts/validate_contribution.py environments/<your_task_name>
"""
from __future__ import annotations

import ast
import json
import sys
import tomllib
from pathlib import Path

from task_ledger import _load_ledger, find_duplicates

REQUIRED_README_SECTIONS = ["overview", "datasets", "task", "quickstart", "metrics", "citation"]


def validate_contribution(folder: Path) -> list[str]:
    """Return validation error messages for `folder`; empty means it's ready for a PR."""
    errors = []
    if not folder.is_dir():
        return [f"{folder} is not a directory"]

    readme = folder / "README.md"
    pyproject = folder / "pyproject.toml"
    py_files = list(folder.glob("*.py"))
    json_files = list(folder.glob("*.json"))

    if not readme.is_file():
        errors.append("missing README.md")
    else:
        text = readme.read_text(encoding="utf-8").lower()
        for section in REQUIRED_README_SECTIONS:
            if section not in text:
                errors.append(f"README.md is missing a '{section.title()}' section")

    if not pyproject.is_file():
        errors.append("missing pyproject.toml")
    else:
        try:
            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as e:
            errors.append(f"pyproject.toml is not valid TOML: {e}")
        else:
            project = data.get("project", {})
            for field in ("name", "description", "version"):
                if not project.get(field):
                    errors.append(f"pyproject.toml [project] is missing '{field}'")
            include = data.get("tool", {}).get("hatch", {}).get("build", {}).get("include", [])
            if not include:
                errors.append("pyproject.toml [tool.hatch.build] is missing an 'include' list")
            for rel in include:
                if not (folder / rel).is_file():
                    errors.append(f"pyproject.toml includes {rel!r} but that file doesn't exist in {folder}")

    if not py_files:
        errors.append("no .py file found (need a verifiers Environment module)")
    else:
        has_load_environment = any(
            isinstance(node, ast.FunctionDef) and node.name == "load_environment"
            for py in py_files
            for node in ast.parse(py.read_text(encoding="utf-8"), filename=str(py)).body
        )
        if not has_load_environment:
            errors.append("no .py file defines a top-level `load_environment` function")

    if not json_files:
        errors.append("no .json task file found")
    else:
        for jf in json_files:
            try:
                json.loads(jf.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                errors.append(f"{jf.name} is not valid JSON: {e}")

    for dup in find_duplicates(folder, _load_ledger()):
        errors.append(f"duplicate: {dup}")

    return errors


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print(__doc__)
        return 2

    folder = Path(argv[0])
    errors = validate_contribution(folder)
    if errors:
        lines = [f"FAIL: {folder} has {len(errors)} issue(s):", *(f"  - {e}" for e in errors)]
    else:
        lines = [f"PASS: {folder} looks ready for a PR."]

    report_dir = Path(".contrib/validate-out")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{folder.name}.log"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("\n".join(lines))
    print(f"(report saved to {report_path})")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
