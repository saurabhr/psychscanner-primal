# CLI reference

Installing the package (see **Install as a developer** in [Using psychscanner-primal](using_psychscanner_primal.md)) wires up a `psychscanner-primal` console command, backed by `psychscanner.cli:cli` (`src/psychscanner/cli.py`). It builds an `ExpCardInit`/`ExpCard`, runs a `ScannerModel`, and writes results with `to_csv` — the same objects used in the [Quickstart](quickstart.md).

```bash
psychscanner-primal --help
```

If `-pers`/`--persona_files` is omitted, the run defaults to a single no-persona simulation (`cogtype="no"`, `nsim=1`) — matching the README quickstart. Passing persona files switches to `cogtype="custom"` and runs one simulation per persona.

## Options

| Flag | Type | Default | Description |
|---|---|---|---|
| `-m`, `--model` | text | — | Use the specified model. |
| `-f`, `--family` | text | — | Use the specified family. |
| `-p`, `--parameters` | dict | — | Additional parameters for the model. |
| `-mem`, `--memory` | `SingleTurn` \| `Convo` | `SingleTurn` | Memory type to use. |
| `-memk`, `--memory_k` | int | `-1` | Memory K, number of past interactions to use. |
| `-pers`, `--persona_files` | path list | — | Persona files to use. |
| `-t`, `--task_file` | path | — | Task file to use. |
| `-tc`, `--task_context` | `True` \| `False` \| unset | — | Task context to use. |
| `-tus`, `--tunnel_status` | `0` \| `1` | `0` | Inactive (`0`) or active (`1`, recommended for the final run after testing, to save space) — resumes from the last saved iteration under wall-time limits. |
| `-tuk`, `--tunnel_k` | int | `-1` | Not currently implemented (accepted for forward-compatibility only; a non-default value logs a warning). Data is saved once per simulated participant regardless of this value. |
| `-projname`, `--projectname` | text | `DEFAULTPROJ` | Project name, used when saving experiment data. |
| `-tg`, `--tags` | text list | `[]` | Tags for added information on the experiment card, used when saving data. |
| `-pa`, `--parser` | text | `0` | Parser callable name, if not `0` — must be defined in `staging`. |
| `-praw`, `--parser_raw` | bool | `False` | Return the dict with the raw `AIMessage` output. |
| `-pcon`, `--parser_config` | dict | — | Parser configuration dict. Default behavior is `method=json_schema`. |
| `-pd`, `--proj_dir` | path | `~/psychscanner` | Directory results are written to. |
| `-le`, `--login_env` | path | — | `.env` file to load before running, for proprietary-model API keys (see [python-dotenv](https://github.com/theskumar/python-dotenv)). Keep this file out of version control. |
| `-tq`, `--enabletqdm` | flag | `False` | Enable the tqdm progress bar. |
| `-v`, `--version` | flag | — | Print the installed version and exit. |
| `-h`, `--help` | flag | — | Show the help text and exit. |

## Example

```bash
psychscanner-primal \
  -m mock-llm -f mock-llm \
  -t examples/tasks/rm_singleturn_demo.json \
  -mem SingleTurn \
  -projname primal_quickstart \
  -pd ./results
```

Runs the same task as the [Quickstart](quickstart.md), from the shell instead of Python.
