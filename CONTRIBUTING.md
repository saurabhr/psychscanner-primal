# Contributing a task

A contribution is a self-contained folder under `environments/<task_name>/` with everything needed to run and score the task — modeled on the existing [`environments/psychscanner_nback/`](https://github.com/saurabhr/psychscanner-primal/tree/main/environments/psychscanner_nback), which is the reference example to copy from:

```
environments/<task_name>/
├── <task_name>.py       # verifiers Environment: must define load_environment()
├── pyproject.toml       # hatchling build, [tool.hatch.build] include list, verifiers metadata
├── <task_name>.json     # task data (stimuli/trials) — one or more JSON files
└── README.md            # Overview, Datasets, Task, Quickstart, Metrics, Citation sections
```

There's no requirement to reuse the Reality Monitoring or PAL50 scoring logic — a contribution can define its own trial data, its own parser, and its own correct/incorrect rule in `<task_name>.py`, as long as it's an honest, documented reward signal (see the "Scope" section of the psychscanner_nback README for how to be upfront about what a proxy metric does and doesn't cover).

Not the same thing as [`task_library()`](https://github.com/saurabhr/psychscanner-primal/blob/main/src/psychscanner/task_library.py): that's a runtime lookup for a bare task-card JSON (stimuli only), used from Python code via the `psychscanner` API. This workflow is for a full packaged, scored environment meant to ship on the Hub.

## Build it as a draft first

`.contrib/` is gitignored — never committed, never shows up in `git status`. Build and iterate on your task folder at `.contrib/drafts/<task_name>/` until it's ready, then move it to `environments/<task_name>/` for the PR:

```bash
mkdir -p .contrib/drafts/<task_name>
# ...build the folder above under .contrib/drafts/<task_name>/...
mv .contrib/drafts/<task_name> environments/<task_name>
```

## Validate locally before opening a PR

```bash
python scripts/validate_contribution.py environments/<task_name>
# or, while still drafting:
python scripts/validate_contribution.py .contrib/drafts/<task_name>
```

This checks the folder shape (required files present), that `pyproject.toml` is valid TOML with the fields Hub packaging expects, that your `.py` module defines `load_environment`, that every task JSON file parses, **and that it isn't a duplicate** (see below). It won't catch scoring-logic bugs — write real trials through it and check the rewards by hand before submitting. Every run also writes its pass/fail report to `.contrib/validate-out/<task_name>.log`.

Requires Python 3.11+ (uses `tomllib`).

## Task ledger — avoiding duplicate contributions

`TASK_LEDGER.json` (repo root, committed) records every `environments/<name>/` folder by task name and a content hash of its task JSON. It's derived, not hand-edited. `validate_contribution.py` checks against it automatically, flagging:

- **Name collision** — another environment already uses `<task_name>`.
- **Content duplicate** — your task JSON is byte-identical to an existing contribution under a different name.

You can also check a draft on its own, before it's even in `environments/`:

```bash
python scripts/task_ledger.py check .contrib/drafts/<task_name>
```

Once your folder is in `environments/<task_name>/` and validation passes, regenerate the ledger and commit the updated file as part of your PR:

```bash
python scripts/task_ledger.py build
```

If you're flagged but believe it's a false positive — a genuine, independent task that happens to share stimuli or a name with an existing one — don't work around the check. [Open an issue](https://github.com/saurabhr/psychscanner-primal/issues) explaining why, and a maintainer will sort it out with you.

## Releasing on the Hub

1. Open a PR against this repo with your `environments/<task_name>/` folder (and the regenerated `TASK_LEDGER.json`). A maintainer reviews the scoring logic and scope claims.
2. Once merged, publish it to the Prime Intellect Environments Hub yourself with the `prime` CLI from inside your environment folder (`prime env push`) — this repo doesn't automate that step. New to the Hub? See [Prime Intellect Environments Hub](https://github.com/saurabhr/psychscanner-primal/blob/main/docs/content/prime_intellect_hub.md) in this repo's docs for a plain-language walkthrough of `prime env push` / `prime eval run`, or the [official Hub docs](https://docs.primeintellect.ai/tutorials-environments/environments) for the full reference.
