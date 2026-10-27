"""Render real citation, portal and topology blocks without hiding parser warnings."""

import json
import re
from io import StringIO
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TOPOLOGY_PAGES = (
    "get_bondgraph",
    "get_covalent_blocks",
    "get_covalent_paths",
    "get_dihedral_quartets",
    "get_sequence_alignment",
    "get_sequence_identity",
)


def _markdown(path):
    return "\n\n".join(
        "".join(cell["source"])
        for cell in json.loads(path.read_text())["cells"]
        if cell["cell_type"] == "markdown"
    )


@pytest.fixture
def build(tmp_path):
    pytest.importorskip("myst_parser")
    pytest.importorskip("sphinx_design")
    from sphinx.testing.util import SphinxTestApp

    source = tmp_path / "source"
    source.mkdir()
    (source / "conf.py").write_text(
        'extensions = ["myst_parser", "sphinx_design"]\n'
        'myst_enable_extensions = ["colon_fence"]\nmaster_doc = "index"\n'
    )
    apps = []

    def render(text, extra=None):
        (source / "index.md").write_text(text)
        for relative, payload in (extra or {}).items():
            path = source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(payload)
        warnings = StringIO()
        app = SphinxTestApp(
            srcdir=source, builddir=tmp_path, status=StringIO(), warning=warnings
        )
        apps.append(app)
        app.build(force_all=True)
        assert app.statuscode == 0, warnings.getvalue()
        return app, warnings.getvalue(), (tmp_path / "html/index.html").read_text()

    yield render
    for app in reversed(apps):
        app.cleanup()


@pytest.mark.parametrize(
    "legacy", [False, True], ids=["actual", "broken-negative-control"]
)
def test_citation_panels_keep_text_doi_and_bibliography_download(build, legacy):
    text = (ROOT / "docs/content/about/citation.md").read_text()
    if legacy:
        text = text.replace("{tab-set}", "{tabs}").replace("{tab-item}", "{tab}")
    # Preserve the real page's relative bibliography location in the fixture.
    app, warnings, html = build(
        "# Citation fixture\n\n```{toctree}\ncontent/about/citation\n```\n",
        {
            "content/about/citation.md": text,
            "_bibtex/software.bib": (ROOT / "docs/_bibtex/software.bib").read_text(),
        },
    )
    if legacy:
        assert "Unknown directive type: 'tabs'" in warnings
        return
    assert warnings == ""
    html = (Path(app.outdir) / "content/about/citation.html").read_text()
    assert (
        "sd-tab-set" in html
        and len(re.findall(r'class="[^\"]*\bsd-tab-content\b[^\"]*"', html)) == 2
    )
    assert "Paper" in html and "Software" in html
    assert "Diego Prada-Gracia" in html and "Liliana M. Moreno-Vargas" in html
    assert "https://doi.org/10.5281/zenodo.1298752" in html
    assert 'class="reference download internal"' in html and "software.bib" in html
    downloads = list(Path(app.outdir).glob("_downloads/*/software.bib"))
    assert len(downloads) == 1
    assert (
        downloads[0].read_bytes() == (ROOT / "docs/_bibtex/software.bib").read_bytes()
    )


@pytest.mark.parametrize(
    "legacy", [False, True], ids=["actual", "broken-negative-control"]
)
def test_supported_forms_notice_keeps_body_and_live_portal_link(build, legacy):
    from docutils import nodes

    text = _markdown(
        ROOT / "docs/content/course/Common_Core/01_The_Form_Agnostic_Philosophy.ipynb"
    )
    block = re.search(
        r"(?ms)^:::\{(?:info|admonition)\}[^\n]*\n.*?^:::\s*$", text
    ).group()
    if legacy:
        block = block.replace("{admonition} Supported Forms Portal", "{info}")
    app, warnings, html = build("# Supported forms\n\n" + block)
    if legacy:
        assert "Unknown directive type: 'info'" in warnings
        return
    assert warnings == ""
    notices = list(app.env.get_doctree("index").findall(nodes.admonition))
    assert len(notices) == 1 and {"dropdown", "info"} <= set(notices[0]["classes"])
    assert "Supported Forms Portal" in notices[0].astext()
    assert "full list of 60+ supported forms" in notices[0].astext()
    assert "https://www.uibcdf.org/molsysmt" in html


@pytest.mark.parametrize(
    "legacy", [False, True], ids=["actual", "broken-negative-control"]
)
def test_topology_dropdowns_keep_tutorial_bodies_and_reference_lists(build, legacy):
    from docutils import nodes
    from sphinx import addnodes

    blocks = []
    for name in TOPOLOGY_PAGES:
        text = _markdown(ROOT / f"docs/content/user/tools/topology/{name}.ipynb")
        blocks.extend(
            match.group()
            for match in re.finditer(
                r"(?ms)^:::\{(?:note|seealso)\}[^\n]*\n.*?^:::\s*$", text
            )
            if "Demo Systems Catalog" in match.group()
            or "Related Tools & References" in match.group()
        )
    assert len(blocks) == 10
    text = "\n\n".join(blocks)
    if legacy:
        for kind, title in [
            ("note", "Demo Systems Catalog"),
            ("seealso", "Related Tools & References"),
        ]:
            text = text.replace(
                f":::{{{kind}}}\n:class: dropdown\n\n**{title}**\n\n",
                f":::{{{kind}}} {title}\n:class: dropdown\n\n",
            )
    # The miniature site isolates directive parsing. Full-site builds separately
    # check real tutorial targets; these fixture labels preserve link rendering.
    labels = set()
    for target in re.findall(r"\{ref\}`([^`]+)`", text):
        labels.add(target.split("<")[-1].rstrip(">"))
    references = (
        "---\norphan: true\n---\n\n# Fixture reference targets\n\n"
        + "\n\n".join(f"({label})=\n## {label}" for label in sorted(labels))
    )
    app, warnings, html = build(
        "# Topology dropdowns\n\n" + text, {"references.md": references}
    )
    if legacy:
        assert "[myst.directive_parse]" in warnings
        return
    assert warnings == ""
    tree = app.env.get_doctree("index")
    notes = list(tree.findall(nodes.note))
    related = list(tree.findall(addnodes.seealso))
    assert len(notes) == 4 and len(related) == 6
    for note in notes:
        assert "dropdown" in note["classes"]
        assert "Demo Systems Catalog" in note.astext()
        assert "full catalog of bundled systems, forms, and file paths" in note.astext()
    for node in related:
        assert "dropdown" in node["classes"]
        assert "Related Tools & References" in node.astext()
        assert len(list(node.findall(nodes.list_item))) >= 3
    assert html.count('class="reference internal"') >= len(related)
