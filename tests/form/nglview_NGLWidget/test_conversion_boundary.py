"""Keeping native validation keywords inside the MolSysMT boundary."""

import warnings

import pytest
from depdigest.core import checker

import molsysmt as msm
from molsysmt._private.smonitor import LibraryNotFoundError
from molsysmt.form.molsysmt_MolSys.to_nglview_NGLWidget import to_nglview_NGLWidget


def test_native_conversion_does_not_send_validation_keywords_to_widget(builder_pdb_molsys):
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "error",
            message="Passing unrecognized arguments.*skip_digestion.*",
            category=DeprecationWarning,
        )
        view = msm.convert(builder_pdb_molsys, to_form="nglview.NGLWidget")
    assert msm.get(view, element="system", n_atoms=True) == 4
    assert msm.get(view, element="system", n_structures=True) == 1


def test_direct_native_converter_reports_the_absent_optional_provider(
    builder_pdb_molsys, monkeypatch
):
    original = checker.is_installed
    monkeypatch.setattr(
        checker, "is_installed", lambda name: False if name == "nglview" else original(name)
    )
    with pytest.raises(LibraryNotFoundError):
        to_nglview_NGLWidget(builder_pdb_molsys)
