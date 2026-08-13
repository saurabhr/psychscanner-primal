# Prime Intellect Environments Hub

If you've never heard of this, you're the audience for this page. Everything else in these docs assumes you'll eventually run something through it, so here's what it actually is.

## What it is

The [Environments Hub](https://app.primeintellect.ai/dashboard/environments) is a public catalog of packaged tasks for evaluating and training LLMs — reinforcement learning environments and agent evals, in one place. Someone packages a task (dataset + scoring rule) as a small Python module, publishes it to the Hub, and from then on anyone can run any model against it with one command, without reading that person's code.

Under the hood, every Hub environment is built on [`verifiers`](https://github.com/PrimeIntellect-ai/verifiers) — a small framework for exactly this: a dataset, a parser for the model's output, and a rubric (reward function) that scores it. That's what `environments/psychscanner_nback/psychscanner_nback.py` in this repo is — a `verifiers` environment, ready to push to the Hub.

This is the reason `psychscanner-primal` exists as a separate, slim package in the first place (see the [Home](index.md) page): it's the minimal runtime a Hub environment needs to import, stripped of everything (surveys, agent architectures, interpretability backends) that doesn't carry a reward signal.

## Install the CLI

```bash
uv tool install prime
# or: pip install prime
```

Then authenticate:

```bash
prime login
```

(Or set a key manually with `prime config set-api-key` — see the [API keys reference](https://docs.primeintellect.ai/api-reference/api-keys).)

## Running an eval against an existing environment

This is the common case: someone else already published an environment (like this repo's `psychscanner-nback`), and you want to test a model against it.

```bash
prime eval run psychscanner-nback -m openai/gpt-4.1-mini -n 8 -r 3
```

- `-m / --model` — which model to test (default `openai/gpt-4.1-mini`)
- `-n / --num-examples` — how many dataset rows to sample (default 5)
- `-r / --rollouts-per-example` — repeats per row, for statistical noise (default 3)

!!! warning
    This spends real money/credits — it's an actual inference call per rollout. Start with a small `-n`/`-r` and a cheap model.

To use your own model provider's key instead of Prime's billing, point at the provider directly:

```bash
prime eval run psychscanner-nback \
  --api-base-url https://api.openai.com/v1 --api-key-var OPENAI_API_KEY \
  -m gpt-4.1-mini -n 8 -r 3
```

To run fully locally against Ollama (no Hub, no billing at all) — this is what `environments/psychscanner_nback/README.md`'s own Quickstart documents:

```bash
vf-eval psychscanner_nback --provider local \
  --api-base-url http://localhost:11434/v1 --api-key-var OLLAMA_API_KEY \
  -m smollm2:360m-instruct-fp16 -n 8 -r 1
```

## Publishing a new environment

This is the other direction — you built a new task (see **Contributing a task**) and want it runnable by anyone via `prime eval run`.

```bash
prime login
cd environments/<your_task_name>
prime env push
```

Common flags:

- `--team <team-username>` — publish under a team account instead of yours
- `--visibility=PRIVATE` — keep it unlisted
- `--auto-bump` — auto-increment the version on repeat pushes

Once pushed, anyone can install and run it:

```bash
prime env install <your-username>/<your_task_name>
prime eval run <your-username>/<your_task_name>
```

The **Contributing a task** page covers everything before this point — folder shape, local validation, the duplicate-checking ledger, and the PR process. `prime env push` is the last step, done after your PR is merged.
