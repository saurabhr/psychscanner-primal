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
        # Hub environment tutorial

        The **Prime Intellect Environments Hub** page covers the `prime`
        commands. This page is the hands-on complement: it runs the actual
        `psychscanner-nback` environment module, end to end, entirely
        locally — no `prime` account, no API key, no cost. This is exactly
        what `prime env push` uploads and what `prime eval run` executes on
        the Hub; here you can see it work before publishing anything.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 1. Load the pieces `load_environment()` builds

        `psychscanner_nback.load_environment()` wraps a dataset and a
        parser in a `verifiers.SingleTurnEnv` — the object `prime eval run`
        actually drives. That wrapper installs its own SIGINT/SIGTERM
        handlers on construction, which only works on a notebook kernel's
        main thread; this page's cells don't run there, so this tutorial
        builds the same two pieces directly instead, the exact same way
        `load_environment()` does internally. Nothing about the dataset or
        the scoring logic differs — only the final `SingleTurnEnv` wrapping
        step is skipped here.
        """
    )
    return


@app.cell
def _():
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path("../environments/psychscanner_nback").resolve()))
    import psychscanner_nback as nback
    import verifiers as vf

    dataset = nback._build_dataset()
    parser = vf.XMLParser(fields=["answer"], answer_field="answer")
    return dataset, parser, nback


@app.cell(hide_code=True)
def _(dataset, mo):
    mo.md(
        f"Built a dataset with **{len(dataset)}** rows — the same "
        f"`Dataset` object `load_environment()` would hand to "
        f"`SingleTurnEnv`, straight from `nback_demo.json`."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 2. Look at the dataset""")
    return


@app.cell
def _(dataset):
    dataset.to_pandas()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Each row is one trial: a letter sequence position, tagged with its
        n-back level (`n`) and history condition (`memory_mode`, either
        `conversation` — a raw trailing window — or `summary` — older
        letters folded into counts). `answer` carries the ground-truth
        `match` / `no-match` judgment the rubric checks against — it's
        never shown to the model.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 3. Score a completion""")
    return


@app.cell
def _(dataset, parser, nback):
    # Simulating what a model's raw completion would look like for one
    # trial, then scoring it exactly the way the Hub rubric does.
    match_row = next(r for r in dataset if r["answer"] == "match")
    nomatch_row = next(r for r in dataset if r["answer"] == "no-match")

    match_completion = "<answer>match</answer>"
    nomatch_completion = "<answer>no-match</answer>"

    match_score = nback.nback_correct(match_completion, match_row["answer"], parser)
    nomatch_score = nback.nback_correct(nomatch_completion, nomatch_row["answer"], parser)
    return (
        match_completion,
        match_row,
        match_score,
        nomatch_completion,
        nomatch_row,
        nomatch_score,
    )


@app.cell(hide_code=True)
def _(
    match_completion,
    match_score,
    mo,
    nomatch_completion,
    nomatch_score,
):
    mo.md(
        f"""
        | Ground truth | Completion | `nback_correct` |
        |---|---|---|
        | match | `{match_completion}` | **{match_score}** |
        | no-match | `{nomatch_completion}` | **{nomatch_score}** |

        Both score `1.0` — the completion's judgment matches the trial's
        ground truth. Try swapping `match_completion` for
        `<answer>no-match</answer>` and re-run — the score drops to `0.0`.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 4. Ship it

        Everything above ran from the plain Python module in
        `environments/psychscanner_nback/`. Once your own environment
        (see **Contributing a task**) does the same locally, publishing it
        is just:

        ```bash
        cd environments/<your_task_name>
        prime env push
        ```

        See **Prime Intellect Environments Hub** for the full command
        reference — `prime eval run`, costs, and local-only alternatives via
        `vf-eval`.
        """
    )
    return


if __name__ == "__main__":
    app.run()
