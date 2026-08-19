# Conditional Next Trial

psychscanner-primal keeps only feedback-scored tasks (see the
[Demonstration Suite](demonstration_suite.md)) — tasks where a trial has a real correct/incorrect signal. That
signal makes adaptive designs a natural fit: retry a trial when the response doesn't
parse, raise or lower difficulty based on accuracy, or insert a follow-up probe — all
decided at run time from the model's actual response, not fixed in the task card
ahead of time.

`next_trial_fn` is the hook for this. After every trial, it's asked whether a new
trial should run *before* the task card's own next one.

## How it works

1. Set `next_trial=True` and provide a `next_trial_fn` class on the card.
2. After each trial, the scanner calls `next_trial_fn.next_trial(trial, response)`.
3. Returning a trial dict (same shape as a task JSON item: `trcode`/`stimulus`,
   optional `fb`/`tools`/`parser`) runs it immediately. Returning `None` moves on to
   the task card's next trial.
4. If the handler proposes the exact same `stimulus` more than `max_repeat` times in a
   row (default 3), the runner stops asking and resumes the task card's own sequence —
   this bounds a handler that would otherwise retry forever.

## Retry once on an unparseable answer

Dry-run this against `mock-llm` first — no API key needed:

```python
from pathlib import Path
from psychscanner import ExpCard, ExpCardInit, NextTrialBase, ScannerModel, to_csv

class RetryOnce(NextTrialBase):
    def __init__(self):
        super().__init__()
        self.retried = set()

    def next_trial(self, trial, response):
        trcode = trial["trcode"]
        if trcode not in self.retried and "retry" not in trcode:
            self.retried.add(trcode)
            return {"trcode": trcode + "_retry", "stimulus": "Please answer again, briefly."}
        return None

task = {
    "tasktype": "sc",
    "taskname": "my_first_task",
    "instructions": {"definition": ["Answer each question briefly."]},
    "contexts": ["general"],
    "contexts_id": ["Q"],
    "context_present": False,
    "items": {"Q_1": [{"trcode": "Q_1", "stimulus": "What is 2 + 2?", "corrAns": "4"}]},
    "chain_type": "task",   # required: the retry needs to see the original question
    "parser": None,
}

card = ExpCardInit(
    model="mock-llm",
    family="mock-llm",
    task_file=task,
    memory="Convo",         # required: same reason as chain_type="task"
    chain_type="task",
    cogtype="no",
    nsim=1,
    proj_dir=Path("./results"),
    projectname="my_first_task_nt",
    next_trial=True,
    next_trial_fn=RetryOnce,
)

scanner = ScannerModel(expcard=ExpCard(card))
results = scanner.run()
to_csv(scanner, path=card.proj_dir)
```

`results[0]` now has two rows — `Q_1` and `Q_1_retry` — instead of one.

## Adaptive difficulty from `corrAns`

Since primal's tasks carry `corrAns`, a handler can score the response itself and
branch on correctness — no separate `FeedbackBase` needed unless you also want text
injected into the conversation:

```python
class Staircase(NextTrialBase):
    def __init__(self):
        super().__init__()
        self.level = 1

    def next_trial(self, trial, response):
        correct = str(response.get("content", "")).strip() == str(trial.get("corrAns"))
        new_level = min(self.level + 1, 5) if correct else max(self.level - 1, 1)
        if new_level == self.level:
            return None  # no change, let the task card continue
        self.level = new_level
        return {"trcode": f"stair_{self.level}", "stimulus": f"Difficulty level {self.level} item"}
```

Like `FeedbackBase`, the handler is instantiated once per participant simulation, so
`__init__` state (`self.level`, `self.retried`) is safe to keep across trials.

## Required card settings

| Parameter | Required value |
|-----------|---------------|
| `next_trial` | `True` |
| `next_trial_fn` | Your `NextTrialBase` subclass (class, not instance) |

Inserted trials inherit `context_present`/`context_item`/`tasktype` from the trial
they follow unless you override them explicitly in the returned dict.

## See also

- [Write and run your own task](write_your_own_task.md) — the task-card basics this
  page builds on
- The equivalent mechanism for injecting text feedback rather than branching the trial
  sequence is `FeedbackBase` — see the `on_response`/`inject_feedback` docstrings in
  `psychscanner.feedback.feedback_base`
