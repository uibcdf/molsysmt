"""
Tests for small_molecule_is_amino_acid (11% coverage).
"""

import molsysmt as msm
from molsysmt.element.group.small_molecule.small_molecule_is_amino_acid import small_molecule_is_amino_acid


def test_not_in_group_names_returns_false(hp35_pdb_molsys):
    """ALA is an amino acid name, not a small-molecule name → returns False immediately."""
    result = small_molecule_is_amino_acid(hp35_pdb_molsys, 'ALA')
    assert result is False


def test_water_is_not_amino_acid(hp35_solvated_molsys):
    """HOH is in small-molecule group_names but has no backbone atoms → False."""
    result = small_molecule_is_amino_acid(hp35_solvated_molsys, 'HOH')
    assert result is False


def test_nonexistent_name_returns_false(hp35_pdb_molsys):
    """Any name not in group_names → returns False."""
    result = small_molecule_is_amino_acid(hp35_pdb_molsys, 'DOESNOTEXIST')
    assert result is False
