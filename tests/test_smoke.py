"""Smoke test: confirm the trimmed package still runs a bundled RM task end to end."""
from pathlib import Path

from psychscanner import ExpCard, ExpCardInit, ScannerModel, task_library, to_csv

TASKS_DIR = Path(__file__).resolve().parent.parent / "examples" / "tasks"


def test_rm_singleturn_runs_with_mock_llm(tmp_path):
    task_path = task_library("rm_singleturn_demo", format="path", dirs=TASKS_DIR)

    card = ExpCardInit(
        model="mock-llm",
        family="mock-llm",
        projectname="smoke",
        proj_dir=tmp_path,
        cogtype="no",
        nsim=1,
        memory="SingleTurn",
        task_file=task_path,
    )

    scanner = ScannerModel(expcard=ExpCard(card))
    results = scanner.run()
    assert results, "expected at least one trial result"

    df = to_csv(scanner, path=tmp_path)
    assert len(df) > 0, "expected at least one row in the exported CSV"
