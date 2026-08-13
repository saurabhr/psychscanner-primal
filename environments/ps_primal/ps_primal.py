"""Paired-associate recall (single-turn proxy) environment.

Derived from psychscanner-primal's pal50.json task card
(https://github.com/saurabhr/psychscanner-primal), a paired-associate
learning paradigm crossing five word-pair semantic-similarity levels
(0.0-1.0). Scores recall accuracy as a function of similarity -- see
README for what's simplified relative to the source task.
"""

import json
from pathlib import Path

import verifiers as vf
from datasets import Dataset

_TASK_FILE = Path(__file__).parent / "pal50.json"

_INSTRUCTIONS = (
    "You will study a word pair, then be asked to recall it.\n\n"
    "STUDY: the word '{word1}' is paired with '{word2}'.\n\n"
    "TEST: what word was paired with '{word1}'? "
    "Respond with only that word, wrapped in <recall>...</recall> tags."
)


def _build_dataset() -> Dataset:
    task = json.loads(_TASK_FILE.read_text())

    # Test-phase items carry the ground-truth pair already (word1/word2),
    # so each row is self-contained -- no separate lookup into the
    # matching *_enc_* item is needed.
    rows = []
    for _, trial_list in task["items"].items():
        trial = trial_list[0] if isinstance(trial_list, list) else trial_list
        if trial.get("phase") != "test":
            continue
        word1, word2 = trial["word1"], trial["word2"]
        rows.append(
            {
                "prompt": _INSTRUCTIONS.format(word1=word1, word2=word2),
                "answer": word2,
                "info": {"trcode": trial["trcode"], "similarity": trial["similarity"]},
            }
        )
    return Dataset.from_list(rows)


def recall_correct(completion, answer, parser: vf.Parser, **kwargs) -> float:
    """1.0 if the recalled word exactly matches the studied pair (case-insensitive)."""
    given = (parser.parse_answer(completion) or "").strip().lower()
    return 1.0 if given == answer.strip().lower() else 0.0


def load_environment(**kwargs) -> vf.Environment:
    """Load the paired-associate recall (single-turn proxy) environment."""
    parser = vf.XMLParser(fields=["recall"], answer_field="recall")
    rubric = vf.Rubric(funcs=[recall_correct], weights=[1.0], parser=parser)

    return vf.SingleTurnEnv(
        dataset=_build_dataset(),
        parser=parser,
        rubric=rubric,
        **kwargs,
    )
