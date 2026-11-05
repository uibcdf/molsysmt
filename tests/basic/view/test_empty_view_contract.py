"""Exercise empty workspaces and preflight without rendering a browser canvas."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError


@pytest.mark.parametrize("viewer", ["MolSysViewer", "NGLView"])
@pytest.mark.parametrize("explicit", [False, True])
@pytest.mark.parametrize("trusted", [False, True])
def test_default_or_explicit_none_creates_empty_workspace(
    viewer, explicit, trusted, monkeypatch
):
    pytest.importorskip("molsysviewer" if viewer == "MolSysViewer" else "nglview")
    monkeypatch.delenv("MSM_VIEWS_FROM_HTML_FILES", raising=False)
    kwargs = dict(viewer=viewer, skip_digestion=trusted)
    if explicit:
        kwargs["molecular_system"] = None
    result = msm.view(**kwargs)
    try:
        if viewer == "MolSysViewer":
            assert msm.get_form(result) == "molsysviewer.MolSysView"
            assert result.molsys is None
        else:
            assert msm.get_form(result) == "nglview.NGLWidget"
            assert result._ngl_component_ids == []
    finally:
        result.close()


@pytest.mark.parametrize("viewer", ["MolSysViewer", "NGLView"])
@pytest.mark.parametrize(
    "selection,structures",
    [(None, None), ([], []), (np.array([], dtype=np.int64), "all"), ("all", [])],
)
def test_empty_source_accepts_all_none_and_flat_empty_axes(
    viewer, selection, structures, monkeypatch
):
    from molsysmt.basic.viewer import _dict_view

    seen = []
    monkeypatch.setitem(
        _dict_view, viewer, lambda **kwargs: seen.append(kwargs) or kwargs
    )
    result = msm.view(selection=selection, structure_indices=structures, viewer=viewer)
    assert result["molecular_system"] is None
    assert len(seen) == 1
    assert result["skip_digestion"] is True


@pytest.mark.parametrize(
    "viewer,dependency", [("MolSysViewer", "molsysviewer"), ("NGLView", "nglview")]
)
def test_absent_selected_backend_uses_native_dependency_diagnostic(
    viewer, dependency, monkeypatch
):
    from depdigest.core import checker

    from molsysmt._private.smonitor import LibraryNotFoundError

    original_find_spec = checker.find_spec

    def missing(name, *args, **kwargs):
        return None if name == dependency else original_find_spec(name, *args, **kwargs)

    try:
        monkeypatch.setattr(checker, "find_spec", missing)
        checker.is_installed.cache_clear()
        with pytest.raises(LibraryNotFoundError, match=dependency):
            msm.view(viewer=viewer)
    finally:
        monkeypatch.setattr(checker, "find_spec", original_find_spec)
        checker.is_installed.cache_clear()


@pytest.mark.parametrize("viewer", ["MolSysViewer", "NGLView"])
def test_real_empty_axes_create_empty_workspace(viewer, monkeypatch):
    pytest.importorskip("molsysviewer" if viewer == "MolSysViewer" else "nglview")
    monkeypatch.delenv("MSM_VIEWS_FROM_HTML_FILES", raising=False)
    result = msm.view(selection=[], structure_indices=[], viewer=viewer)
    try:
        if viewer == "MolSysViewer":
            assert result.molsys is None
        else:
            assert result._ngl_component_ids == []
    finally:
        result.close()


@pytest.mark.parametrize(
    "argument,value",
    [
        ("selection", "atom_type == 'C'"),
        ("selection", 0),
        ("selection", [0]),
        ("selection", [-1]),
        ("selection", True),
        ("selection", [[]]),
        ("structure_indices", [0]),
        ("structure_indices", -1),
        ("structure_indices", False),
        ("structure_indices", [[]]),
        ("viewer", "unknown"),
        ("viewer", 17),
        ("syntax", "unknown"),
        ("skip_digestion", 1),
    ],
)
def test_invalid_empty_request_never_creates_backend(argument, value, monkeypatch):
    from molsysmt.basic.viewer import _dict_view

    def forbidden(**kwargs):
        raise AssertionError("Invalid empty request reached backend construction")

    monkeypatch.setitem(_dict_view, "MolSysViewer", forbidden)
    with pytest.raises(ArgumentError):
        msm.view(**{argument: value})


@pytest.mark.parametrize(
    "caller",
    [
        None,
        "molsysmt.basic.get.get",
        "molsysmt.structure.get_distances.get_distances",
        "other.module.view",
        "molsysmt.basic.view_other.view",
    ],
)
def test_none_exception_is_scoped_to_exact_public_view(caller):
    from molsysmt._private.argdigest.argument.molecular_system import (
        digest_molecular_system,
    )

    with pytest.raises(ArgumentError):
        digest_molecular_system(None, caller=caller)
    assert digest_molecular_system(None, caller="molsysmt.basic.view.view") is None


def test_explicit_viewer_none_reads_configuration_but_omission_keeps_default(
    monkeypatch,
):
    from molsysmt.basic.viewer import _dict_view

    monkeypatch.setattr(msm.configure, "default_viewer", "NGLView")
    monkeypatch.setitem(_dict_view, "MolSysViewer", lambda **kwargs: "MolSysViewer")
    monkeypatch.setitem(_dict_view, "NGLView", lambda **kwargs: "NGLView")
    assert msm.view(viewer=None) == "NGLView"
    assert msm.view() == "MolSysViewer"


@pytest.mark.parametrize("argument", ["selection", "structure_indices"])
def test_loaded_empty_axis_is_forwarded_as_a_loaded_request(
    alanine_molsys, argument, monkeypatch
):
    from molsysmt.basic.viewer import _dict_view

    monkeypatch.setitem(_dict_view, "MolSysViewer", lambda **kwargs: kwargs)
    output = msm.view(alanine_molsys, **{argument: []})
    assert output["molecular_system"] is alanine_molsys
    assert output[argument] == []


@pytest.mark.parametrize(
    "selection,structures",
    [([99999], "all"), ("atom_type === 'C'", "all"), ("all", [99999])],
)
def test_loaded_input_still_validates_before_backend(
    alanine_molsys, monkeypatch, selection, structures
):
    from molsysmt.basic.viewer import _dict_view

    def forbidden(**kwargs):
        raise AssertionError("Invalid loaded selection reached backend construction")

    monkeypatch.setitem(_dict_view, "MolSysViewer", forbidden)
    with pytest.raises(ArgumentError):
        msm.view(alanine_molsys, selection=selection, structure_indices=structures)
