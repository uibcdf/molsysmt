"""Render real course/Foundations takeaways and preserve their parsed content."""

import json
import re
from io import StringIO
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _blocks():
    sources = [ROOT / "docs/content/user/foundations/index.md"]
    sources.extend(sorted((ROOT / "docs/content/course/Common_Core").glob("*.ipynb")))
    sources.append(ROOT / "docs/content/course/_template.ipynb")
    blocks = []
    for path in sources:
        if path.suffix == ".ipynb":
            text = "\n".join(
                "".join(c["source"])
                for c in json.loads(path.read_text())["cells"]
                if c["cell_type"] == "markdown"
            )
        else:
            text = path.read_text()
        blocks.extend(re.findall(r"```\{key-takeaway\}\n(.*?)\n```", text, re.S))
    return blocks


@pytest.mark.parametrize(
    "register", [True, False], ids=["registered", "missing-negative-control"]
)
def test_real_takeaways_render_body_and_inline_content(tmp_path, register):
    pytest.importorskip("myst_parser")
    from docutils import nodes
    from sphinx.testing.util import SphinxTestApp

    source = tmp_path / "source"
    source.mkdir()
    extension = ", 'key_takeaway'" if register else ""
    (source / "conf.py").write_text(
        f"import sys\nsys.path.insert(0, {str(ROOT / 'docs/_ext')!r})\n"
        f'extensions = ["myst_parser"{extension}]\nmaster_doc = "index"\n'
    )
    bodies = _blocks()
    assert len(bodies) >= 22
    blocks = "\n\n".join("```{key-takeaway}\n" + body + "\n```" for body in bodies)
    (source / "index.md").write_text("# Actual takeaway blocks\n\n" + blocks)
    # A standard admonition is the independent rendering oracle for the alias.
    (source / "oracle.md").write_text(
        "---\norphan: true\n---\n\n# Standard admonitions\n\n"
        + blocks.replace("{key-takeaway}", "{admonition} Key takeaway")
    )
    warnings = StringIO()
    app = SphinxTestApp(
        srcdir=source, builddir=tmp_path, status=StringIO(), warning=warnings
    )
    try:
        app.build(force_all=True)
        if not register:
            assert "Unknown directive type: 'key-takeaway'" in warnings.getvalue()
            assert not list(app.env.get_doctree("index").findall(nodes.admonition))
            return
        assert app.statuscode == 0, warnings.getvalue()
        assert warnings.getvalue() == ""
        actual = list(app.env.get_doctree("index").findall(nodes.admonition))
        oracle = list(app.env.get_doctree("oracle").findall(nodes.admonition))
        assert len(actual) == len(oracle) == len(bodies)
        assert [node.astext() for node in actual] == [node.astext() for node in oracle]
        html = (tmp_path / "html/index.html").read_text()
        assert html.count("admonition-key-takeaway") == len(bodies)
        assert "Key takeaway" in html
    finally:
        app.cleanup()
