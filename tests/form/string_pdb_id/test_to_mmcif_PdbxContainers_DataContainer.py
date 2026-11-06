"""Tests for string_pdb_id -> mmcif DataContainer conversion behavior."""

import importlib
import shutil

import numpy as np
import pytest

import molsysmt as msm


def test_to_mmcif_pdbxcontainers_datacontainer_reports_aggregated_offline_error(
    monkeypatch,
):
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
        module_under_test.to_mmcif_PdbxContainers_DataContainer(
            "pdb_id:181l", skip_digestion=True
        )

    text = str(exc.value)
    assert "Attempted formats: bcif.gz, bcif, cif.gz, cif" in text
    assert "bcif.gz offline" in text
    assert "bcif offline" in text
    assert "cif.gz offline" in text
    assert "cif offline" in text


def test_convert_multimodel_pdb_id_uses_all_nmr_models_offline(monkeypatch):
    """Convert the public 1L2Y identifier into its complete NMR ensemble."""

    source = msm.systems["Trp-Cage"]["1l2y.bcif.gz"]
    deposited = msm.convert(source, to_form="mmcif.PdbxContainers.DataContainer")
    atom_site = deposited.getObj("atom_site")
    columns = {name: index for index, name in enumerate(atom_site.getAttributeList())}
    models = {}
    for row in atom_site.getRowList():
        models.setdefault(row[columns["pdbx_PDB_model_num"]], []).append(row)
    assert len(models) == 38
    first_model = next(iter(models.values()))
    expected_coordinates = np.asarray(
        [
            [
                [
                    float(row[columns[field]])
                    for field in ("Cartn_x", "Cartn_y", "Cartn_z")
                ]
                for row in rows
            ]
            for rows in models.values()
        ]
    )
    requested_ids = []

    def use_bundled_bcif(pdb_id=None, output_filename=None, **kwargs):
        requested_ids.append(pdb_id)
        shutil.copyfile(source, output_filename)
        return output_filename

    file_bcif_gz = importlib.import_module("molsysmt.form.file_bcif_gz")
    monkeypatch.setattr(file_bcif_gz, "download", use_bundled_bcif)

    ensemble = msm.convert("1L2Y")

    # Downloads use the canonical lowercase ID; the ensemble stays complete.
    assert requested_ids == ["1l2y"]
    assert msm.get_form(ensemble) == "molsysmt.MolSys"
    assert ensemble.topology.n_atoms == 304
    assert ensemble.topology.n_groups == 20
    assert ensemble.structures.n_structures == 38
    assert ensemble.structures.coordinates.shape == (38, 304, 3)
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(ensemble.structures.coordinates, to_unit="angstrom"),
        expected_coordinates,
        rtol=0,
        atol=1e-12,
    )
    assert ensemble.topology.atoms.atom_id.tolist() == [
        str(row[columns["id"]]) for row in first_model
    ]
    assert ensemble.topology.atoms.atom_name.tolist() == [
        row[columns["label_atom_id"]] for row in first_model
    ]
    assert all(isinstance(label, str) for label in ensemble.topology.atoms.atom_id)
    # The source explicitly declares full occupancy for every observation.
    np.testing.assert_array_equal(ensemble.structures.occupancy, np.ones((38, 304)))
