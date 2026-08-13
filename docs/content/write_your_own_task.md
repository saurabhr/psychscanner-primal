# Write and run your own task

The Quickstart runs a task card that ships with this repo (`rm_singleturn_demo`). This
page is for when you want to run *your own* task or point it at *your own* model —
the two things a new user actually needs, not the bundled demo.

## 1. Write a minimal task card

A task card is a plain dict (or JSON file) — no schema class, no registration. The
smallest one that runs has an `items` dict of trials and a `parser` key (`None` if you
don't want structured output):

```python
task = {
    "tasktype": "sc",
    "taskname": "my_first_task",
    "instructions": {"definition": ["Answer each question briefly."]},
    "contexts": ["general"],
    "contexts_id": ["Q"],
    "context_present": False,
    "items": {
        "Q_1": [{"trcode": "Q_1", "stimulus": "What is 2 + 2?", "corrAns": "4"}],
        "Q_2": [{"trcode": "Q_2", "stimulus": "What color is the sky?", "corrAns": "blue"}],
    },
    "chain_type": "item",
    "parser": None,
}
```

`corrAns` is optional context for your own scoring — psychscanner-primal doesn't grade
it automatically, but it's there in the output for you (or a `FeedbackBase` handler,
see below) to compare against `pred_resp`.

## 2. Dry-run it against `mock-llm`

No API key, no network — good for checking your task card is well-formed before
spending money:

```python
from pathlib import Path
from psychscanner import ExpCard, ExpCardInit, ScannerModel, to_csv

card = ExpCardInit(
    model="mock-llm",
    family="mock-llm",
    task_file=task,          # a dict works directly, no need to write JSON to disk yet
    cogtype="no",
    nsim=1,
    memory="SingleTurn",
    proj_dir=Path("./results"),
    projectname="my_first_task",
)

scanner = ScannerModel(expcard=ExpCard(card))
results = scanner.run()
df = to_csv(scanner, path=card.proj_dir)
```

`results[0]` is a list of per-trial dicts (`trcode`, `pred_resp`, …); `df` is the same
data as a Polars DataFrame, also saved to a timestamped CSV under `proj_dir`.

## 3. Point it at a real model

Swap `model`/`family` — everything else about the task card stays the same. Only
`ollama` ships out of the box; every other family needs its own LangChain integration
package (`uv pip install langchain-openai`, etc.) and its API key env var (see the
table in **Quickstart**):

```python
card = ExpCardInit(
    model="llama3.2",
    family="ollama",
    task_file=task,
    cogtype="no",
    nsim=5,          # run 5 independent participants
    memory="SingleTurn",
    proj_dir=Path("./results"),
    projectname="my_first_task",
)
```

## 4. Move the task card to its own file

Once you're happy with it, save the dict as JSON and point `task_file` at the path
instead — this is what lets you (or a teammate) fetch it later with
`task_library("my_first_task")` instead of hardcoding a path. See **Using
psychscanner-primal** §3 for how `task_library()` resolves names to files.

## 5. Add adaptive branching

If a trial's response should determine what runs next — retry on an invalid answer,
raise/lower difficulty, insert a follow-up probe — see **Conditional Next Trial**.
That mechanism, not a bigger task card, is the right tool once "what runs next"
depends on what the model just said.

## See also

- [Using psychscanner-primal](using_psychscanner_primal.md) — the four different
  things people use this repo for, and which one you actually want
- [Conditional Next Trial](conditional_next_trial.md) — branch the trial sequence
  based on the model's response
- Task JSON schema and multimodal/tool-calling stimuli are documented in full in the
  upstream [psychscanner](https://github.com/saurabhr/psychscanner) docs — the schema
  is identical here, this package just ships fewer bundled task cards
