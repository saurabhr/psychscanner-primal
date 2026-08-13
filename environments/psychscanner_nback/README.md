# psychscanner-nback

### Overview
- **Environment ID**: `psychscanner-nback`
- **Short description**: N-back working-memory task — judge whether the current letter matches the one shown `n` positions back, from [psychscanner-primal](https://github.com/saurabhr/psychscanner-primal)'s `nback_demo` task card. Replaces `psychscanner-rm-encoding` as the default registered task.
- **Tags**: psychology, cognitive-science, working-memory, single-turn

### Memory levels
Two independent axes, crossed in the bundled dataset:

- **n-back level** (`n`): 1, 2, or 3 — how many letters back the model must compare against. Higher `n` = higher working-memory load.
- **History-quantization condition** (`memory`), mirroring psychscanner's own `memory_k` / `summary_k` (see `docs/guides/memory_types.md` in the main [psychscanner](https://github.com/saurabhr/psychscanner) repo):
  - `conversation` — the trailing `memory_k=5` letters are shown verbatim.
  - `summary` — everything older than `summary_k=10` letters is folded into a per-letter count summary; the most recent `summary_k=10` letters are still shown verbatim.

### Datasets
- **Primary dataset**: `nback_demo.json`, bundled in this package (132 trials: 3 n-levels x 2 memory conditions x ~22 trials each, seeded/deterministic).

### Task
- **Type**: single-turn (each trial's prompt embeds the relevant slice of history per the memory condition above)
- **Output format**: response wrapped in `<answer>match</answer>` / `<answer>no-match</answer>` tags (parsed with `verifiers.XMLParser`)
- **Rubric overview**: one reward function, `nback_correct` — 1.0 if the match/no-match judgment equals the trial's ground truth, else 0.0.

### Quickstart
Run an evaluation with default settings (all n-levels, both memory conditions):

```bash
prime eval run psychscanner-nback
```

Restrict to one n-back level and/or memory condition via env args:

```bash
vf-eval psychscanner_nback --env-args '{"n": 2, "memory": "summary"}' \
  -m openai/gpt-4.1-mini -n 22 -r 3
```

Locally, against a self-hosted OpenAI-compatible endpoint (e.g. Ollama):

```bash
vf-eval psychscanner_nback --provider local \
  --api-base-url http://localhost:11434/v1 --api-key-var OLLAMA_API_KEY \
  -m smollm2:360m-instruct-fp16 -n 22 -r 1
```

### Metrics

| Metric | Meaning |
| ------ | ------- |
| `reward` / `nback_correct` | 1.0 if the match/no-match judgment is correct, else 0.0 |
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
