"""
Tests for add_missing_heavy_atoms with engine='MolSysMT'.

No external dependencies (no tleap, no PDBFixer required).
Uses build_peptide(engine='MolSysMT') as the input source.
"""

import pytest
import molsysmt as msm


@pytest.fixture(scope="module")
def aaa_molsys():
    return msm.build.build_peptide('AAA', engine='MolSysMT', to_form='molsysmt.MolSys')


class TestAddMissingHeavyAtomsEngMolSysMT:

    def test_restores_atom_count(self, aaa_molsys):
        """Removing CB from each ALA and restoring must recover the original count."""
        n_before = msm.get(aaa_molsys, n_atoms=True)
        molsys_no_cb = msm.remove(aaa_molsys, selection='atom_name=="CB"')
        assert msm.get(molsys_no_cb, n_atoms=True) == n_before - 3
        restored = msm.build.add_missing_heavy_atoms(molsys_no_cb, engine='MolSysMT')
        assert msm.get(restored, n_atoms=True) == n_before

    def test_missing_detection_consistent(self, aaa_molsys):
        """get_missing_heavy_atoms must report CB missing for all three ALA residues."""
        molsys_no_cb = msm.remove(aaa_molsys, selection='atom_name=="CB"')
        missing = msm.build.get_missing_heavy_atoms(molsys_no_cb, engine='MolSysMT')
        assert set(missing.keys()) == {0, 1, 2}
        assert all(v == ['CB'] for v in missing.values())

    def test_cb_atoms_present_after_restore(self, aaa_molsys):
        """After restoring, exactly 3 CB atoms must be present."""
        molsys_no_cb = msm.remove(aaa_molsys, selection='atom_name=="CB"')
        restored = msm.build.add_missing_heavy_atoms(molsys_no_cb, engine='MolSysMT')
        n_cb = msm.get(restored, element='atom', selection='atom_name=="CB"', n_atoms=True)
        assert n_cb == 3

    def test_no_missing_atoms_returns_unchanged(self, aaa_molsys):
        """Calling on a complete system must return the same atom count."""
        n_before = msm.get(aaa_molsys, n_atoms=True)
        result = msm.build.add_missing_heavy_atoms(aaa_molsys, engine='MolSysMT')
        assert msm.get(result, n_atoms=True) == n_before

    def test_cb_bonded_to_ca_after_restore(self, aaa_molsys):
        """Restored CB atoms must be bonded to CA (bond count increases accordingly)."""
        molsys_no_cb = msm.remove(aaa_molsys, selection='atom_name=="CB"')
        n_bonds_before = molsys_no_cb.topology.bonds.shape[0]
        restored = msm.build.add_missing_heavy_atoms(molsys_no_cb, engine='MolSysMT')
        n_bonds_after = restored.topology.bonds.shape[0]
        # Each CB adds 1 bond (CB-CA) — CB hydrogens are not heavy atoms
        assert n_bonds_after == n_bonds_before + 3
