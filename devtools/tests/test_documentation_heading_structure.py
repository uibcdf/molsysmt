"""Protect semantic Markdown headings without mistaking literal examples for sections."""

import json
import shlex
import subprocess
import sys
from pathlib import Path

import pytest

from devtools.tests.test_documentation_directive_rendering import build as build
from devtools.tests.test_documentation_source_boundary import _discover, _exclusions

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"


def _headings(text):
    pytest.importorskip("myst_parser")
    from markdown_it.renderer import RendererHTML
    from myst_parser.config.main import MdParserConfig
    from myst_parser.parsers.mdit import create_md_parser

    parser = create_md_parser(
        MdParserConfig(enable_extensions={"colon_fence", "dollarmath", "amsmath"}),
        RendererHTML,
    )
    return [
        (int(token.tag[1]), token.map[0])
        for token in parser.parse(text)
        if token.type == "heading_open" and token.level == 0
    ]


@pytest.mark.parametrize(
    "text,expected",
    [
        ("# Page\n\n## Section\n\n### Detail\n", [1, 2, 3]),
        ("# Page\n\n```markdown\n#### Literal example\n```\n", [1]),
        ("# Page\n\n:::{note}\n\n### Inside a note\n:::\n", [1]),
        ("# Page\n\n### Skipped level\n", [1, 3]),
    ],
)
def test_heading_inventory_distinguishes_sections_and_examples(text, expected):
    assert [level for level, _ in _headings(text)] == expected


def test_published_markdown_has_continuous_heading_levels():
    found = _discover(_exclusions())
    checked = []
    failures = []
    for name in sorted(found):
        paths = [DOCS / (name + suffix) for suffix in (".md", ".ipynb")]
        path = next((candidate for candidate in paths if candidate.is_file()), None)
        if path is None:
            continue
        cells = (
            json.loads(path.read_text())["cells"]
            if path.suffix == ".ipynb"
            else [{"cell_type": "markdown", "source": path.read_text()}]
        )
        headings = []
        for index, cell in enumerate(cells):
            if cell["cell_type"] == "markdown":
                headings.extend(
                    (level, index, line)
                    for level, line in _headings("".join(cell["source"]))
                )
        assert headings, f"No document title: {path.relative_to(ROOT)}"
        previous = 0
        for level, cell, line in headings:
            if level > previous + 1:
                failures.append((name, cell, line, previous, level))
            previous = level
        if name.startswith("content/course/") or name == "index":
            assert sum(level == 1 for level, _, _ in headings) == 1, name
        checked.append(name)
    assert len(checked) >= 400
    assert failures == [], failures


def test_published_markdown_labels_are_unambiguous():
    pytest.importorskip("myst_parser")
    from docutils.nodes import fully_normalize_name
    from markdown_it.renderer import RendererHTML
    from myst_parser.config.main import MdParserConfig
    from myst_parser.parsers.mdit import create_md_parser

    parser = create_md_parser(
        MdParserConfig(enable_extensions={"colon_fence"}), RendererHTML
    )
    found = _discover(_exclusions())
    labels = {}
    duplicates = []
    for name in sorted(found):
        path = next(
            (
                DOCS / (name + suffix)
                for suffix in (".md", ".ipynb")
                if (DOCS / (name + suffix)).is_file()
            ),
            None,
        )
        if path is None:
            continue
        cells = (
            json.loads(path.read_text())["cells"]
            if path.suffix == ".ipynb"
            else [{"cell_type": "markdown", "source": path.read_text()}]
        )
        for ci, cell in enumerate(cells):
            if cell["cell_type"] != "markdown":
                continue
            for token in parser.parse("".join(cell["source"])):
                if token.type != "myst_target":
                    continue
                label = fully_normalize_name(token.content)
                if label in labels:
                    duplicates.append((label, labels[label], (name, ci)))
                labels[label] = (name, ci)
    assert len(labels) >= 200
    assert duplicates == [], duplicates
    assert (
        labels["tutorial_is_composed_of"][0]
        == "content/user/tools/basic/is_composed_of"
    )
    assert (
        labels["tutorial_element_is_composed_of"][0]
        == "content/user/tools/element/is_composed_of"
    )


def test_home_has_one_semantic_title_and_preserved_section_names():
    notebook = json.loads((DOCS / "index.ipynb").read_text())
    text = "\n\n".join(
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "markdown"
    )
    headings = _headings(text)
    lines = text.splitlines()
    assert [(level, lines[line]) for level, line in headings] == [
        (1, "# MolSysMT"),
        (2, "## Install it"),
        (2, "## Use it"),
        (2, "## Citation"),
    ]
    assert "(index-top)=\n# MolSysMT" in text
    assert "{rst-class} molsysmt-home" in text


@pytest.mark.parametrize(
    "legacy", [False, True], ids=["actual", "broken-negative-control"]
)
def test_home_render_keeps_brand_and_one_document_title(build, legacy):
    from docutils import nodes

    notebook = json.loads((DOCS / "index.ipynb").read_text())
    text = "\n\n".join(
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "markdown"
        and ".. toctree::" not in "".join(cell["source"])
    )
    if legacy:
        text = text.replace(
            ":::{rst-class} molsysmt-home\n:::\n\n(index-top)=\n# MolSysMT\n", ""
        )
    app, warnings, html = build(
        text,
        {
            "_static/logo.svg": (DOCS / "_static/logo.svg").read_text(),
            "_static/logo_dark.svg": (DOCS / "_static/logo_dark.svg").read_text(),
            "_bibtex/software.bib": (DOCS / "_bibtex/software.bib").read_text(),
            "content/about/citation.md": "---\norphan: true\n---\n\n"
            + (DOCS / "content/about/citation.md").read_text(),
        },
    )
    if legacy:
        assert warnings.count("Document headings start at H2, not H1") == 3
        return
    assert warnings == ""
    tree = app.env.get_doctree("index")
    root_sections = [node for node in tree.children if isinstance(node, nodes.section)]
    assert len(root_sections) == 1
    section = root_sections[0]
    assert "molsysmt-home" in section["classes"]
    assert section.next_node(nodes.title).astext() == "MolSysMT"
    children = [node for node in section.children if isinstance(node, nodes.section)]
    assert [node.next_node(nodes.title).astext() for node in children] == [
        "Install it",
        "Use it",
        "Citation",
    ]
    assert [node["ids"][0] for node in children] == ["install-it", "use-it", "citation"]
    assert len(list(tree.findall(nodes.image))) == 2
    assert 'style="width: 50%;"' in html
    assert "designed to simplify work with molecular models and simulations" in html
    assert "https://doi.org/10.5281/zenodo.1298752" in html
    css = (DOCS / "_static/custom.css").read_text()
    assert ".molsysmt-home > h1" in css and "clip: rect(0, 0, 0, 0)" in css
    assert (
        ".molsysmt-home > section > h2" in css
        and "font-size: var(--pst-font-size-h1)" in css
    )


@pytest.mark.parametrize(
    "legacy", [False, True], ids=["actual", "broken-negative-control"]
)
def test_documentation_ci_options_reject_real_sphinx_warning(tmp_path, legacy):
    yaml = pytest.importorskip("yaml")
    pytest.importorskip("myst_parser")
    workflow = yaml.safe_load(
        (ROOT / ".github/workflows/sphinx_docs_to_gh_pages.yaml").read_text()
    )
    steps = workflow["jobs"]["sphinx_docs_to_gh-pages"]["steps"]
    action = next(
        step
        for step in steps
        if step.get("uses", "").startswith("uibcdf/action-sphinx-docs-to-gh-pages@")
    )
    options = shlex.split(action["with"]["sphinx-opts"])
    if legacy:
        options = [option for option in options if option != "-W"]
    source = tmp_path / "source"
    source.mkdir()
    (source / "conf.py").write_text("extensions=['myst_parser']\nmaster_doc='index'\n")
    (source / "index.md").write_text("# Warning guard\n\n### Skipped section level\n")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sphinx",
            "-M",
            "html",
            str(source),
            str(tmp_path / "build"),
            *options,
        ],
        capture_output=True,
        text=True,
    )
    output = result.stdout + result.stderr
    assert "[myst.header]" in output
    assert result.returncode == (0 if legacy else 1), output
