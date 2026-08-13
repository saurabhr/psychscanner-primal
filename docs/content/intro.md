# psychscanner-primal

![logo](../logo.jpeg)

Slim, Hub-optimized distribution of [psychscanner](https://github.com/saurabhr/psychscanner) — a framework for running psychological experiments with large language models.

This package exists as a lightweight dependency for RL/eval tooling such as the [Prime Intellect Environments Hub](https://docs.primeintellect.ai/tutorials-environments/environments): it carries only the tasks that have a real per-trial correct/incorrect signal, so they can be scored as a reward, plus the runtime needed to execute them. It does **not** itself register anything with Prime Intellect or depend on `verifiers` — it's the stable, minimal thing a Hub environment package would import.

!!! tip
    For the full research package — psychometric surveys (BFI-44, VVIQ-16), the LangGraph agent architectures, multimodal/interpretability backends (nnsight, nnterp, VLM), notebooks, and full docs — see [psychscanner](https://github.com/saurabhr/psychscanner).

## What's included

- Core runtime: `ExpCard`/`ExpCardInit`, `ScannerModel`, `TaskRunner`, `FeedbackBase`, `NextTrialBase`, parsers, `task_library`, `SessionTunnel`, `SimulationModel`.
- Multi-provider model calling via LangChain (OpenAI, Anthropic, Groq, Mistral, Google, Ollama, HuggingFace, etc.).
- Only the feedback-scored task cards: Reality Monitoring (`rm_*`) and paired-associate learning (`pal50`).
- `CustomAgent`/`ScanningAgent` adapter protocol, for plugging in your own agent.

## What's excluded

- Psychometric surveys (`bfi44`, `vviq16`, `example_survey`) — no ground truth to score against, so no reward signal.
- The five LangGraph agent architectures.
- Interpretability/multimodal backends: `nnsight_backend`, `nnterp_backend`, `vlm_backend`.

## Installation

```bash
uv venv psyscan-primal --python 3.11
source psyscan-primal/bin/activate

git clone https://github.com/saurabhr/psychscanner-primal.git
cd psychscanner-primal
uv pip install -e .
```

## Next steps

1. See **Quickstart** for a live, runnable example against the built-in `mock-llm` family.
2. See **Write and run your own task** to author a task card from scratch and point it at a real model.
3. See **Conditional Next Trial** to branch the trial sequence adaptively based on the model's response.
4. See **Contributing a task** if you want to add a new cognitive task and release it as a Hub environment.
5. See **Reality Monitoring environment** for the one task already shipped on the Hub.
