"""Structural guards for the published API reference."""

from io import StringIO
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
API_ROOT = REPOSITORY_ROOT / "docs" / "api"


def test_published_api_reference_excludes_private_modules():
    assert not any(path.is_file() for path in (API_ROOT / "_private").rglob("*"))

    offenders = []
    for source in API_ROOT.rglob("*"):
        if source.suffix not in {".md", ".rst"}:
            continue
        if "molsysmt._private" in source.read_text(encoding="utf-8"):
            offenders.append(source.relative_to(REPOSITORY_ROOT).as_posix())

    assert offenders == []


def _render_api_docstring(tmp_path, function_name, tutorial_label):
    """Render actual public API text through its NumPy-to-RST boundary."""
    pytest.importorskip("sphinx")
    from sphinx.testing.util import SphinxTestApp

    source = tmp_path / "source"
    source.mkdir()
    (source / "conf.py").write_text(
        "extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']\n"
        "master_doc = 'index'\n",
        encoding="utf-8",
    )
    (source / "index.rst").write_text(
        f".. _{tutorial_label}:\n\n"
        "Public API\n==========\n\n"
        f".. autofunction:: {function_name}\n",
        encoding="utf-8",
    )
    warnings = StringIO()
    app = SphinxTestApp(
        srcdir=source,
        builddir=tmp_path,
        status=StringIO(),
        warning=warnings,
        warningiserror=True,
    )
    try:
        app.build(force_all=True)
        assert app.statuscode == 0, warnings.getvalue()
        assert warnings.getvalue() == ""
        rendered = (tmp_path / "html" / "index.html").read_text(encoding="utf-8")
        assert function_name.rsplit(".", 1)[-1] in rendered
    finally:
        app.cleanup()


def test_box_geometry_docstring_renders_without_rst_errors(tmp_path):
    _render_api_docstring(
        tmp_path,
        "molsysmt.pbc.get_lengths_and_angles_from_box",
        "Tutorial_Get_lengths_and_angles_from_box",
    )


def test_least_rmsd_fit_docstring_renders_without_rst_errors(tmp_path):
    _render_api_docstring(
        tmp_path,
        "molsysmt.structure.least_rmsd_fit",
        "Tutorial_Least_rmsd_fit",
    )


def test_molsys_manual_type_setter_docstring_renders_and_example_runs(tmp_path):
    _render_api_docstring(
        tmp_path,
        "molsysmt.form.molsysmt_MolSys.set.set_atom_ff_type_to_atom",
        "Tutorial_Set",
    )

    import doctest

    from molsysmt.form.molsysmt_MolSys.set import set_atom_ff_type_to_atom

    example = doctest.DocTestParser().get_doctest(
        set_atom_ff_type_to_atom.__doc__,
        {"set_atom_ff_type_to_atom": set_atom_ff_type_to_atom},
        "set_atom_ff_type_to_atom",
        "public-docstring",
        0,
    )
    result = doctest.DocTestRunner().run(example)
    assert result.failed == 0 and result.attempted == 4


@pytest.mark.parametrize(
    "function_name,tutorial_label",
    [
        ("molsysmt.build.build_peptide", "Tutorial_Build_peptide"),
        ("molsysmt.third_party.tleap.TLeap.run", "Tutorial_TLeap"),
    ],
)
def test_resource_lifecycle_docstrings_render_without_rst_errors(
    tmp_path, function_name, tutorial_label
):
    _render_api_docstring(tmp_path, function_name, tutorial_label)


def test_nglview_color_docstring_renders_without_rst_errors(tmp_path, monkeypatch):
    _render_api_docstring(
        tmp_path,
        "molsysmt.third_party.nglview.set_color_by_value",
        "Tutorial_NGLView_Set_color_by_value",
    )

    import doctest
    from importlib import import_module

    pytest.importorskip("nglview")
    from molsysmt.third_party.nglview import set_color_by_value

    def reject_remote_example(*args, **kwargs):
        raise AssertionError("The public example must use bundled local data.")

    downloader = import_module("molsysmt.form.file_pdb.download")
    monkeypatch.setattr(downloader, "download", reject_remote_example)
    example = doctest.DocTestParser().get_doctest(
        set_color_by_value.__doc__, {}, "set_color_by_value", "public-docstring", 0
    )
    runner = doctest.DocTestRunner()
    result = runner.run(example, clear_globs=False)
    assert result.failed == 0
    representation = example.globs["view"]._ngl_msg_archive[-1]
    assert representation["reconstruc_color_scheme"] is True
    assert len(representation["kwargs"]["color"]) == len(example.globs["values"])


def test_legacy_toolbox_cards_render_without_directive_errors(tmp_path):
    """Render the retained draft's actual cards, without its separate navigation."""
    pytest.importorskip("sphinx_design")
    pytest.importorskip("myst_parser")
    from sphinx.testing.util import SphinxTestApp

    source = tmp_path / "source"
    source.mkdir()
    (source / "conf.py").write_text(
        "extensions = ['myst_parser', 'sphinx_design']\n"
        "myst_enable_extensions = ['colon_fence']\nmaster_doc = 'index'\n",
        encoding="utf-8",
    )
    draft = REPOSITORY_ROOT / "docs/content/user/tools/index_v2.md"
    cards = draft.read_text(encoding="utf-8").split("```{eval-rst}", 1)[0]
    (source / "index.md").write_text(cards, encoding="utf-8")
    warnings = StringIO()
    app = SphinxTestApp(
        srcdir=source,
        builddir=tmp_path,
        status=StringIO(),
        warning=warnings,
        warningiserror=True,
    )
    try:
        app.build(force_all=True)
        assert app.statuscode == 0, warnings.getvalue()
        assert warnings.getvalue() == ""
        rendered = (tmp_path / "html/index.html").read_text(encoding="utf-8")
        assert "sd-row-cols-1" in rendered
        assert "sd-row-cols-md-2" in rendered
        assert "sd-row-cols-lg-3" in rendered
        assert "Explore Basic" in rendered
        assert "Explore Third Party" in rendered
    finally:
        app.cleanup()


@pytest.mark.parametrize(
    "function_name",
    [
        "molsysmt.form.file_prmtop.get_structural_attributes.get_box_from_system",
        "molsysmt.form.file_trjpk.to_file_trjpk.to_file_trjpk",
        "molsysmt.form.file_trjpk.get_topological_attributes.get_n_atoms_from_system",
        "molsysmt.form.file_trjpk.get_topological_attributes.get_atom_index_from_atom",
        "molsysmt.form.file_trjpk.get_structural_attributes.get_n_structures_from_system",
        "molsysmt.form.file_trjpk.get_structural_attributes.get_coordinates_from_atom",
        "molsysmt.form.file_trjpk.get_structural_attributes.get_coordinates_from_system",
        "molsysmt.form.file_trjpk.get_structural_attributes.get_box_from_system",
        "molsysmt.form.file_trjpk.get_structural_attributes.get_time_from_system",
        "molsysmt.form.file_trjpk.get_structural_attributes.get_structure_id_from_system",
    ],
)
def test_restored_file_query_docstrings_render_without_rst_errors(
    tmp_path, function_name
):
    _render_api_docstring(tmp_path, function_name, "Restored_file_query")
