"""Protect published content while keeping repository-only material out of Sphinx."""

import ast
import json
import re
import shutil
from io import StringIO
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
REPOSITORY_ONLY = (
    "AGENTS.md",
    "index.AGENTS.md",
    "README.md",
    "api/index_v2.md",
    "content/user/tools/index_v2.md",
    "content/user/tools/Supported.ipynb",
    "content/course/README.md",
    "content/course/_template.ipynb",
    "content/course/devtools/README.md",
    "content/course/pending_fixes/README.md",
    "content/course/pending_fixes/unit_01_supported_forms_link.md",
    "content/course/pending_proposals/README.md",
)


def _config_value(name, default=()):
    tree = ast.parse((DOCS / "conf.py").read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name
            for target in node.targets
        ):
            return ast.literal_eval(node.value)
    return list(default)


def _exclusions():
    return _config_value("exclude_patterns")


def _discover(exclusions):
    pytest.importorskip("sphinx")
    from sphinx.project import Project

    project = Project(DOCS, _config_value("source_suffix"))
    # BuildEnvironment.find_files also excludes the HTML builder's assets and
    # templates. Their README files are resources, not published documents.
    resources = (
        _config_value("templates_path")
        + _config_value("html_static_path")
        + _config_value("html_extra_path")
    )
    return project.discover(
        exclude_paths=exclusions + resources,
        include_paths=_config_value("include_patterns", ["**"]),
    )


@pytest.mark.parametrize(
    "legacy", [False, True], ids=["actual", "broken-negative-control"]
)
def test_repository_only_material_stays_out_of_published_source_set(legacy):
    exclusions = _exclusions()
    if legacy:
        exclusions = [
            "_build",
            "Thumbs.db",
            ".DS_Store",
            "**.ipynb_checkpoints",
            "old_api",
            "freezer",
            "temp",
            "**/AGENTS.md",
            "**/*.AGENTS.md",
        ]
    found = _discover(exclusions)
    leaked = {
        source
        for source in REPOSITORY_ONLY
        if Path(source).with_suffix("").as_posix() in found
    }
    assert all((DOCS / source).is_file() for source in REPOSITORY_ONLY)
    if legacy:
        assert leaked == set(REPOSITORY_ONLY)
        return
    assert leaked == set()
    assert not any("AGENTS" in name for name in found)


def test_active_user_course_and_api_sources_remain_discoverable():
    yaml = pytest.importorskip("yaml")
    found = _discover(_exclusions())
    expected = {"index"}
    # All real API and User Guide sources are protected, not just a few examples.
    for area in (DOCS / "api", DOCS / "content/user"):
        for path in area.rglob("*"):
            if path.suffix not in {".md", ".rst", ".ipynb"} or not path.is_file():
                continue
            relative = path.relative_to(DOCS).as_posix()
            if (
                relative in REPOSITORY_ONLY
                or "AGENTS" in path.name
                or ".ipynb_checkpoints" in path.parts
            ):
                continue
            expected.add(path.relative_to(DOCS).with_suffix("").as_posix())
    course = yaml.safe_load((DOCS / "content/course/course_manifest.yml").read_text())
    assert len(course) == 156
    for module in course:
        source = DOCS / "content/course" / module["path"]
        assert source.is_file()
        expected.add(source.relative_to(DOCS).with_suffix("").as_posix())
    expected.update(
        path.relative_to(DOCS).with_suffix("").as_posix()
        for path in (DOCS / "content/course").rglob("index.md")
    )
    manifest = yaml.safe_load((DOCS / "docs_manifest.yml").read_text())

    def visit(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key in {"agents_file", "index_agents_file"}:
                    source = ROOT / item
                    assert source.is_file(), item
                    assert (
                        source.relative_to(DOCS).with_suffix("").as_posix() not in found
                    )
                    continue
                if key in {"file", "index_file"} or (
                    key == "path"
                    and isinstance(item, str)
                    and Path(item).suffix in {".md", ".rst", ".ipynb"}
                ):
                    source = ROOT / item
                    assert source.is_file(), item
                    expected.add(source.relative_to(DOCS).with_suffix("").as_posix())
                else:
                    visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    visit(manifest)
    assert expected <= found, sorted(expected - found)


@pytest.mark.parametrize(
    "legacy", [False, True], ids=["actual", "broken-negative-control"]
)
def test_public_bond_and_historical_hbond_api_pages_are_connected(tmp_path, legacy):
    pytest.importorskip("sphinx")
    from sphinx.testing.util import SphinxTestApp

    source = tmp_path / "source"
    source.mkdir()
    for area in ("element", "hbonds"):
        shutil.copytree(DOCS / "api" / area, source / "api" / area)
    if legacy:
        element = source / "api/element/api_element.rst"
        element.write_text(element.read_text().replace("   bond/api_bond\n", ""))
        hbonds = source / "api/hbonds/api_hbonds.rst"
        hbonds.write_text(hbonds.read_text().split("Historical import paths", 1)[0])
    (source / "conf.py").write_text(
        "extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosummary', 'sphinx.ext.napoleon']\n"
        "autosummary_generate = False\nmaster_doc = 'index'\n"
    )
    (source / "index.rst").write_text(
        "API navigation\n==============\n\n.. toctree::\n\n"
        "   api/element/api_element\n   api/hbonds/api_hbonds\n   references\n"
    )
    # Supply only real public tutorial anchors. The full-site build verifies
    # their complete pages; this miniature isolates API navigation and imports.
    tutorial_sources = (
        [
            "content/user/tools/element/atom/atom_types.md",
            "content/user/tools/interactions/result.md",
        ]
        + [
            f"content/user/tools/hbonds/{name}.ipynb"
            for name in (
                "get_buch_hbonds",
                "get_donor_atoms",
                "get_acceptor_atoms",
                "get_luzard_chandler_hbonds",
            )
        ]
        + [
            f"content/user/tools/interactions/{name}.ipynb"
            for name in (
                "get_hbonds",
                "get_hbond_sites",
                "get_hbond_site_directions",
            )
        ]
    )
    reference_text = "Real tutorial targets\n=====================\n\n"
    for relative in tutorial_sources:
        path = DOCS / relative
        text = path.read_text()
        if path.suffix == ".ipynb":
            text = "\n\n".join(
                "".join(cell["source"])
                for cell in json.loads(text)["cells"]
                if cell["cell_type"] == "markdown"
            )
        label = re.search(r"^\(([^)]+)\)=$", text, flags=re.M)
        assert label is not None, relative
        reference_text += f".. _{label[1]}:\n\n{label[1]}\n{'-' * len(label[1])}\n\n"
    (source / "references.rst").write_text(reference_text)
    warnings = StringIO()
    app = SphinxTestApp(
        srcdir=source, builddir=tmp_path, status=StringIO(), warning=warnings
    )
    try:
        app.build(force_all=True)
        assert app.statuscode == 0, warnings.getvalue()
        targets = {"api/element/bond/api_bond"} | {
            f"api/hbonds/autosummary/molsysmt.hbonds.{name}"
            for name in (
                "get_acceptor_atoms",
                "get_donor_atoms",
                "get_buch_hbonds",
                "get_luzard_chandler_hbonds",
            )
        }
        connected = set().union(*app.env.toctree_includes.values())
        if legacy:
            assert not (targets & connected)
            assert warnings.getvalue().count("[toc.not_included]") == 5
            return
        assert targets <= connected
        assert warnings.getvalue() == ""
        bond_html = (Path(app.outdir) / "api/element/bond/api_bond.html").read_text()
        assert (
            "max_expected_bond_length" in bond_html
            and "bond_length_tolerance" in bond_html
        )
        assert "not a general" in bond_html and "angstroms" in bond_html
        hbonds_html = (Path(app.outdir) / "api/hbonds/api_hbonds.html").read_text()
        assert "Historical import paths" in hbonds_html
        assert all(
            Path(target).name + ".html" in hbonds_html
            for target in targets
            if "/hbonds/" in target
        )
    finally:
        app.cleanup()
