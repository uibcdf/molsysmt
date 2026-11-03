"""Render real citation, portal and topology blocks without hiding parser warnings."""

import ast
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
OTHER_DROPDOWN_SOURCES = (
    "docs/content/course/Path_Enzyme/32_Interaction_Matrices.ipynb",
    "docs/content/developer/core_architecture/return_types.md",
    "docs/content/user/cookbook/preparing_charged_participants.ipynb",
    "docs/content/user/cookbook/saving_pi_pi_interactions.ipynb",
)
DROPDOWN_LABELS = {
    "Demo Systems Catalog",
    "Molecular Mechanics Backend Engine",
    "Related Tools & References",
    "Related",
}


def _dropdown_blocks(text):
    """Locate actual directives, leaving fenced code examples opaque."""
    pytest.importorskip("myst_parser")
    from markdown_it.renderer import RendererHTML
    from myst_parser.config.main import MdParserConfig
    from myst_parser.parsers.mdit import create_md_parser

    parser = create_md_parser(
        MdParserConfig(enable_extensions={"colon_fence"}), RendererHTML
    )
    lines = text.splitlines(keepends=True)
    blocks = []
    for token in parser.parse(text):
        if token.type not in {"fence", "colon_fence"}:
            continue
        match = re.fullmatch(r"\{(note|seealso)\}(?:\s+(.*))?", token.info.strip())
        if not match:
            continue
        title = match[2] or ""
        label = re.search(r"(?:\A|\n\n)\*\*([^*\n]+)\*\*(?:\n|$)", token.content)
        label = title or (label[1] if label else "")
        if title or label in DROPDOWN_LABELS:
            blocks.append(
                {
                    "kind": match[1],
                    "title": title,
                    "label": label,
                    "lines": token.map,
                    "markup": token.markup,
                    "content": token.content,
                    "text": "".join(lines[token.map[0] : token.map[1]]),
                }
            )
    return blocks


def _standard_dropdown_sources():
    paths = sorted((ROOT / "docs/content/user/tools").rglob("*.ipynb"))
    paths += [ROOT / name for name in OTHER_DROPDOWN_SOURCES]
    for path in paths:
        if ".ipynb_checkpoints" in path.parts:
            continue
        cells = (
            json.loads(path.read_text())["cells"]
            if path.suffix == ".ipynb"
            else [{"cell_type": "markdown", "source": path.read_text()}]
        )
        for index, cell in enumerate(cells):
            if cell["cell_type"] == "markdown":
                for block in _dropdown_blocks("".join(cell["source"])):
                    yield {
                        "path": path.relative_to(ROOT).as_posix(),
                        "cell": index,
                        **block,
                    }


@pytest.mark.parametrize(
    "text,count",
    [
        (":::{note} Demo Systems Catalog\n:class: dropdown\n\nBody.\n:::\n", 1),
        (":::{note}\n:class: dropdown\n\n**Demo Systems Catalog**\n\nBody.\n:::\n", 1),
        (
            "````markdown\n:::{note} Demo Systems Catalog\n:class: dropdown\n\nBody.\n:::\n````\n",
            0,
        ),
    ],
)
def test_dropdown_inventory_distinguishes_directives_from_code_examples(text, count):
    assert len(_dropdown_blocks(text)) == count


def _markdown(path):
    return "\n\n".join(
        "".join(cell["source"])
        for cell in json.loads(path.read_text())["cells"]
        if cell["cell_type"] == "markdown"
    )


@pytest.mark.parametrize(
    "legacy", [False, True], ids=["actual", "broken-negative-control"]
)
def test_docstring_guide_preserves_literal_examples_with_correct_highlighting(
    build, legacy
):
    from docutils import nodes
    from markdown_it import MarkdownIt

    text = (ROOT / "docs/content/developer/documentation/api/docstrings.md").read_text()
    if legacy:
        text = text.replace("```rst\n", "```python\n")
    fences = [token for token in MarkdownIt().parse(text) if token.type == "fence"]
    app, warnings, html = build(text)
    if legacy:
        assert "[misc.highlighting_failure]" in warnings
        return
    assert warnings == ""
    literal = list(app.env.get_doctree("index").findall(nodes.literal_block))
    assert len(literal) == len(fences) >= 23
    assert [node.astext().strip() for node in literal] == [
        token.content.strip() for token in fences
    ]
    fragments = [
        token
        for token in fences
        if token.content.startswith(("Returns\n", ".. ", "- Supported"))
    ]
    assert len(fragments) == 8
    assert all(token.info == "rst" for token in fragments)
    assert (
        "If `in_place=False`, returns a new molecular system."
        in app.env.get_doctree("index").astext()
    )
    assert "highlight-rst" in html and "highlight-python" in html


@pytest.mark.parametrize(
    "legacy", [False, True], ids=["actual", "broken-negative-control"]
)
def test_public_docstring_notes_and_attribution_render_without_loss(build, legacy):
    from docutils import nodes
    from sphinx.ext.napoleon.docstring import NumpyDocstring

    sequence_tree = ast.parse(
        (ROOT / "molsysmt/topology/get_sequence_identity.py").read_text()
    )
    sequence = ast.get_docstring(
        next(node for node in sequence_tree.body if isinstance(node, ast.FunctionDef))
    )
    iterator_tree = ast.parse((ROOT / "molsysmt/basic/iterator.py").read_text())
    iterator = ast.get_docstring(
        next(node for node in iterator_tree.body if isinstance(node, ast.ClassDef))
    )
    if legacy:
        sequence = sequence.replace(
            "calculate_seq_identity [1]_", "calculate_seq_identity"
        )
        iterator = iterator.replace(
            "  with updated structural attributes.",
            "with updated structural attributes.",
        )
    labels = "\n\n".join(
        f"({label})=\n## {label}"
        for label in (
            "Introduction_Forms",
            "Introduction_Selection",
            "Tutorial_Iterator",
        )
    )
    extras = {
        f"{name}.rst": f"{name}\n{'=' * len(name)}\n\n" + str(NumpyDocstring(docstring))
        for name, docstring in (("sequence", sequence), ("iterator", iterator))
    }
    app, warnings, _ = build(
        "# Public docstrings\n\n```{toctree}\nsequence\niterator\n```\n\n" + labels,
        extras,
    )
    if legacy:
        assert "[ref.footnote]" in warnings and "[docutils]" in warnings
        return
    assert warnings == ""
    tree = app.env.get_doctree("sequence")
    references = list(tree.findall(nodes.footnote_reference))
    footnotes = list(tree.findall(nodes.footnote))
    assert len(references) == len(footnotes) == 1
    assert references[0]["refid"] in footnotes[0]["ids"]
    assert "264930d28d3d4987c4fc0c03caba6cf0066e12ca" in footnotes[0].astext()
    assert any(
        "If no attributes are requested, the iterator returns a molecular system per iteration\nwith updated structural attributes."
        in item.astext()
        for item in app.env.get_doctree("iterator").findall(nodes.list_item)
    )


@pytest.mark.parametrize(
    "legacy", [False, True], ids=["actual", "broken-negative-control"]
)
def test_third_party_trees_keep_distinct_targets_and_navigation(build, legacy):
    from sphinx import addnodes

    parent = (ROOT / "docs/api/third_party/api_thirds.rst").read_text()
    child = (ROOT / "docs/api/third_party/openmm/api_openmm.rst").read_text()
    if legacy:
        parent = re.sub(r":name: [^\n]+", ":name: items", parent)
        child = re.sub(r":name: [^\n]+", ":name: items", child)
    extras = {
        "api/third_party/api_thirds.rst": parent,
        "api/third_party/openmm/api_openmm.rst": child,
    }
    for target in (
        "nglview/api_nglview",
        "openmm/forces/api_forces",
        "openmm/platforms/api_platforms",
        "openmm/reporters/api_reporters",
    ):
        extras[f"api/third_party/{target}.rst"] = f"{target}\n{'=' * len(target)}\n"
    app, warnings, _ = build(
        "# Third-party navigation\n\n```{toctree}\napi/third_party/api_thirds\n```\n",
        extras,
    )
    if legacy:
        assert "duplicate label items" in warnings
        return
    assert warnings == ""
    parent_tree = list(
        app.env.get_doctree("api/third_party/api_thirds").findall(addnodes.toctree)
    )
    child_tree = list(
        app.env.get_doctree("api/third_party/openmm/api_openmm").findall(
            addnodes.toctree
        )
    )
    assert len(parent_tree) == len(child_tree) == 1
    assert parent_tree[0]["includefiles"] == [
        "api/third_party/nglview/api_nglview",
        "api/third_party/openmm/api_openmm",
    ]
    assert child_tree[0]["includefiles"] == [
        f"api/third_party/openmm/{part}/api_{part}"
        for part in ("forces", "platforms", "reporters")
    ]
    for name in ("items", "openmm-items"):
        assert name in app.env.domaindata["std"]["labels"]


@pytest.mark.parametrize(
    "legacy", [False, True], ids=["actual", "broken-negative-control"]
)
def test_bond_tutorial_links_to_existing_native_bond_editing_guide(build, legacy):
    text = _markdown(ROOT / "docs/content/user/tools/build/add_missing_bonds.ipynb")
    block = next(
        block["text"] for block in _dropdown_blocks(text) if block["kind"] == "seealso"
    )
    target_path = "content/user/foundations/native_world/classes/molsysmt_Topology"
    target = (ROOT / f"docs/{target_path}.md").read_text()
    if legacy:
        block = block.replace(
            "user-foundations-native-world-classes-molsysmt-topology",
            "Tutorial_Add_bonds",
        )
    # Use the real target header, not a fabricated label for the missing tutorial.
    extra = {
        target_path + ".md": "---\norphan: true\n---\n\n"
        + target.split("\n\n", 1)[0]
        + "\n"
    }
    other_labels = (
        "user-foundations-entrance-demo-systems",
        "Tutorial_Convert",
        "Tutorial_Get",
        "Tutorial_Add_missing_bonds",
    )
    labels = "\n\n".join(f"({label})=\n## {label}" for label in other_labels)
    app, warnings, html = build(
        "# Related bond tools\n\n" + block + "\n" + labels, extra
    )
    if legacy:
        assert "undefined label: 'tutorial_add_bonds'" in warnings
        return
    assert warnings == ""
    tree = app.env.get_doctree("index")
    assert "Topology.add_bonds" in tree.astext()
    assert f'href="{target_path}.html' in html


@pytest.mark.parametrize(
    "legacy", [False, True], ids=["actual", "broken-negative-control"]
)
def test_home_citation_has_live_guidance_and_real_bibliography_download(build, legacy):
    cells = json.loads((ROOT / "docs/index.ipynb").read_text())["cells"]
    sections = [
        "".join(cell["source"])
        for cell in cells
        if cell["cell_type"] == "markdown"
        and "".join(cell["source"]).startswith("## Citation")
    ]
    assert len(sections) == 1
    text = sections[0]
    if legacy:
        text = text.replace(
            "See {ref}`citation guidance <About_Citation>`.",
            "[[BibTeX](_bibtex/papers.bib)]",
        )
    citation = (ROOT / "docs/content/about/citation.md").read_text()
    app, warnings, html = build(
        "# Home citation\n\n" + text,
        {
            "content/about/citation.md": "---\norphan: true\n---\n\n" + citation,
            "_bibtex/software.bib": (ROOT / "docs/_bibtex/software.bib").read_text(),
        },
    )
    if legacy:
        assert "_bibtex/papers.bib" in warnings and "[myst.xref_missing]" in warnings
        return
    assert warnings == ""
    tree = app.env.get_doctree("index")
    assert "The paper is coming soon" in tree.astext()
    assert 'href="content/about/citation.html' in html
    downloads = list(Path(app.outdir).glob("_downloads/*/software.bib"))
    assert len(downloads) == 1
    assert (
        downloads[0].read_bytes() == (ROOT / "docs/_bibtex/software.bib").read_bytes()
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
        domain = (
            "topology"
            if name in {"get_sequence_alignment", "get_sequence_identity"}
            else "chemical_states"
        )
        text = _markdown(ROOT / f"docs/content/user/tools/{domain}/{name}.ipynb")
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


@pytest.mark.parametrize(
    "legacy", [False, True], ids=["actual", "broken-negative-control"]
)
def test_all_standard_dropdowns_keep_contents_and_links(build, legacy):
    from docutils import nodes
    from sphinx import addnodes

    records = list(_standard_dropdown_sources())
    # Do not make a syntax gate pass by deleting the problematic blocks.
    assert len(records) >= 278
    blocks = []
    for record in records:
        block = record["text"]
        if legacy and not record["title"]:
            lines = block.splitlines(keepends=True)
            label_index = next(
                i
                for i, line in enumerate(lines)
                if line.strip() == f"**{record['label']}**"
            )
            del lines[label_index]
            if label_index < len(lines) and not lines[label_index].strip():
                del lines[label_index]
            lines[0] = lines[0].rstrip("\n") + " " + record["label"] + "\n"
            block = "".join(lines)
        blocks.append(block)
    text = "\n\n".join(blocks)
    labels = {
        nodes.fully_normalize_name(target.split("<")[-1].rstrip(">"))
        for target in re.findall(r"\{ref\}`([^`]+)`", text)
    }
    references = "---\norphan: true\n---\n\n# Fixture labels\n\n" + "\n\n".join(
        f"({label})=\n## {label}" for label in sorted(labels)
    )
    extra = {"references.md": references}
    # Render each complete body independently as ordinary Markdown. Comparing
    # parsed text and links catches truncation while allowing legitimate prose
    # differences between catalog, backend and scientific-scope notices.
    oracle_blocks = []
    for index, record in enumerate(records):
        assert record["content"].startswith(":class: dropdown\n\n")
        body = record["content"].split("\n\n", 1)[1]
        oracle_blocks.append(f"::::{{container}} dropdown-body-{index}\n\n{body}\n::::")
    extra["oracle.md"] = "---\norphan: true\n---\n\n# Body oracle\n\n" + "\n\n".join(
        oracle_blocks
    )
    for target in re.findall(r"\{doc\}`([^`]+)`", text):
        target = target.split("<")[-1].rstrip(">")
        extra[target.lstrip("/") + ".md"] = (
            "---\norphan: true\n---\n\n# Fixture document\n"
        )
    app, warnings, html = build("# Standard dropdowns\n\n" + text, extra)
    if legacy:
        assert "[myst.directive_parse]" in warnings
        return
    assert warnings == ""
    tree = app.env.get_doctree("index")
    rendered = list(
        tree.findall(lambda node: isinstance(node, (nodes.note, addnodes.seealso)))
    )
    oracle = list(
        app.env.get_doctree("oracle").findall(
            lambda node: (
                isinstance(node, nodes.container)
                and any(c.startswith("dropdown-body-") for c in node["classes"])
            )
        )
    )
    assert len(rendered) == len(oracle) == len(records)
    for record, node, expected in zip(records, rendered, oracle, strict=True):
        assert "dropdown" in node["classes"], record["path"]
        assert record["label"] in node.astext(), record["path"]
        assert node.astext() == expected.astext(), record["path"]
        assert len(node.astext()) > len(record["label"]) + 20
        for reference_type in (nodes.reference, addnodes.pending_xref):
            assert [
                (ref.astext(), ref.get("reftarget"), ref.get("refuri"))
                for ref in node.findall(reference_type)
            ] == [
                (ref.astext(), ref.get("reftarget"), ref.get("refuri"))
                for ref in expected.findall(reference_type)
            ], record["path"]
        if record["kind"] == "note":
            assert isinstance(node, nodes.note)
            if record["label"] == "Molecular Mechanics Backend Engine":
                assert (
                    "OpenMM" in node.astext()
                    and "delegating energy evaluations" in node.astext()
                )
        else:
            assert isinstance(node, addnodes.seealso)
            assert list(node.findall(nodes.list_item)), record["path"]
            assert list(
                node.findall(
                    lambda child: isinstance(
                        child, (nodes.reference, addnodes.pending_xref)
                    )
                )
            ), record["path"]
    assert "dropdown" in html
