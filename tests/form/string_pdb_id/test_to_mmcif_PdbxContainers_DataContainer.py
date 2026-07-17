"""Tests for string_pdb_id -> mmcif DataContainer conversion behavior."""

import importlib
import shutil

import pytest

import molsysmt as msm


def test_to_mmcif_pdbxcontainers_datacontainer_reports_aggregated_offline_error(monkeypatch):
    module_under_test = importlib.import_module(
        "molsysmt.form.string_pdb_id.to_mmcif_PdbxContainers_DataContainer"
    )

    def fail_bcif_gz(*args, **kwargs):
        raise RuntimeError("bcif.gz offline")

    def fail_bcif(*args, **kwargs):
        raise RuntimeError("bcif offline")

    def fail_cif_gz(*args, **kwargs):
        raise RuntimeError("cif.gz offline")

    def fail_cif(*args, **kwargs):
        raise RuntimeError("cif offline")

    monkeypatch.setattr(
        importlib.import_module("molsysmt.form.string_pdb_id.to_file_bcif_gz"),
        "to_file_bcif_gz",
        fail_bcif_gz,
    )
    monkeypatch.setattr(
        importlib.import_module("molsysmt.form.string_pdb_id.to_file_bcif"),
        "to_file_bcif",
        fail_bcif,
    )
    monkeypatch.setattr(
        importlib.import_module("molsysmt.form.string_pdb_id.to_file_cif_gz"),
        "to_file_cif_gz",
        fail_cif_gz,
    )
    monkeypatch.setattr(
        importlib.import_module("molsysmt.form.string_pdb_id.to_file_cif"),
        "to_file_cif",
        fail_cif,
    )

    with pytest.raises(RuntimeError) as exc:
        module_under_test.to_mmcif_PdbxContainers_DataContainer("pdb_id:181l", skip_digestion=True)

    text = str(exc.value)
    assert "Attempted formats: bcif.gz, bcif, cif.gz, cif" in text
    assert "bcif.gz offline" in text
    assert "bcif offline" in text
    assert "cif.gz offline" in text
    assert "cif offline" in text


def test_convert_multimodel_pdb_id_uses_all_nmr_models_offline(monkeypatch):
    """Convert the public 1L2Y identifier into its complete NMR ensemble."""

    source = msm.systems["Trp-Cage"]["1l2y.bcif.gz"]
    requested_ids = []

    def use_bundled_bcif(pdb_id=None, output_filename=None, **kwargs):
        requested_ids.append(pdb_id)
        shutil.copyfile(source, output_filename)
        return output_filename

    file_bcif_gz = importlib.import_module("molsysmt.form.file_bcif_gz")
    monkeypatch.setattr(file_bcif_gz, "download", use_bundled_bcif)

    ensemble = msm.convert("1L2Y")

    assert requested_ids == ["1L2Y"]
    assert msm.get_form(ensemble) == "molsysmt.MolSys"
    assert ensemble.topology.n_atoms == 304
    assert ensemble.topology.n_groups == 20
    assert ensemble.structures.n_structures == 38
    assert ensemble.structures.coordinates.shape == (38, 304, 3)
    assert ensemble.structures.occupancy is None
