"""
Tests for add_missing_terminal_cappings with engine='MolSysMT'.

No external dependencies (no tleap, no PDBFixer required).
Uses build_peptide(engine='MolSysMT') as the input source.
"""

import pytest
import numpy as np
import molsysmt as msm


@pytest.fixture(scope="module")
def avp_molsys():
    return msm.build.build_peptide('AlaValPro', engine='MolSysMT', to_form='molsysmt.MolSys')


class TestAddMissingTerminalCappingsEngMolSysMT:

    def test_case_a_oxt_added(self, avp_molsys):
        """Case A adds OXT to the free C-terminus.

        build_peptide produces AlaValPro without OXT; calling
        add_missing_terminal_cappings with no caps completes the terminal
        residue by adding 1 OXT atom.
        """
        n_before = msm.get(avp_molsys, n_atoms=True)
        result = msm.build.add_missing_terminal_cappings(avp_molsys, engine='MolSysMT')
        assert msm.get(result, n_atoms=True) == n_before + 1

    def test_case_a_no_cappings_groups_unchanged(self, avp_molsys):
        """Group names must remain ['ALA', 'VAL', 'PRO'] when no cappings are requested."""
        result = msm.build.add_missing_terminal_cappings(avp_molsys, engine='MolSysMT')
        groups = msm.get(result, element='group', group_name=True)
        assert groups == ['ALA', 'VAL', 'PRO']

    def test_case_b_ace_nme_group_order(self, avp_molsys):
        """Adding ACE and NME must produce groups in order ACE, ALA, VAL, PRO, NME."""
        result = msm.build.add_missing_terminal_cappings(
            avp_molsys, N_terminal='ACE', C_terminal='NME', engine='MolSysMT'
        )
        groups = msm.get(result, element='group', group_name=True)
        assert groups == ['ACE', 'ALA', 'VAL', 'PRO', 'NME']

    def test_case_b_ace_nme_atom_count(self, avp_molsys):
        """ACE adds 3 heavy atoms (C, O, CH3), NME adds 2 (N, C): total +5."""
        n_before = msm.get(avp_molsys, n_atoms=True)
        result = msm.build.add_missing_terminal_cappings(
            avp_molsys, N_terminal='ACE', C_terminal='NME', engine='MolSysMT'
        )
        assert msm.get(result, n_atoms=True) == n_before + 5

    def test_case_b_ace_only(self, avp_molsys):
        """Adding only ACE must produce groups ['ACE', 'ALA', 'VAL', 'PRO']."""
        result = msm.build.add_missing_terminal_cappings(
            avp_molsys, N_terminal='ACE', C_terminal=None, engine='MolSysMT'
        )
        groups = msm.get(result, element='group', group_name=True)
        assert groups == ['ACE', 'ALA', 'VAL', 'PRO']

    def test_case_b_nme_only(self, avp_molsys):
        """Adding only NME must produce groups ['ALA', 'VAL', 'PRO', 'NME']."""
        result = msm.build.add_missing_terminal_cappings(
            avp_molsys, N_terminal=None, C_terminal='NME', engine='MolSysMT'
        )
        groups = msm.get(result, element='group', group_name=True)
        assert groups == ['ALA', 'VAL', 'PRO', 'NME']

    def test_case_b_ace_nme_peptide_bonds_exist(self, avp_molsys):
        """ACE.C must be bonded to first residue N, last residue C must be bonded to NME.N."""
        result = msm.build.add_missing_terminal_cappings(
            avp_molsys, N_terminal='ACE', C_terminal='NME', engine='MolSysMT'
        )
        topo = result.topology
        bonds = topo.bonds

        ace_C_idx = topo.atoms[
            (topo.atoms['group_index'] == 0) & (topo.atoms['atom_name'] == 'C')
        ].index[0]
        ala_N_idx = topo.atoms[
            (topo.atoms['group_index'] == 1) & (topo.atoms['atom_name'] == 'N')
        ].index[0]
        pro_C_idx = topo.atoms[
            (topo.atoms['group_index'] == 3) & (topo.atoms['atom_name'] == 'C')
        ].index[0]
        nme_N_idx = topo.atoms[
            (topo.atoms['group_index'] == 4) & (topo.atoms['atom_name'] == 'N')
        ].index[0]

        def bond_exists(i, j):
            a, b = min(i, j), max(i, j)
            return ((bonds['atom1_index'] == a) & (bonds['atom2_index'] == b)).any()

        assert bond_exists(ace_C_idx, ala_N_idx), "ACE.C – ALA.N bond missing"
        assert bond_exists(pro_C_idx, nme_N_idx), "PRO.C – NME.N bond missing"
