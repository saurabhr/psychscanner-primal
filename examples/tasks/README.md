# Task Definitions

The feedback-scored task cards carried over from [psychscanner](https://github.com/saurabhr/psychscanner). Fetch any of them by name with `psychscanner.task_library("name")`.

psychscanner-primal only ships tasks that have a real per-trial correct/incorrect signal (`corrAns` on each trial, scored via `psychscanner.feedback.FeedbackBase`) — the property that makes a task usable as an RL/eval reward, e.g. on the [Prime Intellect Environments Hub](https://docs.primeintellect.ai/tutorials-environments/environments). Psychometric surveys (personality inventories, imagery questionnaires) have no ground truth to reward against, so they stay in the main psychscanner package instead of here.

## Files

- `nback_demo.json` - N-back working-memory task (n=1,2,3 routines), default task card — run with `memory="Convo"` (`memory_k=5` for conversation memory, or add `summary_k=10` for summary memory)
- `pal50.json` - Paired-associate learning task (50 word pairs, study + test phases)
- `rm_singleturn_demo.json` - Relational-memory task, single-turn trial
- `rm_trialchain_demo.json` - Relational-memory task, chained trials
- `rm_dynamic_demo.json` - Relational-memory task, dynamic encoding/test trials
- `rm_episodic_demo.json` - Relational-memory task, episodic conversation (no feedback)
- `rm_episodic_fb_demo.json` - Relational-memory task, episodic conversation with feedback
- `introspection_weights_demo.json` - Multi-attribute 2AFC choice task (10 simulated agents x 6 trials), adapted from Plunkett et al. (2025)'s LLM self-interpretability paradigm; see [psychscanner's `07_introspective_selfreport` demo](https://github.com/saurabhr/psychscanner/tree/main/examples/demonstration_suite/07_introspective_selfreport). Each trial's `corrAns` is the option the simulated agent's (randomly-generated, in-context-instilled) attribute weights actually favor. The introspective self-report half of that demo has no scalar ground truth to score, so it's intentionally not included here.

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
