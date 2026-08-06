"""Smoke tests for the task ledger: builds correctly, and flags name/content duplicates."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from task_ledger import build_ledger, find_duplicates

ENVIRONMENTS_DIR = Path(__file__).resolve().parent.parent / "environments"


def test_build_ledger_finds_bundled_environment():
    ledger = build_ledger()
    assert "psychscanner_rm_encoding" in ledger
    assert ledger["psychscanner_rm_encoding"]["path"] == "environments/psychscanner_rm_encoding"


def test_no_duplicate_against_its_own_ledger_entry():
    ledger = build_ledger()
    warnings = find_duplicates(ENVIRONMENTS_DIR / "psychscanner_rm_encoding", ledger)
    assert warnings == []


def test_flags_name_collision(tmp_path):
    ledger = build_ledger()
    clash = tmp_path / "psychscanner_rm_encoding"
    clash.mkdir()
    (clash / "other_data.json").write_text('{"unrelated": true}', encoding="utf-8")

    warnings = find_duplicates(clash, ledger)
    assert any("name" in w and "already used" in w for w in warnings)


def test_flags_content_duplicate(tmp_path):
    ledger = build_ledger()
    copy = tmp_path / "psychscanner_rm_encoding_v2"
    copy.mkdir()
    src = ENVIRONMENTS_DIR / "psychscanner_rm_encoding" / "rm_singleturn_demo.json"
    (copy / src.name).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    warnings = find_duplicates(copy, ledger)
    assert any("byte-identical" in w for w in warnings)
