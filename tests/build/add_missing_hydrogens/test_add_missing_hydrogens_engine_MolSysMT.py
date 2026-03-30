"""
Tests for add_missing_hydrogens with engine='MolSysMT'.

No external dependencies (no OpenMM, no PDBFixer required).
Uses build_peptide(engine='MolSysMT') as the input source.
"""

import pytest
import molsysmt as msm


@pytest.fixture(scope="module")
def avp_heavy():
    """AlaValPro peptide with all H atoms removed."""
    molsys = msm.build.build_peptide('AlaValPro', engine='MolSysMT', to_form='molsysmt.MolSys')
    return msm.remove(molsys, selection='atom_type=="H"')


@pytest.fixture(scope="module")
def avp_full():
    """AlaValPro peptide as built (already contains H atoms)."""
    return msm.build.build_peptide('AlaValPro', engine='MolSysMT', to_form='molsysmt.MolSys')


class TestAddMissingHydrogensEngMolSysMT:

    def test_round_trip_atom_count(self, avp_heavy, avp_full):
        """Restoring H on heavy-only system must recover the original atom count."""
        restored = msm.build.add_missing_hydrogens(avp_heavy, engine='MolSysMT')
        assert msm.get(restored, n_atoms=True) == msm.get(avp_full, n_atoms=True)

    def test_round_trip_h_count(self, avp_heavy, avp_full):
        """Number of H atoms after restoration must match the original."""
        restored = msm.build.add_missing_hydrogens(avp_heavy, engine='MolSysMT')
        n_h_restored = msm.get(restored, element='atom', selection='atom_type=="H"', n_atoms=True)
        n_h_orig = msm.get(avp_full, element='atom', selection='atom_type=="H"', n_atoms=True)
        assert n_h_restored == n_h_orig

    def test_no_missing_h_returns_unchanged(self, avp_full):
        """Calling on a system that already has all H must not add any atoms."""
        n_before = msm.get(avp_full, n_atoms=True)
        result = msm.build.add_missing_hydrogens(avp_full, engine='MolSysMT')
        assert msm.get(result, n_atoms=True) == n_before

    def test_group_names_unchanged(self, avp_heavy):
        """Group names must remain ['ALA', 'VAL', 'PRO'] after H addition."""
        restored = msm.build.add_missing_hydrogens(avp_heavy, engine='MolSysMT')
        groups = msm.get(restored, element='group', group_name=True)
        assert groups == ['ALA', 'VAL', 'PRO']

    def test_h_atoms_bonded_to_heavy(self, avp_heavy):
        """Every H atom in the restored system must have at least one bond to a heavy atom."""
        restored = msm.build.add_missing_hydrogens(avp_heavy, engine='MolSysMT')
        topo = restored.topology
        bonds = topo.bonds

        bonded_atoms = set()
        for _, brow in bonds.iterrows():
            bonded_atoms.add(int(brow['atom1_index']))
            bonded_atoms.add(int(brow['atom2_index']))

        h_indices = topo.atoms[topo.atoms['atom_type'] == 'H'].index.tolist()
        for h_idx in h_indices:
            assert h_idx in bonded_atoms, f"H atom {h_idx} has no bond"

    def test_ala_has_backbone_hn(self, avp_heavy):
        """ALA (N-terminal) must have backbone H after restoration."""
        restored = msm.build.add_missing_hydrogens(avp_heavy, engine='MolSysMT')
        topo = restored.topology
        ala_g = 0   # ALA is the first group
        ala_atoms = topo.atoms[topo.atoms['group_index'] == ala_g]['atom_name'].tolist()
        # At least one backbone NH hydrogen must be present (named H, HN, or similar)
        backbone_hs = [a for a in ala_atoms if a in ('H', 'HN')]
        assert len(backbone_hs) >= 1, f"No backbone H in ALA: {ala_atoms}"

    def test_pro_no_backbone_hn(self, avp_heavy):
        """PRO must not have a backbone HN (N is in the ring, no HN in template)."""
        restored = msm.build.add_missing_hydrogens(avp_heavy, engine='MolSysMT')
        topo = restored.topology
        # PRO is the last group (index 2)
        pro_g = 2
        pro_atoms = topo.atoms[topo.atoms['group_index'] == pro_g]['atom_name'].tolist()
        backbone_hn = [a for a in pro_atoms if a in ('H', 'HN')]
        assert len(backbone_hn) == 0, f"PRO should not have backbone HN: {pro_atoms}"

    def test_partial_h_only_missing_added(self, avp_full):
        """If only CB hydrogens are removed, only those should be restored."""
        # ALA has HB1, HB2, HB3; remove just those three
        no_hb = msm.remove(avp_full, selection='atom_name in ["HB1", "HB2", "HB3"] and group_name=="ALA"')
        n_before = msm.get(no_hb, n_atoms=True)
        restored = msm.build.add_missing_hydrogens(no_hb, engine='MolSysMT')
        assert msm.get(restored, n_atoms=True) == n_before + 3


@pytest.fixture(scope="module")
def capped_ala_heavy():
    """ACE-ALA-NME with all H atoms removed (heavy atoms only)."""
    mol = msm.build.build_peptide('ALA', engine='MolSysMT', to_form='molsysmt.MolSys')
    mol = msm.build.add_missing_terminal_cappings(mol, N_terminal='ACE', C_terminal='NME', engine='MolSysMT')
    return msm.remove(mol, selection='atom_type=="H"')


@pytest.fixture(scope="module")
def capped_ala_full():
    """ACE-ALA-NME with all H atoms (reference)."""
    mol = msm.build.build_peptide('ALA', engine='MolSysMT', to_form='molsysmt.MolSys')
    return msm.build.add_missing_terminal_cappings(mol, N_terminal='ACE', C_terminal='NME', engine='MolSysMT')


class TestAddMissingHydrogensCapGroups:

    def test_ace_h_atoms_placed(self, capped_ala_heavy):
        """ACE methyl H atoms (HH31, HH32, HH33) must be placed on pre-existing ACE group."""
        restored = msm.build.add_missing_hydrogens(capped_ala_heavy, engine='MolSysMT')
        names = msm.get(restored, element='atom', selection='all', atom_name=True)
        for h in ('HH31', 'HH32', 'HH33'):
            assert h in names, f"Missing {h} after H restoration"

    def test_nme_h_atoms_placed(self, capped_ala_heavy):
        """NME H atoms (H, H1, H2, H3) must be placed on pre-existing NME group."""
        restored = msm.build.add_missing_hydrogens(capped_ala_heavy, engine='MolSysMT')
        names = msm.get(restored, element='atom', selection='all', atom_name=True)
        for h in ('H', 'H1', 'H2', 'H3'):
            assert h in names, f"Missing NME {h} after H restoration"

    def test_round_trip_atom_count(self, capped_ala_heavy, capped_ala_full):
        """Atom count after H restoration must match the fully capped reference."""
        restored = msm.build.add_missing_hydrogens(capped_ala_heavy, engine='MolSysMT')
        assert msm.get(restored, n_atoms=True) == msm.get(capped_ala_full, n_atoms=True)

    def test_no_change_when_h_already_present(self, capped_ala_full):
        """Calling on a system that already has all H must not add any atoms."""
        n_before = msm.get(capped_ala_full, n_atoms=True)
        result = msm.build.add_missing_hydrogens(capped_ala_full, engine='MolSysMT')
        assert msm.get(result, n_atoms=True) == n_before

    def test_ace_h_bonded_to_ch3(self, capped_ala_heavy):
        """ACE H atoms must be bonded to CH3, not to any other atom."""
        restored = msm.build.add_missing_hydrogens(capped_ala_heavy, engine='MolSysMT')
        topo = restored.topology
        bonds = topo.bonds
        atoms = topo.atoms
        ch3_idx = atoms[atoms['atom_name'] == 'CH3'].index[0]
        bonded_to_ch3 = set()
        for _, brow in bonds.iterrows():
            a1, a2 = int(brow['atom1_index']), int(brow['atom2_index'])
            if a1 == ch3_idx:
                bonded_to_ch3.add(a2)
            elif a2 == ch3_idx:
                bonded_to_ch3.add(a1)
        for h in ('HH31', 'HH32', 'HH33'):
            h_idx = atoms[atoms['atom_name'] == h].index[0]
            assert h_idx in bonded_to_ch3, f"{h} not bonded to CH3"
