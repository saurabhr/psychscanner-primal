# Using psychscanner-primal

Four different things bring people to this repo. Pick the one that matches what you're actually trying to do — they need different tools, and some of them don't even need this repo installed.

## 1. Just run an existing Hub environment

You don't want to write any code — you want to test a model against a task that's already published, like `psychscanner-rm-encoding`.

You don't need `psychscanner-primal` at all for this. Install the `prime` CLI and run:

```bash
prime eval run psychscanner-rm-encoding -m openai/gpt-4.1-mini -n 8 -r 3
```

See **Prime Intellect Environments Hub** for the full command reference, and **Hub environment tutorial** to see what that environment actually does before you spend money running it.

## 2. Publish your own task to the Hub

You have a new cognitive task in mind and want anyone to be able to run `prime eval run your-task` against it.

`psychscanner-primal` is a **dev-time tool** here, not a runtime dependency of what you publish. The workflow:

1. Author your task as a task card (JSON stimuli/trials) and dry-run it locally against the free `mock-llm` family using `ExpCard`/`ScannerModel` — see **Quickstart** and **Write and run your own task**. This is the fast iteration loop, no `verifiers`, no Hub, no cost. If the trial sequence itself should depend on the model's response (retry, adaptive difficulty), see **Conditional Next Trial**.
2. Once the task card and scoring logic are right, port them into a `verifiers`-based environment module (`environments/<task_name>/<task_name>.py` with a `load_environment()` function) — see **Contributing a task** for the exact folder shape, and **Hub environment tutorial** for a worked example.
3. `prime env push` to publish — see **Prime Intellect Environments Hub**.

One accuracy note: your published environment module does **not** have to `import psychscanner` at runtime. The shipped `psychscanner_rm_encoding.py` example doesn't — it only depends on `verifiers` and `datasets`, reimplementing its own parsing/scoring in plain Python. You *can* import `psychscanner.parsers` or other pieces from this package in your environment module if you want to reuse them, but then you must add `psychscanner-primal` to your environment's own `pyproject.toml` dependencies (as a git dependency, since it isn't on PyPI — see §4).

## 3. Contribute a task card to the task library

This is a **different, smaller thing** than publishing to the Hub, and it has nothing to do with Prime Intellect. [`task_library()`](https://github.com/saurabhr/psychscanner-primal/blob/main/src/psychscanner/task_library.py) is a plain filename-based lookup: anyone using the `psychscanner` Python API can call `task_library("your_task_name")` and get back whichever `your_task_name.json` it finds first, searching in order:

1. A `dirs=` argument passed to the call.
2. Each directory in the `PSYCHSCANNER_TASK_LIBRARY_DIRS` environment variable (`os.pathsep`-separated).
3. `./demonstrations` (relative to the current working directory).
4. `./tasks` (relative to the current working directory) — where this repo's own bundled task cards live, in [`examples/tasks/`](https://github.com/saurabhr/psychscanner-primal/tree/main/examples/tasks).

To contribute a task card for others to reuse this way, there's no PR, no validator, no ledger — you just drop `<your_task_name>.json` into a `demonstrations/` folder (your own, or one shared with a team via `PSYCHSCANNER_TASK_LIBRARY_DIRS`), and it's immediately fetchable by that filename. This is purely about sharing raw task data for local/programmatic use — it carries no reward signal or Hub packaging on its own. If you want the task scored and runnable by the wider world via `prime eval run`, that's §2, not this.

## 4. Install as a developer

`psychscanner-primal` isn't on PyPI — the only supported install path is an editable install from a clone:

```bash
uv venv psyscan-primal --python 3.11
source psyscan-primal/bin/activate

git clone https://github.com/saurabhr/psychscanner-primal.git
cd psychscanner-primal
uv pip install -e .
```

Optional extras, same pattern as any `pyproject.toml` extras group:

```bash
uv pip install -e ".[tests]"       # pytest
uv pip install -e ".[multimodal]"  # beautifulsoup4, httpx
uv pip install -e ".[docs]"        # marimo-book, verifiers, datasets — to build this site
uv pip install -e ".[dev]"         # tests + multimodal together
```

This also installs a `psychscanner-primal` console command (`[project.scripts]` in `pyproject.toml`, wired to `psychscanner.cli:cli`) and, since it's editable, any change you make to `src/psychscanner/` is live immediately — no reinstall needed. Run the test suite with `pytest tests/` from the repo root.
