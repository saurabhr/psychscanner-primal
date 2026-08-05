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
