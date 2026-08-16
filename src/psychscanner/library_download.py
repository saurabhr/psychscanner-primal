"""Fetch psyscan-library's task cards onto local disk.

`download_lib()` clones (or updates) a checkout of the `psyscan-library`
index repo and returns paths you can pass straight to `task_library()` as
`dirs=`.

Quick recipe::

    from psychscanner import download_lib, task_library

    paths = download_lib()  # library="primal" (this package)
    card = task_library("rm_singleturn_demo", dirs=paths["tasks"])

primal has no `experiment_library` (see `psychscanner-primal`'s
`__init__.py`), so this only ever hands back `tasks/` -- `kind` isn't a
parameter here the way it is on full `psychscanner`.

Cards aren't portable between the `psychscanner` and `primal` distributions
-- see `psyscan-library`'s README. By default `download_lib()` refuses to
fetch cards for a distro other than the one actually installed; pass
`library="all"` to opt into fetching both anyway (browsing, or CI that
covers both distros).
"""

from __future__ import annotations

import importlib.metadata as metadata
import subprocess
from pathlib import Path
from typing import Literal

__all__ = ["download_lib"]

LIBRARY_REPO_URL = "https://github.com/saurabhr/psyscan-library.git"
_CACHE_DIR = Path.home() / ".cache" / "psychscanner" / "psyscan-library"

Library = Literal["psychscanner", "primal", "all"]
_DISTROS: tuple[str, ...] = ("psychscanner", "primal")


def _installed_distro() -> str | None:
    """Which of psychscanner/psychscanner-primal is installed here, if either
    (they share the `psychscanner` import name, so at most one really is)."""
    for dist_name, distro in (("psychscanner-primal", "primal"), ("psychscanner", "psychscanner")):
        try:
            metadata.version(dist_name)
            return distro
        except metadata.PackageNotFoundError:
            continue
    return None


# ponytail: shells out to the system `git` (already a dev-environment
# dependency) instead of adding a git library. No lockfile around the cache
# dir -- concurrent callers racing the same dest is unhandled, add a lock if
# this ever runs from parallel processes against one cache dir.
def _sync_repo(dest: Path, ref: str) -> None:
    if (dest / ".git").is_dir():
        subprocess.run(["git", "-C", str(dest), "fetch", "--depth", "1", "origin", ref], check=True)
        subprocess.run(["git", "-C", str(dest), "reset", "--hard", "FETCH_HEAD"], check=True)
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "clone", "--depth", "1", "--branch", ref, LIBRARY_REPO_URL, str(dest)],
            check=True,
        )


def download_lib(
    library: Library = "primal",
    dest: str | Path | None = None,
    ref: str = "main",
) -> dict[str, Path] | dict[str, dict[str, Path]]:
    """Clone/update `psyscan-library` and return the `tasks/` subfolder(s).

    Parameters
    ----------
    library : "psychscanner" | "primal" | "all"
        Which distro's task cards to hand back. `"primal"` (default) checks
        that it matches the package actually installed in this environment
        and raises if it doesn't. `"psychscanner"` and `"all"` are for
        inspecting/porting the other distro's cards -- primal can't
        actually run them.
    dest : str | os.PathLike | None
        Where to clone/update the checkout. Defaults to a shared cache dir
        (`~/.cache/psychscanner/psyscan-library`) so repeat calls just
        `git fetch` instead of re-cloning.
    ref : str
        Branch/tag to check out. Defaults to `"main"`.

    Returns
    -------
    dict[str, Path]
        `{"tasks": Path}` for a single library. For `library="all"`,
        `{"psychscanner": {"tasks": Path}, "primal": {"tasks": Path}}`.

    Raises
    ------
    ValueError
        `library` invalid.
    RuntimeError
        `library="primal"` but the installed package isn't primal.
    """
    if library not in (*_DISTROS, "all"):
        raise ValueError(f"library must be one of {(*_DISTROS, 'all')}, got {library!r}")

    if library == "primal":
        installed = _installed_distro()
        if installed != "primal":
            raise RuntimeError(
                f"library='primal' but the installed package is {installed!r} -- "
                "primal cards aren't guaranteed to run here. Install psychscanner-primal, "
                "or pass library='all'/'psychscanner' to fetch the other distro's cards."
            )

    dest = Path(dest) if dest is not None else _CACHE_DIR
    _sync_repo(dest, ref)

    distros = _DISTROS if library == "all" else (library,)
    results = {distro: {"tasks": dest / "tasks" / distro} for distro in distros}
    return results if library == "all" else results[library]
