#!/usr/bin/env python3
"""Task ledger: tracks every environments/<name>/ contribution and flags duplicates.

TASK_LEDGER.json is derived, not hand-edited. Regenerate it after adding or
removing an environments/ folder, and commit the update as part of the PR:

    python scripts/task_ledger.py build

Check a candidate folder (a draft, or a new environments/<name>/) against the
ledger before opening a PR — flags a name that's already taken, or task JSON
that's byte-identical to an existing contribution under a different name:

    python scripts/task_ledger.py check .contrib/drafts/<task_name>
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LEDGER_PATH = REPO_ROOT / "TASK_LEDGER.json"
ENVIRONMENTS_DIR = REPO_ROOT / "environments"


def _content_hash(folder: Path) -> str:
    """Hash the concatenated bytes of every *.json file directly in `folder`, sorted by name."""
    h = hashlib.sha256()
    for jf in sorted(folder.glob("*.json")):
        h.update(jf.name.encode("utf-8"))
        h.update(jf.read_bytes())
    return h.hexdigest()


def build_ledger(environments_dir: Path = ENVIRONMENTS_DIR) -> dict[str, dict]:
    """Scan `environments_dir` and return {task_name: {path, content_hash}}."""
    ledger = {}
    if not environments_dir.is_dir():
        return ledger
    for folder in sorted(p for p in environments_dir.iterdir() if p.is_dir()):
        ledger[folder.name] = {
            "path": str(folder.relative_to(environments_dir.parent)),
            "content_hash": _content_hash(folder),
        }
    return ledger


def find_duplicates(candidate: Path, ledger: dict[str, dict]) -> list[str]:
    """Return warnings if `candidate` collides by name or task-data content with a ledger entry."""
    warnings = []
    candidate_path = candidate.resolve()
    candidate_hash = _content_hash(candidate)

    for existing_name, entry in ledger.items():
        entry_path = (REPO_ROOT / entry["path"]).resolve()
        if entry_path == candidate_path:
            continue  # candidate is this ledger entry itself

        if existing_name == candidate.name:
            warnings.append(f"name '{candidate.name}' is already used by {entry['path']}")
        if candidate_hash == entry["content_hash"]:
            warnings.append(
                f"task data is byte-identical to existing contribution "
                f"'{existing_name}' ({entry['path']})"
            )

    return warnings


def _load_ledger() -> dict[str, dict]:
    if LEDGER_PATH.exists():
        return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    return build_ledger()


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print(__doc__)
        return 2

    cmd, *rest = argv

    if cmd == "build":
        ledger = build_ledger()
        LEDGER_PATH.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"Wrote {len(ledger)} entries to {LEDGER_PATH}")
        return 0

    if cmd == "check":
        if not rest:
            print("usage: task_ledger.py check <folder>")
            return 2
        candidate = Path(rest[0])
        warnings = find_duplicates(candidate, _load_ledger())
        if warnings:
            print(f"DUPLICATE: {candidate} conflicts with existing contribution(s):")
            for w in warnings:
                print(f"  - {w}")
            return 1
        print(f"OK: {candidate} is not a duplicate of any ledgered task.")
        return 0

    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
