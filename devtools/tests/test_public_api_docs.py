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
    from sphinx.application import Sphinx

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
    app = Sphinx(
        str(source),
        str(source),
        str(tmp_path / "html"),
        str(tmp_path / "doctrees"),
        "html",
        status=StringIO(),
        warning=warnings,
        warningiserror=True,
    )
    app.build(force_all=True)
    assert app.statuscode == 0, warnings.getvalue()
    assert warnings.getvalue() == ""
    rendered = (tmp_path / "html" / "index.html").read_text(encoding="utf-8")
    assert function_name.rsplit(".", 1)[-1] in rendered


def test_box_geometry_docstring_renders_without_rst_errors(tmp_path):
    _render_api_docstring(
        tmp_path,
        "molsysmt.pbc.get_lengths_and_angles_from_box",
        "Tutorial_Get_lengths_and_angles_from_box",
    )


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
