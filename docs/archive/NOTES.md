# Docs archive

Edits made 2026-08-19. Unlike psychscanner, psychscanner-primal never had a
standalone "Reality Monitoring" example page — RM was named directly in the
core docs (`intro.md`, `README.md`, `CONTRIBUTING.md`,
`conditional_next_trial.md`) as one of the two task families the package
actually ships (`examples/tasks/rm_*.json`, confirmed byte-identical to
psychscanner's reality-monitoring task cards; `pal50.json` is the other).
Those files were **not** deleted — only the doc prose naming "Reality
Monitoring" by name was genericized to "`rm_*`" and pointed at the new
[Demonstration Suite](../content/demonstration_suite.md) page instead, since
this package has no demonstration suite of its own (per the decision to use
psychscanner's `examples/demonstration_suite/` as the reference demos for
primal too).

## What changed and why

- `docs/content/intro.md` — "Only the feedback-scored task cards: Reality
  Monitoring (`rm_*`) and paired-associate learning (`pal50`)." →
  genericized to "`rm_*` and `pal50`" + link to `examples/tasks/` and the new
  Demonstration Suite page. Worked fine as original prose; changed only to
  drop the named callout per the removal request.
- `docs/content/conditional_next_trial.md` — "psychscanner-primal keeps only
  feedback-scored tasks (Reality Monitoring, paired-associate learning)" →
  "(see the Demonstration Suite)". Same reasoning; the doc's actual content
  (the `next_trial_fn` mechanism) is unaffected.
- `README.md` — same "Reality Monitoring (`rm_*`)" phrase in the
  Included/Excluded list, genericized the same way.
- `CONTRIBUTING.md` — "There's no requirement to reuse the Reality Monitoring
  or PAL50 scoring logic" → "the existing `rm_*` or PAL50 scoring logic".

## What was intentionally left alone

- `README.md`'s citation section ("please cite the psychscanner framework
  paper (and the Reality Monitoring paper, since that task is bundled
  here)") — this is an academic citation requirement, not a documentation
  example; removing it would misattribute a paper whose task is genuinely
  bundled in this package. Left untouched.
- `examples/tasks/rm_*.json` and `examples/tasks/README.md` — the actual task
  files and their file listing were out of scope (docs-only removal); the
  README there already describes them (inaccurately, as "Relational-memory
  task" rather than reality monitoring) but that predates this change and
  wasn't part of the requested edit.
- `docs/content/using_psychscanner_primal.md`, `hub_environment.md`,
  `write_your_own_task.md`, `cli_reference.md`, `prime_intellect_hub.md` — no
  RM mentions found in these; unchanged.
