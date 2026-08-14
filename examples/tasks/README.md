# Task Definitions

The feedback-scored task cards carried over from [psychscanner](https://github.com/saurabhr/psychscanner). Fetch any of them by name with `psychscanner.task_library("name")`.

psychscanner-primal only ships tasks that have a real per-trial correct/incorrect signal (`corrAns` on each trial, scored via `psychscanner.feedback.FeedbackBase`) — the property that makes a task usable as an RL/eval reward, e.g. on the [Prime Intellect Environments Hub](https://docs.primeintellect.ai/tutorials-environments/environments). Psychometric surveys (personality inventories, imagery questionnaires) have no ground truth to reward against, so they stay in the main psychscanner package instead of here.

## Files

- `pal50.json` - Paired-associate learning task (50 word pairs, study + test phases)
- `rm_singleturn_demo.json` - Relational-memory task, single-turn trial
- `rm_trialchain_demo.json` - Relational-memory task, chained trials
- `rm_dynamic_demo.json` - Relational-memory task, dynamic encoding/test trials
- `rm_episodic_demo.json` - Relational-memory task, episodic conversation (no feedback)
- `rm_episodic_fb_demo.json` - Relational-memory task, episodic conversation with feedback

N-back working-memory task: use
[`environments/psychscanner_nback/nback_demo.json`](../../environments/psychscanner_nback/nback_demo.json)
instead of adding one here — it's the real, working card (n=1,2,3, pre-baked
history text for `SingleTurnEnv`'s Hub-environment scoring, see that
environment's own README for the schema). A `nback_demo.json` used to live
in this folder too, but it used a different, stale schema that no code in
`src/psychscanner` reads and couldn't actually run; removed rather than left
as a trap.

## Structure

```json
{
    "tasktype": "sc",
    "taskname": "your_task",
    "instructions": {...},
    "items": {...},
    "chain_type": "trial"
}
```

Each trial carries a `corrAns` field; `FeedbackBase.on_response(trial, response)` compares the model's response against it.

## Using These Templates

```python
from psychscanner import ExpCard, ScannerModel

exp_card = ExpCard(
    model="gpt-4o-mini",
    family="openai",
    task_file="examples/tasks/pal50.json",
    projectname="my_study"
)

scanner = ScannerModel(exp_card)
results = scanner.run()
```

## Contributing new cards

New task and experiment cards no longer go through a PR against this folder.
Submit them to [`psyscan-library-primal`](https://github.com/saurabhr/psyscan-library-primal)
instead — the public, versioned index of vetted cards for psychscanner-primal.
Every submission there is validated structurally, checked for duplicates, and
actually run end-to-end against the mock LLM before being merged. See that
repo's `CONTRIBUTING.md` for the steps.

This is separate from packaging a task for the Prime Intellect Hub
(`environments/<name>/`, see the root [`CONTRIBUTING.md`](../../CONTRIBUTING.md))
— that flow is unchanged.
