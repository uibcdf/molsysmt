"""Prevent loss of bracket-declared hydrogen chemistry without adding atom indices."""

import numpy as np
import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.mark.parametrize("smiles", ["NC(=[NH2+])N", "c1cc[nH]c1", "[NH4+]"])
def test_bracket_hydrogen_counts_survive_native_and_h5msm_round_trip(smiles, tmp_path):
    source = Chem.MolFromSmiles(smiles)
    expected = [atom.GetNumExplicitHs() for atom in source.GetAtoms()]
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    assert msm.get(molsys, element="atom", n_explicit_hydrogens=True) == expected
    molsys.structures.append(
        coordinates=puw.quantity(np.zeros((1, len(expected), 3)), "nm")
    )
    path = str(tmp_path / "hydrogens.h5msm")
    msm.convert(molsys, to_form=path)
    assert msm.get(path, element="atom", n_explicit_hydrogens=True) == expected
    restored = msm.convert(path, to_form="molsysmt.MolSys")
    for item in (molsys, restored):
        actual = msm.convert(item, to_form="rdkit.Mol")
        assert actual.GetNumAtoms() == source.GetNumAtoms()
        assert Chem.MolToSmiles(actual) == Chem.MolToSmiles(source)
        assert [atom.GetNumExplicitHs() for atom in actual.GetAtoms()] == expected
        assert [atom.GetNumImplicitHs() for atom in actual.GetAtoms()] == [
            atom.GetNumImplicitHs() for atom in source.GetAtoms()
        ]
    chemistry = msm.convert(
        molsys.chemical_states, to_form="molsysmt.ChemicalStatesDict"
    )
    rebuilt = msm.convert(chemistry, to_form="molsysmt.ChemicalStates")
    assert (
        rebuilt._states[0].atom_attributes["n_explicit_hydrogens"].tolist() == expected
    )


def test_public_declared_count_is_distinct_from_real_bonded_hydrogen_atoms():
    molsys = msm.convert(
        Chem.AddHs(Chem.MolFromSmiles("[NH4+]")), to_form="molsysmt.MolSys"
    )
    assert len(molsys.topology.atoms) == 5
    assert msm.get(molsys, element="atom", n_explicit_hydrogens=True) == [0] * 5
    msm.set(molsys, element="atom", selection=[0], n_explicit_hydrogens=1)
    assert msm.get(
        molsys, element="atom", selection=[0], n_explicit_hydrogens=True
    ) == [1]
