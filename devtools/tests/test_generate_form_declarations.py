"""Protecting class recognition after catalogue regeneration."""

import json
from pathlib import Path

from devtools.scripts.generate_form_declarations import declaration
from molsysmt.form import catalogue, molsysviewer_MolSysView


def test_regeneration_preserves_viewer_class_recognition(tmp_path, monkeypatch):
    generated = declaration(molsysviewer_MolSysView, "molsysviewer.MolSysView")
    plugin = tmp_path / "molsysviewer_MolSysView"
    plugin.mkdir()
    (plugin / "form.json").write_text(json.dumps(generated))
    monkeypatch.setattr(catalogue, "__file__", str(tmp_path / "catalogue.py"))
    monkeypatch.setattr(catalogue, "_catalogue", None)
    for name in ("MolSysView", "IframeMarkup"):
        cls = type(name, (), {"__module__": "molsysviewer.views"})
        assert catalogue.form_of_class(cls()) == "molsysviewer.MolSysView"
    # The generator must also match the declaration currently shipped, rather
    # than making only this isolated synthetic catalogue recognize the classes.
    shipped = Path(molsysviewer_MolSysView.__file__).with_name("form.json")
    assert generated == json.loads(shipped.read_text())
