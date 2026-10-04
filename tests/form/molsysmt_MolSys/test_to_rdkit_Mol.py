"""
Tests for molsysmt.MolSys → rdkit.Mol conversion.

Covers:
- Full conversion: atom/bond count, conformer count
- Non-contiguous atom subset: correct local atom count (regression for abs→local index bug)
- No self-bonds in the resulting molecule
- Coordinate conformers: shape and dtype
"""

import numpy as np
import pytest

import molsysmt as msm


@pytest.mark.parametrize("residue_name", ["HID", "HIE", "TRP"])
def test_declared_no_implicit_hydrogen_policy_survives_aromatic_nh_sanitization(
    residue_name,
):
    pytest.importorskip("rdkit")
    molsys = msm.physchem.get_peptide_chemical_template(
        [residue_name], "ammonium", "carboxylate"
    )["template"]
    fields = molsys.chemical_states._states[0].atom_attributes
    expected_counts = fields["n_explicit_hydrogens"].to_numpy(dtype=int)
    result = msm.convert(molsys, to_form="rdkit.Mol")
    assert all(atom.GetNoImplicit() for atom in result.GetAtoms())
    np.testing.assert_array_equal(
        [atom.GetNumExplicitHs() for atom in result.GetAtoms()], expected_counts
    )
    assert all(atom.GetNumImplicitHs() == 0 for atom in result.GetAtoms())


@pytest.mark.tier3
class TestToRdkitMolFullConversion:
    """Full conversion of a small molecular system."""

    def test_atom_count(self, proline_molsys):
        rdmol = msm.convert(proline_molsys, to_form="rdkit.Mol")
        n_atoms = msm.get(proline_molsys, element="system", n_atoms=True)
        assert rdmol.GetNumAtoms() == n_atoms

    def test_conformer_count(self, proline_molsys):
        rdmol = msm.convert(proline_molsys, to_form="rdkit.Mol")
        n_structures = msm.get(proline_molsys, element="system", n_structures=True)
        assert rdmol.GetNumConformers() == n_structures

    def test_conformer_shape(self, proline_molsys):
        rdmol = msm.convert(proline_molsys, to_form="rdkit.Mol")
        n_atoms = msm.get(proline_molsys, element="system", n_atoms=True)
        conf = rdmol.GetConformer(0)
        positions = conf.GetPositions()
        assert positions.shape == (n_atoms, 3)

    def test_no_self_bonds(self, proline_molsys):
        rdmol = msm.convert(proline_molsys, to_form="rdkit.Mol")
        for bond in rdmol.GetBonds():
            assert bond.GetBeginAtomIdx() != bond.GetEndAtomIdx()

    def test_bond_count(self, proline_molsys):
        rdmol = msm.convert(proline_molsys, to_form="rdkit.Mol")
        n_bonds = msm.get(proline_molsys, element="system", n_bonds=True)
        assert rdmol.GetNumBonds() == n_bonds


@pytest.mark.tier3
class TestToRdkitMolSubset:
    """Non-contiguous atom subset — regression for abs→local index bug.

    Atoms 5, 10, 15, 20 are non-contiguous; their absolute indices differ from
    the local (rdkit) indices 0, 1, 2, 3.  The old code used enumerate() over
    the neighbor list which returned absolute neighbour node ids, causing
    incorrect bond indices and an rdkit AddBond crash.
    """

    def test_subset_atom_count(self, proline_molsys):
        selection = [5, 10, 15, 20]
        rdmol = msm.convert(proline_molsys, to_form="rdkit.Mol", selection=selection)
        assert rdmol.GetNumAtoms() == len(selection)

    def test_subset_no_self_bonds(self, proline_molsys):
        selection = [5, 10, 15, 20]
        rdmol = msm.convert(proline_molsys, to_form="rdkit.Mol", selection=selection)
        for bond in rdmol.GetBonds():
            assert bond.GetBeginAtomIdx() != bond.GetEndAtomIdx()

    def test_subset_bond_indices_in_range(self, proline_molsys):
        """All bond endpoint indices must be valid local indices (< n_atoms_selected)."""
        selection = [3, 7, 12, 18, 22]
        rdmol = msm.convert(proline_molsys, to_form="rdkit.Mol", selection=selection)
        n_local = len(selection)
        for bond in rdmol.GetBonds():
            assert bond.GetBeginAtomIdx() < n_local
            assert bond.GetEndAtomIdx() < n_local
