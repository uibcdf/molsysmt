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


def test_box_geometry_docstring_renders_without_rst_errors(tmp_path):
    """Render the actual public API text through its NumPy-to-RST boundary."""
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
        ".. _Tutorial_Get_lengths_and_angles_from_box:\n\n"
        "Box geometry\n============\n\n"
        ".. autofunction:: molsysmt.pbc.get_lengths_and_angles_from_box\n",
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
    assert "get_lengths_and_angles_from_box" in rendered
