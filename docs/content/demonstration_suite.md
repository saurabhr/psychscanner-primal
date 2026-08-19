# Demonstration Suite

psychscanner-primal doesn't ship its own multi-experiment demonstration
suite — it's the slim, Hub-optimized distribution (see [Using
psychscanner-primal](using_psychscanner_primal.md)). For real, run
demonstrations of the underlying task/agent machinery, see
[psychscanner](https://github.com/saurabhr/psychscanner)'s
[`examples/demonstration_suite/`](https://github.com/saurabhr/psychscanner/tree/main/examples/demonstration_suite)
(rendered at
[saurabhr.github.io/psychscanner/examples/demonstration_suite/](https://saurabhr.github.io/psychscanner/examples/demonstration_suite/)):

1. **Reward Task** — swapping agents into the same task harness. Complete.
2. **Association Memory** — trial structures and feedback types. Skeleton.
3. **Personality Survey** — persona conditioning, stateful memory. VVIQ-16 arm complete.
4. **VLM Task** — the same machinery on vision-language models. Partial.
5. **Extracting Internals** — activation extraction and steering. Skeleton.
6. **Advanced Demonstration** — Othello-GPT, ROME, CCS. Othello-GPT complete.
7. **Introspective Self-Report** — instilled preferences + self-report, with a
   psychscanner-primal integration point (see below). Complete.
8. **Prospect Theory Planning** — risky-choice gambles, 3 agent architectures. Complete.

## The one with a primal integration

[`07_introspective_selfreport`](https://github.com/saurabhr/psychscanner/blob/main/examples/demonstration_suite/07_introspective_selfreport/readme.md)
is the only demo that touches this package directly: its decision trials
(the part with a real per-trial correct/incorrect signal — this package's
own inclusion bar) are meant to ship as a standalone task card,
`examples/tasks/introspection_weights_demo.json`, built by that demo's
`simulation/build_primal_task_card.py` and runnable through this package's
own `ExpCard`/`ScannerModel`/`task_library` pattern (see [Using
psychscanner-primal](using_psychscanner_primal.md)). **That file is not
currently present in this repo's `examples/tasks/`** (checked 2026-08-19) —
re-run the build script in the psychscanner repo if you need it here.

## What this package ships instead

The task cards actually bundled in `examples/tasks/` (`rm_*`, `pal50`) are
narrower than the demonstration suite above — single feedback-scored task
cards, not full multi-condition studies. See
[Using psychscanner-primal](using_psychscanner_primal.md) and
[`examples/tasks/README.md`](https://github.com/saurabhr/psychscanner-primal/blob/main/examples/tasks/README.md)
for what's here and how to run it.
