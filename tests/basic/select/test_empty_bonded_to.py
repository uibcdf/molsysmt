"""Keeping valid empty bonded selections distinct from invalid syntax."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.mark.parametrize("topology_only", [False, True])
@pytest.mark.parametrize(
    "query, expected",
    [
        ('all bonded to atom_type=="Xe"', "empty"),
        ('all not bonded to atom_type=="Xe"', "all"),
        ('atom_type=="Xe" bonded to all', "empty"),
        ('atom_type=="Xe" not bonded to all', "empty"),
        ('(all bonded to atom_type=="Xe") or atom_index==0', "first"),
    ],
)
def test_empty_bonded_operands_follow_set_semantics(
    alanine_molsys, topology_only, query, expected
):
    system = alanine_molsys.topology if topology_only else alanine_molsys
    result = msm.select(system, query)
    wanted = (
        np.arange(system.n_atoms if topology_only else system.topology.n_atoms)
        if expected == "all"
        else ([0] if expected == "first" else [])
    )
    np.testing.assert_array_equal(result, wanted)
    assert all(isinstance(index, (int, np.integer)) for index in result)


def test_bonded_to_an_isolated_atom_is_empty(alanine_molsys):
    # A present atom with no graph neighbors differs from an absent operand.
    system = msm.extract(alanine_molsys, selection=[0])
    assert len(msm.select(system, "all bonded to all")) == 0
    np.testing.assert_array_equal(msm.select(system, "all not bonded to all"), [0])


def test_hydrogen_free_protein_roles_and_buch_keep_explicit_empty_coverage(
    tctim_h5msm_molsys, tmp_path
):
    system = tctim_h5msm_molsys
    assert system.topology.n_atoms == 3983
    atoms_before = system.topology.atoms.copy(deep=True)
    coordinates_before = puw.get_value(system.structures.coordinates).copy()
    assert len(msm.select(system, 'atom_type=="H"')) == 0
    names, kinds, groups = msm.get(
        system, element="atom", atom_name=True, atom_type=True, group_name=True
    )
    expected = np.flatnonzero(
        np.isin(kinds, ["O", "N", "S"])
        & ~((np.asarray(names) == "NE2") & (np.asarray(groups) == "GLN"))
    )
    acceptors = msm.interactions.hbonds.get_acceptor_atoms(system)
    donors = msm.interactions.hbonds.get_donor_atoms(system)
    np.testing.assert_array_equal(acceptors, expected)
    assert donors.shape == (0, 2)
    assert donors.dtype.kind == "i"
    triples, distances = msm.interactions.hbonds.get_buch_hbonds(
        system, structure_indices=[0], pbc=False
    )
    assert len(triples) == len(distances) == 1
    assert triples[0].shape == (0, 3)
    assert puw.get_value(distances[0]).shape == (0,)
    result = msm.interactions.hbonds.get_buch_hbonds(
        system, structure_indices=[0, 0], pbc=False, output_type="molsysmt.Interactions"
    )
    assert result.n_interactions == 0
    np.testing.assert_array_equal(result.evaluated_structure_indices, [0])
    np.testing.assert_array_equal(result.evaluation_scope["atom_indices"], acceptors)
    system.interactions = {"no_explicit_hydrogens": result}
    path = tmp_path / "empty.h5msm"
    msm.convert(system, to_form=str(path))
    restored = msm.convert(str(path), to_form="molsysmt.MolSys").interactions[
        "no_explicit_hydrogens"
    ]
    assert restored.n_interactions == 0
    np.testing.assert_array_equal(restored.evaluated_structure_indices, [0])
    pd.testing.assert_frame_equal(system.topology.atoms, atoms_before)
    np.testing.assert_array_equal(
        puw.get_value(system.structures.coordinates), coordinates_before
    )
