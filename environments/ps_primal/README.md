# ps-primal

### Overview
- **Environment ID**: `ps-primal`
- **Short description**: Paired-associate recall — score whether a model recalls the correct second word of a studied pair, across five word-pair semantic-similarity levels, from [psychscanner-primal](https://github.com/saurabhr/psychscanner-primal)'s `pal50` task card.
- **Tags**: psychology, cognitive-science, memory, single-turn

### Scope — please read before using results
This environment is a **single-turn proxy** for the real `pal50` paradigm, not a faithful replication:

- **Covered**: for each of the 50 test pairs, does the model recall the correct `word2` given `word1`, when the pair is studied and tested in the same prompt? Results are tagged by `similarity` (0.0–1.0) so accuracy can be compared across interference levels.
- **Not covered — the real design is interleaved and delayed.** In `pal50.json`, all 50 pairs are studied first (encoding phase), then all 50 are tested afterward (test phase), so recall happens after many *other* pairs have intervened — the actual manipulation is memory under interference/delay, not immediate recall. `verifiers` scores each dataset row as an independent single-turn rollout, so this environment collapses study+test into one prompt per item instead. That's a materially easier task than the source paradigm and will likely show higher, less separated-by-similarity accuracy than a real run.
- A faithful port needs `MultiTurnEnv` (study all 50 pairs across turns, then test all 50, preserving conversation state throughout) — left for a follow-up, same as noted in
  [`psychscanner-nback`](https://github.com/saurabhr/psychscanner-primal/tree/main/environments/psychscanner_nback)'s own README for this same task.

If you need the full paradigm, run `pal50.json` directly through [psychscanner-primal](https://github.com/saurabhr/psychscanner-primal)'s `ExpCard`/`ScannerModel` with `memory="Convo"`, `chain_type="trial"` rather than treating this environment's reward as a complete replication.

### Datasets
- **Primary dataset**: `pal50.json`, bundled in this package (100 items: 50 encoding + 50 matching test trials; only the 50 test trials become dataset rows, since each already carries its studied pair). Same file as `psychscanner-primal`'s `examples/tasks/pal50.json`.
- **Source**: [psychscanner-primal/examples/tasks](https://github.com/saurabhr/psychscanner-primal/tree/main/examples/tasks)
- **Split sizes**: 50 train, no separate eval split (dataset doubles as both) — 5 similarity levels x 10 pairs each.

### Task
- **Type**: single-turn
- **Output format**: response wrapped in `<recall>...</recall>` tags (parsed with `verifiers.XMLParser`)
- **Rubric overview**: one reward function, `recall_correct` — 1.0 if the recalled word exactly matches the studied `word2` (case-insensitive), else 0.0.

### Quickstart
Run an evaluation with default settings:

```bash
prime eval run ps-primal
```

Configure model and sampling:

```bash
prime eval run ps-primal -m openai/gpt-4.1-mini -n 10 -r 3
```

Locally, against a self-hosted OpenAI-compatible endpoint (e.g. Ollama):

```bash
vf-eval ps_primal --provider local \
  --api-base-url http://localhost:11434/v1 --api-key-var OLLAMA_API_KEY \
  -m smollm2:360m-instruct-fp16 -n 10 -r 1
```

### Taskset Config

| Field | Type | Default | Description |
| --- | ---- | ------- | ----------- |
| `similarity` (in `info`, not a config field) | float | — | 0.0/0.25/0.50/0.75/1.0 — the semantic-similarity level of each pair, for post-hoc slicing of accuracy by interference level |

### Metrics

| Metric | Meaning |
| ------ | ------- |
| `reward` / `recall_correct` | 1.0 if the recalled word exactly matches the studied pair, else 0.0 (see Scope for why this is easier than the source paradigm) |
| `num_turns` | Always 1.0 — sanity check that this ran as single-turn |

### Citation

This task is derived from psychscanner-primal, itself a slim distribution of [psychscanner](https://github.com/saurabhr/psychscanner). If you use this environment in research, cite the framework paper:

```bibtex
@misc{ranjan2026psychscanner,
      title={Psych Scanner: A Framework for Systematic Cognitive Evaluation of Large Language Models},
      author={Saurabh Ranjan and Konstantina Sokratous and Mukesh Makwana},
      year={2026},
      note={Manuscript submitted for publication},
}
```

Full citation list: [psychscanner-primal/CITATION.cff](https://github.com/saurabhr/psychscanner-primal/blob/main/CITATION.cff).
