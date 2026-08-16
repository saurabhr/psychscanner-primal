"""N-back working-memory environment.

Sequential letter n-back task: on each trial the model judges whether the
current letter matches the one shown `n` positions back. Ships three memory
loads (n=1,2,3) crossed with two of psychscanner's own history-quantization
conditions (see docs/guides/memory_types.md in the main psychscanner repo):

- conversation: raw trailing window of the last `memory_k=5` letters.
- summary: everything older than `summary_k=10` letters folded into counts,
  raw letters kept for the most recent `summary_k` trials.

Dataset is pre-generated (nback_demo.json) rather than built at import time,
so it's reviewable/diffable like this repo's other task cards.
"""

import json
from pathlib import Path

import verifiers as vf
from datasets import Dataset

_TASK_FILE = Path(__file__).parent / "nback_demo.json"

_INSTRUCTIONS = (
    "You are taking part in an n-back working-memory task. Letters are shown "
    "one at a time. For each new letter, judge whether it is identical to the "
    "letter shown exactly {n} letter(s) earlier in the sequence. "
    "Respond with only your answer, wrapped in <answer>match</answer> or "
    "<answer>no-match</answer> tags."
)


def _build_dataset(n: int | None = None, memory: str | None = None) -> Dataset:
    task = json.loads(_TASK_FILE.read_text())

    rows = []
    for trcode, item in task["items"].items():
        if n is not None and item["n"] != n:
            continue
        if memory is not None and item["memory_mode"] != memory:
            continue

        prompt = (
            f"{_INSTRUCTIONS.format(n=item['n'])}\n\n"
            f"{item['history_text']}\n"
            f"Current letter: {item['letter']}"
        )
        rows.append(
            {
                "prompt": prompt,
                "answer": item["corrAns"],
                "info": {"trcode": trcode, "n": item["n"], "memory_mode": item["memory_mode"]},
            }
        )

    return Dataset.from_list(rows)


def nback_correct(completion, answer, parser: vf.Parser, **kwargs) -> float:
    """1.0 if the match/no-match judgment equals the ground-truth corrAns."""
    given = (parser.parse_answer(completion) or "").strip().lower()
    return 1.0 if given == answer.strip().lower() else 0.0


def load_environment(n: int | None = None, memory: str | None = None, **kwargs) -> vf.Environment:
    """Load the n-back working-memory environment.

    Parameters
    ----------
    n : 1, 2, 3, or None
        Restrict to one n-back memory level; None keeps all three.
    memory : "conversation", "summary", or None
        Restrict to one history-quantization condition; None keeps both.
    """
    parser = vf.XMLParser(fields=["answer"], answer_field="answer")
    rubric = vf.Rubric(funcs=[nback_correct], weights=[1.0], parser=parser)

    return vf.SingleTurnEnv(
        dataset=_build_dataset(n=n, memory=memory),
        parser=parser,
        rubric=rubric,
        **kwargs,
    )
