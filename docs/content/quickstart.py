import marimo

__generated_with = "0.23.2"
app = marimo.App()


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Quickstart

        Runs against the built-in `mock-llm` family (no API key, no network),
        so it works out of the box and this page can execute for real at
        build time.

        Swap `model`/`family` for a real provider (see the Supported
        Providers table below) to run against an actual LLM.
        """
    )
    return


@app.cell
def _():
    import tempfile
    from pathlib import Path

    from psychscanner import ExpCard, ExpCardInit, ScannerModel, task_library, to_csv

    task_path = task_library("rm_singleturn_demo", format="path", dirs="../examples/tasks")

    # A fresh temp dir every run: ScannerModel refuses to reuse a proj_dir
    # that already holds a completed session's tunnel file, which a
    # committed results/ dir would trigger on every rebuild.
    proj_dir = Path(tempfile.mkdtemp(prefix="psychscanner_quickstart_"))

    card = ExpCardInit(
        model="mock-llm",
        family="mock-llm",
        projectname="primal_quickstart",
        proj_dir=proj_dir,
        cogtype="no",
        nsim=1,
        memory="SingleTurn",
        task_file=task_path,
    )

    scanner = ScannerModel(expcard=ExpCard(card))
    results = scanner.run()
    return ExpCard, ExpCardInit, ScannerModel, card, results, scanner, task_library, to_csv


@app.cell(hide_code=True)
def _(mo, results):
    mo.md(f"`scanner.run()` returned **{len(results)}** result batch(es).")
    return


@app.cell
def _(card, scanner, to_csv):
    df = to_csv(scanner, path=card.proj_dir)
    df
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Supported providers

        Only `ollama` ships out of the box (`langchain-ollama` is a base
        dependency). Every other family needs its own LangChain integration
        package too, e.g. `uv pip install langchain-openai` for `openai`.

        | Family | Env var |
        |---|---|
        | `openai` | `OPENAI_API_KEY` |
        | `anthropic` | `ANTHROPIC_API_KEY` |
        | `groq` | `GROQ_API_KEY` |
        | `mistral` | `MISTRAL_API_KEY` |
        | `google` / `gemini` | `GOOGLE_API_KEY` |
        | `huggingface` | `HUGGINGFACEHUB_API_TOKEN` |
        | `ollama` | — (local) / `OLLAMA_API_KEY` (remote) |
        """
    )
    return


if __name__ == "__main__":
    app.run()
