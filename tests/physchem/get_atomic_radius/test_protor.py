"""
Unit tests for ProtOr atom typing and van der Waals radii in molsysmt.physchem.
"""

import molsysmt as msm
from molsysmt import pyunitwizard as puw
import numpy as np
import pytest


def test_protor_atom_typing_standard_amino_acids():
    """Test ProtOr atom typing for standard and capped amino acids."""
    # Build a peptide with diverse residue types
    molsys = msm.build.build_peptide('AlaValProCysMet', engine='MolSysMT')

    # Get ProtOr atom types and provenance rules
    protor_types, rules = msm.physchem.get_protor_atom_type(molsys)

    # Convert to array of names to locate specific atoms
    atom_names = np.asarray(msm.get(molsys, element='atom', atom_name=True), dtype=str)
    group_names = np.asarray(msm.get(molsys, element='atom', group_name=True), dtype=str)

    # 1. Check ALA CB (should be C4H3)
    ala_cb_idx = np.where((group_names == 'ALA') & (atom_names == 'CB'))[0][0]
    assert protor_types[ala_cb_idx] == 'C4H3'
    assert rules[ala_cb_idx] == 'protein_heavy'

    # 2. Check ALA CA (should be C4H1)
    ala_ca_idx = np.where((group_names == 'ALA') & (atom_names == 'CA'))[0][0]
    assert protor_types[ala_ca_idx] == 'C4H1'
    assert rules[ala_ca_idx] == 'protein_backbone'

    # 3. Check GLY CA fallback in backbone logic
    molsys_gly = msm.build.build_peptide('Gly', engine='MolSysMT')
    gly_types, _ = msm.physchem.get_protor_atom_type(molsys_gly)
    gly_names = np.asarray(msm.get(molsys_gly, element='atom', atom_name=True), dtype=str)
    gly_ca_idx = np.where(gly_names == 'CA')[0][0]
    assert gly_types[gly_ca_idx] == 'C4H2'

    # 4. Check PRO N (should be N3H0)
    pro_n_idx = np.where((group_names == 'PRO') & (atom_names == 'N'))[0][0]
    assert protor_types[pro_n_idx] == 'N3H0'
    assert rules[pro_n_idx] == 'protein_backbone'

    # 5. Check CYS SG (should be S2H1 since it is free thiol)
    cys_sg_idx = np.where((group_names == 'CYS') & (atom_names == 'SG'))[0][0]
    assert protor_types[cys_sg_idx] == 'S2H1'

    # 6. Check MET SD (should be S2H0)
    met_sd_idx = np.where((group_names == 'MET') & (atom_names == 'SD'))[0][0]
    assert protor_types[met_sd_idx] == 'S2H0'


def test_protor_hydrogen_independence_parity():
    """Verify that explicit hydrogen presence does not affect heavy-atom ProtOr assignment."""
    # Build a peptide (typically comes with explicit hydrogens)
    peptide_with_h = msm.build.build_peptide('AlaValProTrpTyr', engine='MolSysMT')

    # Create a heavy-atom-only version by selecting non-hydrogens
    peptide_no_h = msm.convert(peptide_with_h, selection="atom_type != 'H'")

    # Select heavy atoms in the hydrogen-containing system
    heavy_selection_with_h = msm.select(peptide_with_h, selection="atom_type != 'H'")

    # Run ProtOr typing on both systems
    types_with_h, rules_with_h = msm.physchem.get_protor_atom_type(
        peptide_with_h, selection=heavy_selection_with_h
    )
    types_no_h, rules_no_h = msm.physchem.get_protor_atom_type(peptide_no_h)

    # Heavy atom count should match
    assert len(types_with_h) == len(types_no_h)

    # Assigned types and rules must be identical
    assert np.array_equal(types_with_h, types_no_h)
    assert np.array_equal(rules_with_h, rules_no_h)


def test_protor_vdw_radii_retrieval():
    """Test get_atomic_radius with definition='protor'."""
    molsys = msm.build.build_peptide('AlaValPro', engine='MolSysMT')

    # Retrieve radii via physical chemistry public entry point
    radii = msm.physchem.get_atomic_radius(molsys, definition='protor')

    # Should be a PyUnitWizard quantity in nanometers
    assert puw.is_quantity(radii)
    assert puw.get_unit(radii) == puw.unit('nm')

    # Convert to array for check
    val_array = puw.get_value(radii)

    atom_names = np.asarray(msm.get(molsys, element='atom', atom_name=True), dtype=str)
    group_names = np.asarray(msm.get(molsys, element='atom', group_name=True), dtype=str)
    atom_types = np.asarray(msm.get(molsys, element='atom', atom_type=True), dtype=str)

    # 1. Check ALA CA (C4H1: 1.88 A -> 0.188 nm)
    ala_ca_idx = np.where((group_names == 'ALA') & (atom_names == 'CA'))[0][0]
    assert np.allclose(val_array[ala_ca_idx], 0.188)

    # 2. Check ALA CB (C4H3: 1.88 A -> 0.188 nm)
    ala_cb_idx = np.where((group_names == 'ALA') & (atom_names == 'CB'))[0][0]
    assert np.allclose(val_array[ala_cb_idx], 0.188)

    # 3. Check ALA C (C3H0: 1.61 A -> 0.161 nm)
    ala_c_idx = np.where((group_names == 'ALA') & (atom_names == 'C'))[0][0]
    assert np.allclose(val_array[ala_c_idx], 0.161)

    # 4. Check ALA O (O1H0: 1.42 A -> 0.142 nm)
    ala_o_idx = np.where((group_names == 'ALA') & (atom_names == 'O'))[0][0]
    assert np.allclose(val_array[ala_o_idx], 0.142)

    # 5. Check Hydrogen atoms (ignored by ProtOr -> default H radius is 0.11 nm)
    h_indices = np.where(atom_types == 'H')[0]
    for idx in h_indices:
        assert np.allclose(val_array[idx], 0.11)
