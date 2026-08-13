"""CLI smoke test: confirm `psychscanner-primal` actually runs an experiment."""
from pathlib import Path

from click.testing import CliRunner

from psychscanner import task_library
from psychscanner.cli import cli

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
