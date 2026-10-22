"""Reject modular files as legacy handlers without loading resident domains."""

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import FormatError
from molsysmt.native import H5MSMFileHandler
from tests.native.test_molsys import build_minimal_molsys


@pytest.mark.parametrize("version", ["0.5", np.bytes_("0.5")])
@pytest.mark.parametrize("path_type", [str, lambda path: path])
@pytest.mark.parametrize("input_kind", ["single", "list", "tuple"])
@pytest.mark.parametrize("multiple_targets", [False, True])
def test_modular_handler_rejected_before_domain_loading(
    tmp_path, monkeypatch, version, path_type, input_kind, multiple_targets
):
    path = tmp_path / "modular.h5msm"
    msm.h5msm.write(build_minimal_molsys(n_structures=2), path)
    with h5py.File(path, "r+") as file:
        file.attrs["version"] = version

    def forbidden(*args, **kwargs):
        pytest.fail("An unsupported handler request materialized modular domains")

    monkeypatch.setattr(
        "molsysmt.form._h5msm05_modular.read_molsys_file", forbidden
    )
    source = path_type(path)
    if input_kind == "list":
        source = [source]
    elif input_kind == "tuple":
        source = (source,)
    target = "molsysmt.H5MSMFileHandler"
    if multiple_targets:
        target = ["molsysmt.MolSys", target]
    with pytest.raises(FormatError) as error:
        msm.convert(source, to_form=target)
    reason = error.value.extra["reason"]
    assert "H5MSM 0.5" in reason
    assert "only H5MSM 0.3 and 0.4" in reason
    assert "to_form='molsysmt.MolSys'" in reason
    assert "read_layers" in reason


def test_direct_modular_handler_rejection_closes_file(tmp_path):
    path = tmp_path / "modular.h5msm"
    with h5py.File(path, "w") as file:
        file.attrs["version"] = "0.5"
    handler = H5MSMFileHandler.__new__(H5MSMFileHandler)
    with pytest.raises(FormatError) as error:
        handler.__init__(path)
    assert "resident load" in error.value.extra["reason"]
    assert not handler.file.id.valid


@pytest.mark.parametrize("version", ["0.3", "0.4"])
def test_legacy_handler_conversion_still_opens_supported_schema(tmp_path, version):
    path = tmp_path / "legacy.h5msm"
    with H5MSMFileHandler(path, "w", format_version=version):
        pass
    with msm.convert(path, to_form="molsysmt.H5MSMFileHandler") as handler:
        assert handler.format_version == version
        assert handler.file.id.valid
