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
        `psychscanner-rm-encoding` environment module, end to end, entirely
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

        `psychscanner_rm_encoding.load_environment()` wraps a dataset and a
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

    sys.path.insert(0, str(Path("../environments/psychscanner_rm_encoding").resolve()))
    import psychscanner_rm_encoding as rm_encoding
    import verifiers as vf

    dataset = rm_encoding._build_dataset()
    parser = vf.XMLParser(fields=["word_2"], answer_field="word_2")
    return dataset, parser, rm_encoding


@app.cell(hide_code=True)
def _(dataset, mo):
    mo.md(
        f"Built a dataset with **{len(dataset)}** rows — the same "
        f"`Dataset` object `load_environment()` would hand to "
        f"`SingleTurnEnv`, straight from `rm_singleturn_demo.json`."
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
        Each row is one trial. `perceived` trials show a real `word_2` the
        model must echo back exactly; `imagined` trials blank it out and the
        model has to invent a novel word. `answer` carries the ground truth
        the rubric checks against — it's never shown to the model.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 3. Score a completion""")
    return


@app.cell
def _(dataset, parser, rm_encoding):
    # Simulating what a model's raw completion would look like, for both
    # trial types, then scoring it exactly the way the Hub rubric does.
    import json

    perceived_row = next(r for r in dataset if '"trial_type": "perceived"' in r["answer"])
    imagined_row = next(r for r in dataset if '"trial_type": "imagined"' in r["answer"])

    perceived_completion = f'<word_2>{json.loads(perceived_row["answer"])["word_2"]}</word_2>'
    imagined_completion = "<word_2>gritty</word_2>"

    perceived_score = rm_encoding.encoding_correct(perceived_completion, perceived_row["answer"], parser)
    imagined_score = rm_encoding.encoding_correct(imagined_completion, imagined_row["answer"], parser)
    return (
        imagined_completion,
        imagined_row,
        imagined_score,
        perceived_completion,
        perceived_row,
        perceived_score,
    )


@app.cell(hide_code=True)
def _(
    imagined_completion,
    imagined_score,
    mo,
    perceived_completion,
    perceived_score,
):
    mo.md(
        f"""
        | Trial type | Completion | `encoding_correct` |
        |---|---|---|
        | perceived | `{perceived_completion}` | **{perceived_score}** |
        | imagined | `{imagined_completion}` | **{imagined_score}** |

        Both score `1.0` — the perceived completion echoes `word_2` exactly,
        and the imagined completion is a single alphabetic token that isn't
        `word_1`. Try changing `imagined_completion` above to `word_1`'s own
        value, or to something with a space in it, and re-run — the score
        drops to `0.0`, matching the Scope rules on the environment page.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 4. Ship it

        Everything above ran from the plain Python module in
        `environments/psychscanner_rm_encoding/`. Once your own environment
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
