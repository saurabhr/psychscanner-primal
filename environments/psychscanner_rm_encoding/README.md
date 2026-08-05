# psychscanner-rm-encoding

### Overview
- **Environment ID**: `psychscanner-rm-encoding`
- **Short description**: Reality Monitoring (encoding phase) — score whether a model correctly echoes a perceived word or generates a valid novel word for an imagined one, from [psychscanner-primal](https://github.com/saurabhr/psychscanner-primal)'s `rm_singleturn_demo` task card.
- **Tags**: psychology, cognitive-science, memory, single-turn

### Scope — please read before using results
This environment scores **only the encoding sub-task**, not the full Reality Monitoring paradigm from Ranjan, Sokratous & Odegaard (2026) ([arXiv:2607.23927](https://arxiv.org/abs/2607.23927)):

- **Covered**: for each trial, was the response the exact perceived word (`perceived` trials), or a plausible novel word (`imagined` trials)?
- **Not covered**: the actual source-monitoring judgment (did the model correctly classify a word as self-generated vs. externally-provided) and confidence rating — the part the paper is actually about. There's no documented, unambiguous ground-truth rule for scoring that sub-task yet, so it isn't implemented here rather than guessed at.
- **"Valid novel word" is a syntactic proxy**, not a dictionary check: a single alphabetic token that isn't `word_1`. No lexicon lookup.
- **No cross-trial novelty tracking.** The reference implementation in psychscanner-primal (`FeedbackBase`-based `RMEncodingFeedback`) tracks reused words across an entire participant session. verifiers scores each dataset row as an independent rollout, so that cross-trial state isn't reproduced here — each trial is judged only against `word_1` and the task's own per-trial constraints (not a compound word, no symbols/numbers).
- `pal50` (paired-associate recall) is not yet ported — it's an interleaved 100-trial episodic design (study/test phases separated by many other trials), which needs `MultiTurnEnv` rather than `SingleTurnEnv`. Left for a follow-up.

If you need the full paradigm, use [psychscanner-primal](https://github.com/saurabhr/psychscanner-primal) directly rather than treating this environment's reward as a complete replication.

### Datasets
- **Primary dataset**: `rm_singleturn_demo.json`, bundled in this package (8 trials: 4 `perceived`, 4 `imagined`). Same file as `psychscanner-primal`'s `examples/tasks/rm_singleturn_demo.json`.
- **Source**: [psychscanner-primal/examples/tasks](https://github.com/saurabhr/psychscanner-primal/tree/main/examples/tasks)
- **Split sizes**: 8 train, no separate eval split (dataset doubles as both).

### Task
- **Type**: single-turn
- **Output format**: response wrapped in `<word_2>...</word_2>` tags (parsed with `verifiers.XMLParser`)
- **Rubric overview**: one reward function, `encoding_correct` — 1.0 if the response satisfies its trial type's correctness rule (see Scope above), else 0.0.

### Quickstart
Run an evaluation with default settings:

```bash
prime eval run psychscanner-rm-encoding
```

Configure model and sampling:

```bash
prime eval run psychscanner-rm-encoding -m openai/gpt-4.1-mini -n 8 -r 3
```

Locally, against a self-hosted OpenAI-compatible endpoint (e.g. Ollama):

```bash
vf-eval psychscanner_rm_encoding --provider local \
  --api-base-url http://localhost:11434/v1 --api-key-var OLLAMA_API_KEY \
  -m smollm2:360m-instruct-fp16 -n 8 -r 1
```

### Metrics

| Metric | Meaning |
| ------ | ------- |
| `reward` / `encoding_correct` | 1.0 if the encoding response is correct for its trial type, else 0.0 (see Scope) |
| `num_turns` | Always 1.0 — sanity check that this ran as single-turn |

### Citation

This task is derived from psychscanner-primal, itself a slim distribution of [psychscanner](https://github.com/saurabhr/psychscanner). If you use this environment in research, cite:

```bibtex
@misc{ranjan2026reality,
      title={Reality Monitoring in Large Language Models: Self-Knowledge That Transforms with Conversation Memory},
      author={Saurabh Ranjan and Konstantina Sokratous and Brian Odegaard},
      year={2026},
      eprint={2607.23927},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2607.23927},
}
```

Full citation list: [psychscanner-primal/CITATION.cff](https://github.com/saurabhr/psychscanner-primal/blob/main/CITATION.cff).
