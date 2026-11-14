"""Preserve maintained API content while generating genuinely missing stubs."""

import runpy
import sys
from io import StringIO
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MODULE = "molsysmt_autosummary_probe_752"


@pytest.fixture(scope="module")
def rendered_api(tmp_path_factory):
    pytest.importorskip("sphinx")
    from sphinx.testing.util import SphinxTestApp

    base = tmp_path_factory.mktemp("owned-api")
    source = base / "source"
    generated = source / "generated"
    generated.mkdir(parents=True)
    (source / "conf.py").write_text(
        "extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosummary']\n"
        "master_doc = 'index'\n",
        encoding="utf-8",
    )
    (source / f"{MODULE}.py").write_text(
        "class StoredValue:\n"
        '    """Hold a declared value."""\n'
        "    def apply(self):\n"
        '        """Apply the explicit stored-value contract."""\n'
        "    def to_dict(self):\n"
        '        """Return the detached stored-value representation."""\n'
        "\ndef new_operation():\n"
        '    """Provide the newly documented operation."""\n',
        encoding="utf-8",
    )
    (source / "index.rst").write_text(
        "Public API\n==========\n\n"
        ".. autosummary::\n   :toctree: generated\n\n"
        f"   {MODULE}.StoredValue\n   {MODULE}.new_operation\n",
        encoding="utf-8",
    )
    owned = generated / f"{MODULE}.StoredValue.rst"
    original = (
        "Maintained API\n==============\n\n"
        "This maintained page records the declared conversion boundary.\n\n"
        f".. autoclass:: {MODULE}.StoredValue\n"
        "   :members: apply, to_dict\n"
    ).encode()
    owned.write_bytes(original)
    warnings = StringIO()
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(sys, "path", sys.path.copy())
        patch.chdir(ROOT / "docs")
        policy = runpy.run_path(str(ROOT / "docs/conf.py"))
        overrides = {
            name: policy[name]
            for name in ("autosummary_generate", "autosummary_generate_overwrite")
            if name in policy
        }
        patch.syspath_prepend(str(source))
        app = SphinxTestApp(
            srcdir=source,
            builddir=base,
            confoverrides=overrides,
            status=StringIO(),
            warning=warnings,
            warningiserror=True,
        )
        try:
            app.build(force_all=True)
            assert app.statuscode == 0, warnings.getvalue()
            assert warnings.getvalue() == ""
            yield {
                "owned": owned,
                "original": original,
                "generated": generated,
                "html": base / "html/generated",
            }
        finally:
            app.cleanup()
            sys.modules.pop(MODULE, None)


def test_autosummary_keeps_the_maintained_source_and_context(rendered_api):
    assert rendered_api["owned"].read_bytes() == rendered_api["original"]
    html = (rendered_api["html"] / f"{MODULE}.StoredValue.html").read_text()
    assert "declared conversion boundary" in html


def test_autosummary_keeps_complete_method_entries(rendered_api):
    html = (rendered_api["html"] / f"{MODULE}.StoredValue.html").read_text()
    for method in ("apply", "to_dict"):
        assert f'id="{MODULE}.StoredValue.{method}"' in html
    assert "explicit stored-value contract" in html
    assert "detached stored-value representation" in html


def test_autosummary_still_generates_a_missing_public_page(rendered_api):
    assert (rendered_api["generated"] / f"{MODULE}.new_operation.rst").is_file()
    html = (rendered_api["html"] / f"{MODULE}.new_operation.html").read_text()
    assert f'id="{MODULE}.new_operation"' in html
    assert "newly documented operation" in html
