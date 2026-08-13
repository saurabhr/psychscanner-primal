"""Post-build step for the docs site: make every link open in a new tab.

book.yml has no extra_javascript hook and _site_src/mkdocs.yml is
regenerated every build, so this patches the built HTML directly instead.
`defer` + document$ keeps it applying after navigation.instant page swaps,
matching psychscanner's own docs/javascripts/open-links-new-tab.js.
"""

import sys
from pathlib import Path

SNIPPET = """<script defer>
(function () {
  function tagLinks(root) {
    root.querySelectorAll("a[href]").forEach(function (a) {
      var href = a.getAttribute("href");
      if (!href || href.charAt(0) === "#" || href.indexOf("mailto:") === 0 || href.indexOf("tel:") === 0) return;
      a.target = "_blank";
      a.rel = "noopener";
    });
  }
  if (typeof document$ !== "undefined") {
    document$.subscribe(function () { tagLinks(document); });
  } else {
    tagLinks(document);
  }
})();
</script>
"""


def main(site_dir: str) -> None:
    for path in Path(site_dir).rglob("*.html"):
        html = path.read_text(encoding="utf-8")
        if "</body>" in html and "tagLinks" not in html:
            path.write_text(html.replace("</body>", SNIPPET + "</body>", 1), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "_site")
