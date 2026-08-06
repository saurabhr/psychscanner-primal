"""Smoke test for the contribution validator: passes on the bundled RM environment, fails on junk."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from validate_contribution import validate_contribution  # noqa: E402

ENVIRONMENTS_DIR = Path(__file__).resolve().parent.parent / "environments"


def test_validate_passes_on_bundled_environment():
    errors = validate_contribution(ENVIRONMENTS_DIR / "psychscanner_rm_encoding")
    assert errors == []


def test_validate_fails_on_empty_folder(tmp_path):
    errors = validate_contribution(tmp_path)
    assert errors
