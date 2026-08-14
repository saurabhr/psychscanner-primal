"""CLI smoke test: confirm `psychscanner-primal` actually runs an experiment."""
from pathlib import Path

import pytest
from click.testing import CliRunner

from psychscanner import task_library
from psychscanner.cli import (
    _parse_bool_or_none,
    _parse_csv_option,
    _parse_json_option,
    cli,
)

TASKS_DIR = Path(__file__).resolve().parent.parent / "examples" / "tasks"


def test_cli_runs_experiment_with_mock_llm(tmp_path):
    task_path = task_library("rm_singleturn_demo", format="path", dirs=TASKS_DIR)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "-m", "mock-llm",
            "-f", "mock-llm",
            "-projname", "cli_smoke",
            "-pd", str(tmp_path),
            "-t", str(task_path),
        ],
    )

    assert result.exit_code == 0, result.output
    assert "Ran 1 result batch" in result.output

    csv_files = list(tmp_path.rglob("*.csv"))
    assert csv_files, f"expected a saved CSV under {tmp_path}, got: {result.output}"


# ── Regression tests for click option callbacks ──────────────────────────────
# type=dict/type=list[str]/type=click.Choice([True, False, None]) on a
# click.Option don't parse CLI strings the way their type hints suggest --
# these callbacks replace them. -p/-pcon crashed on any real JSON input,
# -tg/-pers silently exploded a comma-separated string into single
# characters, and -tc's non-string Choice values crashed --help itself
# under this repo's pinned Click version.


def test_parse_json_option_parses_real_json() -> None:
    assert _parse_json_option(None, None, '{"temperature": 0.5}') == {"temperature": 0.5}


def test_parse_json_option_none_on_empty() -> None:
    assert _parse_json_option(None, None, None) is None
    assert _parse_json_option(None, None, "") is None


def test_parse_json_option_rejects_invalid_json() -> None:
    import click

    with pytest.raises(click.BadParameter):
        _parse_json_option(None, None, "{not json}")


def test_parse_csv_option_splits_on_commas() -> None:
    assert _parse_csv_option(None, None, "a,b,c") == ["a", "b", "c"]
    assert _parse_csv_option(None, None, "a, b , c") == ["a", "b", "c"]


def test_parse_csv_option_none_on_empty() -> None:
    assert _parse_csv_option(None, None, None) is None
    assert _parse_csv_option(None, None, "") is None


def test_parse_bool_or_none_maps_choices() -> None:
    assert _parse_bool_or_none(None, None, "true") is True
    assert _parse_bool_or_none(None, None, "false") is False
    assert _parse_bool_or_none(None, None, "none") is None
    assert _parse_bool_or_none(None, None, None) is None


def test_cli_help_does_not_crash() -> None:
    """Regression: click.Choice([True, False, None]) crashed --help itself
    under this repo's pinned Click version (get_metavar joining non-strings)."""
    result = CliRunner().invoke(cli, ["--help"])
    assert result.exit_code == 0, result.output


def test_cli_accepts_json_and_csv_and_choice_flags(tmp_path: Path) -> None:
    """End-to-end: -p/-tg/-tc used to crash or silently corrupt input."""
    task_path = task_library("rm_singleturn_demo", format="path", dirs=TASKS_DIR)

    result = CliRunner().invoke(
        cli,
        [
            "-m", "mock-llm",
            "-f", "mock-llm",
            "-projname", "cli_flags_smoke",
            "-pd", str(tmp_path),
            "-t", str(task_path),
            "-p", '{"temperature": 0.5}',
            "-tg", "a,b,c",
            "-tc", "false",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "Ran 1 result batch" in result.output
