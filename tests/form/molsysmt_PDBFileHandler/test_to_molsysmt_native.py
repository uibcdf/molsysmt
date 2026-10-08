"""
Regression tests for molsysmt.PDBFileHandler conversions to native MolSysMT forms.
"""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm


@pytest.mark.parametrize("infer_string", [False, True])
@pytest.mark.parametrize("route", ["file", "handler"])
def test_compnd_names_preserve_topology_with_copy_on_write(
    t4_pdb_file, t4_pdb_handler, t4_pdb_molsys, infer_string, route
):
    source = t4_pdb_file if route == "file" else t4_pdb_handler
    records = [
        (record.molecule, list(record.chain))
        for record in t4_pdb_handler.entry.title.compnd
    ]
    with pd.option_context(
        "future.infer_string", infer_string, "mode.copy_on_write", True
    ):
        output = msm.convert(source, to_form="molsysmt.MolSys")

    protein = output.topology.molecules["molecule_type"] == "protein"
    assert output.topology.molecules.loc[protein, "molecule_name"].tolist() == [
        "T4 LYSOZYME"
    ]
    assert output.topology.n_atoms == t4_pdb_molsys.topology.n_atoms
    assert output.topology.n_groups == t4_pdb_molsys.topology.n_groups
    assert output.topology.n_bonds == t4_pdb_molsys.topology.n_bonds
    assert output.topology.n_entities == t4_pdb_molsys.topology.n_entities
    assert output.topology.atoms["atom_id"].tolist() == (
        t4_pdb_molsys.topology.atoms["atom_id"].tolist()
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(output.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(t4_pdb_molsys.structures.coordinates, to_unit="nm"),
    )
    assert [
        (record.molecule, list(record.chain))
        for record in t4_pdb_handler.entry.title.compnd
    ] == records
    assert not t4_pdb_handler.file.closed


def test_pdb_file_handler_to_molsysmt_topology_preserves_counts(
    t4_pdb_handler, t4_pdb_molsys
):
    topology = msm.convert(t4_pdb_handler, to_form="molsysmt.Topology")

    assert topology.n_atoms == t4_pdb_molsys.topology.n_atoms
    assert topology.n_groups == t4_pdb_molsys.topology.n_groups


def test_pdb_file_handler_to_molsysmt_structures_preserves_shape(
    t4_pdb_handler, t4_pdb_molsys
):
    structures = msm.convert(t4_pdb_handler, to_form="molsysmt.Structures")

    assert structures.n_atoms == t4_pdb_molsys.structures.n_atoms
    assert structures.n_structures == t4_pdb_molsys.structures.n_structures


def test_pdb_file_handler_to_molsysmt_molsys_preserves_first_atom_names(
    t4_pdb_handler, t4_pdb_molsys
):
    molsys = msm.convert(t4_pdb_handler, to_form="molsysmt.MolSys")

    assert np.all(
        molsys.topology.atoms["atom_name"].to_numpy()[:5]
        == np.array(["N", "CA", "C", "O", "CB"], dtype=object)
    )
    assert np.all(
        molsys.topology.groups["group_name"].to_numpy()[:3]
        == np.array(["MET", "ASN", "ILE"], dtype=object)
    )


def test_pdb_file_handler_from_builder_fixture_preserves_declared_truth(
    builder_pdb_handler, builder_pdb_molsys
):
    molsys = msm.convert(builder_pdb_handler, to_form="molsysmt.MolSys")

    assert molsys.topology.n_atoms == builder_pdb_molsys.topology.n_atoms
    assert molsys.topology.n_groups == builder_pdb_molsys.topology.n_groups
    assert molsys.topology.n_bonds == builder_pdb_molsys.topology.n_bonds
    assert (
        molsys.topology.atoms["atom_name"].tolist()
        == builder_pdb_molsys.topology.atoms["atom_name"].tolist()
    )
    assert (
        molsys.topology.groups["group_name"].tolist()
        == builder_pdb_molsys.topology.groups["group_name"].tolist()
    )
    assert (
        molsys.topology.chains["chain_id"].tolist()
        == builder_pdb_molsys.topology.chains["chain_id"].tolist()
    )


def test_get_uses_native_attribute_pipes(builder_pdb_handler):
    atom_indices, group_names, coordinates = msm.get(
        builder_pdb_handler,
        element="atom",
        selection=[0, 1],
        atom_index=True,
        group_name=True,
        coordinates=True,
    )

    assert atom_indices == [0, 1]
    assert group_names == ["ALA", "ALA"]
    assert coordinates.shape[1:] == (2, 3)
