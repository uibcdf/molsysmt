"""Checking serialized widget coordinates without claiming browser rendering."""

import base64
import json
from html.parser import HTMLParser

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import Structures


class _WidgetStateParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.states = []
        self.views = []
        self._chunks = None
        self._kind = None

    def handle_starttag(self, tag, attrs):
        kind = dict(attrs).get("type")
        if tag == "script" and kind in {
            "application/vnd.jupyter.widget-state+json",
            "application/vnd.jupyter.widget-view+json",
        }:
            self._chunks = []
            self._kind = kind

    def handle_data(self, data):
        if self._chunks is not None:
            self._chunks.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._chunks is not None:
            destination = (
                self.states
                if self._kind == "application/vnd.jupyter.widget-state+json"
                else self.views
            )
            destination.append(json.loads("".join(self._chunks)))
            self._chunks = None
            self._kind = None


def test_write_html_preserves_each_structure_and_length_units(
    builder_pdb_molsys, tmp_path
):
    molsys = builder_pdb_molsys.copy()
    coordinates = np.arange(36, dtype=np.float32).reshape(3, 4, 3) / 10
    molsys.structures = Structures(coordinates=puw.quantity(coordinates, "nm"))
    source = puw.get_value(molsys.structures.coordinates, to_unit="nm").copy()
    view = msm.view(molsys, viewer="NGLView")
    output = tmp_path / "molecular-structures.html"

    msm.third_party.nglview.write_html(view, output)

    parser = _WidgetStateParser()
    parser.feed(output.read_text())
    assert len(parser.states) == 1
    model = parser.states[0]["state"][view.model_id]
    assert model["model_name"] == "NGLModel"
    state = model["state"]
    assert state["_ngl_serialize"] is True
    resource = state["_ngl_coordinate_resource"]
    assert resource["n_frames"] == 3  # External NGLView serialized field.
    assert len(resource["0"]) == 3
    for index, encoded in enumerate(resource["0"]):
        actual = np.frombuffer(base64.b64decode(encoded), dtype=np.float32).reshape(
            4, 3
        )
        np.testing.assert_allclose(
            actual, coordinates[index] * 10, rtol=1e-6, atol=1e-6
        )
    np.testing.assert_array_equal(
        puw.get_value(molsys.structures.coordinates, to_unit="nm"), source
    )


@pytest.fixture
def independent_views(builder_pdb_molsys):
    import nglview as nv

    view = msm.view(builder_pdb_molsys, viewer="NGLView")
    text = (
        "REMARK UNREQUESTED_SYNTHETIC_WIDGET_B\n"
        "ATOM      1  C   LIG B   1      82.375  83.375  84.375  1.00  0.00           C\n"
        "END\n"
    )
    unrelated = nv.NGLWidget(nv.TextStructure(text))
    try:
        yield view, unrelated, text
    finally:
        view.close()
        unrelated.close()


@pytest.mark.parametrize("skip_digestion", [False, True])
def test_write_html_excludes_unrequested_molecular_widgets(
    independent_views, tmp_path, skip_digestion
):
    from nglview.color import ColormakerRegistry

    view, unrelated, text = independent_views
    source_structure = view._trajlist[0].get_structure_string()
    unrelated_archive = json.loads(json.dumps(unrelated._ngl_msg_archive))
    output = tmp_path / "requested-view.html"

    msm.third_party.nglview.write_html(view, output, skip_digestion=skip_digestion)

    html = output.read_text()
    parser = _WidgetStateParser()
    parser.feed(html)
    state = parser.states[0]["state"]
    assert view.model_id in state
    assert unrelated.model_id not in state
    assert "UNREQUESTED_SYNTHETIC_WIDGET_B" not in html
    archive = state[view.model_id]["state"]["_ngl_msg_archive"]
    assert any(
        argument.get("data") == source_structure
        for message in archive
        if message.get("methodName") == "loadFile"
        for argument in message.get("args", [])
        if isinstance(argument, dict)
    )
    assert ColormakerRegistry.model_id in state
    assert state[ColormakerRegistry.model_id]["model_name"] == "ColormakerRegistryModel"
    assert {item["model_id"] for item in parser.views} == {
        view.model_id,
        ColormakerRegistry.model_id,
    }
    assert "jquery-ui.css" in html and "fontawesome.com" in html
    assert not view._ngl_serialize
    assert view._ngl_coordinate_resource == {}
    assert unrelated._ngl_msg_archive == unrelated_archive
    assert any(
        argument.get("data") == text
        for message in unrelated_archive
        if message.get("methodName") == "loadFile"
        for argument in message.get("args", [])
        if isinstance(argument, dict)
    )


def test_write_html_does_not_serialize_global_state_before_filtering(
    independent_views, tmp_path
):
    from ipywidgets import DOMWidget

    class UnrequestedSerializationGuard(DOMWidget):
        def _get_embed_state(self, *args, **kwargs):
            raise AssertionError("An unrequested widget was serialized")

    view, _, _ = independent_views
    unrelated = UnrequestedSerializationGuard()
    try:
        msm.third_party.nglview.write_html(view, tmp_path / "limited-state.html")
    finally:
        unrelated.close()


@pytest.mark.parametrize("skip_digestion", [False, True])
def test_write_html_clears_serialization_state_after_write_error(
    independent_views, tmp_path, skip_digestion
):
    view, unrelated, _ = independent_views
    unrelated_archive = json.loads(json.dumps(unrelated._ngl_msg_archive))

    with pytest.raises(FileNotFoundError):
        msm.third_party.nglview.write_html(
            view,
            tmp_path / "missing-directory" / "view.html",
            skip_digestion=skip_digestion,
        )

    assert not view._ngl_serialize
    assert view._ngl_coordinate_resource == {}
    assert unrelated._ngl_msg_archive == unrelated_archive


@pytest.mark.parametrize("skip_digestion", [False, True])
def test_write_html_rejects_a_different_supported_viewer(tmp_path, skip_digestion):
    view = msm.view(viewer="MolSysViewer")
    assert msm.get_form(view) == "molsysviewer.MolSysView"

    with pytest.raises(msm.ArgumentError, match="nglview.NGLWidget"):
        msm.third_party.nglview.write_html(
            view,
            tmp_path / "wrong-viewer.html",
            skip_digestion=skip_digestion,
        )

    assert not (tmp_path / "wrong-viewer.html").exists()


def test_write_html_includes_only_the_requested_viewer_gui_theme(
    independent_views, tmp_path
):
    from nglview.color import ColormakerRegistry

    view, unrelated, _ = independent_views
    assert view._widget_theme is None
    unrelated.gui_style = "ngl"
    unrelated_theme = unrelated._widget_theme
    output = tmp_path / "requested-view-without-theme.html"

    msm.third_party.nglview.write_html(view, output)

    parser = _WidgetStateParser()
    parser.feed(output.read_text())
    assert unrelated_theme.model_id not in parser.states[0]["state"]
    assert unrelated_theme.model_id not in {item["model_id"] for item in parser.views}

    view.gui_style = "ngl"
    requested_theme = view._widget_theme
    assert requested_theme is not None
    output = tmp_path / "requested-view-with-theme.html"

    msm.third_party.nglview.write_html(view, output)

    html = output.read_text()
    parser = _WidgetStateParser()
    parser.feed(html)
    state = parser.states[0]["state"]
    assert state[requested_theme.model_id]["model_name"] == "ThemeManagerModel"
    assert state[requested_theme.model_id]["state"]["_theme_css"] == (
        requested_theme._theme_css
    )
    assert {item["model_id"] for item in parser.views} == {
        requested_theme.model_id,
        ColormakerRegistry.model_id,
        view.model_id,
    }
    assert view.model_id in state and unrelated.model_id not in state
    assert "UNREQUESTED_SYNTHETIC_WIDGET_B" not in html
    # NGLView currently shares ThemeManager as a singleton. If a provider uses
    # separate instances, only the explicitly requested viewer's is required.
    if requested_theme is not unrelated_theme:
        assert unrelated_theme.model_id not in state
    assert not view._ngl_serialize
    assert view._ngl_coordinate_resource == {}
