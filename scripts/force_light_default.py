"""Post-build step for the docs site: default to light mode, not OS preference.

book.yml has no extra_javascript hook and _site_src/mkdocs.yml is regenerated
every build (marimo-book hardcodes prefers-color-scheme media queries in its
palette block with no override), so this patches the built HTML directly
instead, same approach as inject_new_tab_links.py.

Pre-seeds Material's __palette storage (via its own __md_get/__md_set helpers,
scoped under the site root path — a raw "__palette" localStorage key would be
the wrong key) before bundle.min.js (loaded at the end of <body>) runs its own
matchMedia-based auto-detection. __md_get/__md_set are defined inline in
<head>, so this only has to land after <body> opens. Reads primary/accent off
the page's own data-md-color-* attributes instead of hardcoding "indigo", so
it stays correct if book.yml ever sets a custom palette color.

A visitor who has never toggled the theme gets light; the toggle still works
normally and their explicit choice still overrides this on later visits.
"""

import sys
from pathlib import Path

SNIPPET = """<script>
(function () {
  if (typeof __md_get === "function" && typeof __md_set === "function" && !__md_get("__palette")) {
    __md_set("__palette", {
      index: 0,
      color: {
        media: "(prefers-color-scheme: light)",
        scheme: "default",
        primary: document.body.getAttribute("data-md-color-primary"),
        accent: document.body.getAttribute("data-md-color-accent")
      }
    });
  }
})();
</script>
"""


def main(site_dir: str) -> None:
    for path in Path(site_dir).rglob("*.html"):
        html = path.read_text(encoding="utf-8")
        if "<body" in html and "__md_get(\"__palette\")" not in html:
            idx = html.index(">", html.index("<body")) + 1
            html = html[:idx] + "\n" + SNIPPET + html[idx:]
            path.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "_site")
