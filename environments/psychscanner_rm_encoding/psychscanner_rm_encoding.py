"""Reality Monitoring (encoding-phase) environment.

Derived from psychscanner-primal's rm_singleturn_demo.json task card
(https://github.com/saurabhr/psychscanner-primal), part of the Reality
Monitoring paradigm from Ranjan, Sokratous & Odegaard (2026),
arXiv:2607.23927. Scores only the encoding sub-task -- see README for
what's out of scope.
"""

import json
import re
from pathlib import Path

import verifiers as vf
from datasets import Dataset

_TASK_FILE = Path(__file__).parent / "rm_singleturn_demo.json"

_WORD_RE = re.compile(r"^[A-Za-z]+$")

_INSTRUCTIONS = (
    "You are taking part in a word-pair memory task. You will see 'word_1' and 'word_2'. "
    "If 'word_2' is a real word, repeat it back exactly. "
    "If 'word_2' is blank ('________'), imagine a single English word to complete the pair. "
    "The imagined word must not be 'word_1', must not be a compound word, "
    "and must not contain symbols, numbers, or spaces. "
    "Respond with only your answer, wrapped in <word_2>...</word_2> tags."
)


def _build_dataset() -> Dataset:
    task = json.loads(_TASK_FILE.read_text())

    rows = []
    for _, trial_list in task["items"].items():
        trial = trial_list[0] if isinstance(trial_list, list) else trial_list
        pair = trial["stimulus"]["Word_Pair"]
        word_1, word_2 = pair["word_1"], pair["word_2"]
        is_imagined = "_" in word_2

        prompt = (
            f"{_INSTRUCTIONS}\n\n"
            f"word_1: {word_1}\n"
            f"word_2: {'________' if is_imagined else word_2}"
        )
        answer = json.dumps(
            {
                "trial_type": "imagined" if is_imagined else "perceived",
                "word_1": word_1,
                "word_2": None if is_imagined else word_2,
            }
        )
        rows.append(
            {"prompt": prompt, "answer": answer, "info": {"trcode": trial["trcode"]}}
        )

    return Dataset.from_list(rows)


def encoding_correct(completion, answer, parser: vf.Parser, **kwargs) -> float:
    """1.0 if the encoding response is correct for its trial type, else 0.0.

    perceived trials: the response must exactly echo word_2.
    imagined trials: the response must be a single word-shaped token that
    isn't word_1. This is a syntactic proxy for "valid novel English word"
    (no dictionary lookup) and does not check for reuse against other
    trials in the episode -- see README limitations.
    """
    target = json.loads(answer)
    given = (parser.parse_answer(completion) or "").strip()

    if target["trial_type"] == "perceived":
        return 1.0 if given.lower() == target["word_2"].strip().lower() else 0.0

    if not given or not _WORD_RE.match(given):
        return 0.0
    if given.lower() == target["word_1"].strip().lower():
        return 0.0
    return 1.0


def load_environment(**kwargs) -> vf.Environment:
    """Load the Reality Monitoring encoding-phase environment."""
    parser = vf.XMLParser(fields=["word_2"], answer_field="word_2")
    rubric = vf.Rubric(funcs=[encoding_correct], weights=[1.0], parser=parser)

    return vf.SingleTurnEnv(
        dataset=_build_dataset(),
        parser=parser,
        rubric=rubric,
        **kwargs,
    )
