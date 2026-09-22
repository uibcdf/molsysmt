"""Regression tests for file:cif conversions to native MolSysMT forms."""

import sys

import numpy as np

import molsysmt as msm


def test_file_cif_to_molsysmt_topology_preserves_counts(hp35_cif_file):
    topology = msm.convert(hp35_cif_file, to_form="molsysmt.Topology")

    assert topology.n_atoms == 596
    assert topology.n_groups == 36
    assert topology.n_entities == 1


def test_file_cif_to_molsysmt_molsys_preserves_first_names(hp35_cif_file):
    molsys = msm.convert(hp35_cif_file, to_form="molsysmt.MolSys")

    assert np.all(
        molsys.topology.atoms["atom_name"].to_numpy()[:5]
        == np.array(["N", "CA", "C", "O", "CB"], dtype=object)
    )
    assert np.all(
        molsys.topology.groups["group_name"].to_numpy()[:3]
        == np.array(["MET", "LEU", "SER"], dtype=object)
    )


def test_file_cif_to_molsysmt_molsys_preserves_explicit_entity_ids(hp35_cif_file):
    molsys = msm.convert(hp35_cif_file, to_form="molsysmt.MolSys")

    assert molsys.topology.entities["entity_id"].to_list() == ["1"]


def test_file_cif_conversion_uses_the_portable_public_adapter(
    hp35_cif_file, monkeypatch
):
    import mmcif.io
    from mmcif.io.IoAdapterPy import IoAdapterPy

    from molsysmt.form.file_cif.to_mmcif_PdbxContainers_DataContainer import (
        to_mmcif_PdbxContainers_DataContainer,
    )

    monkeypatch.setattr(mmcif.io, "IoAdapter", IoAdapterPy)
    monkeypatch.setitem(sys.modules, "mmcif.io.IoAdapterCore", None)

    container = to_mmcif_PdbxContainers_DataContainer(hp35_cif_file)

    assert container.getName() == "1VII"
    assert container.getObj("atom_site").getRowCount() == 596
