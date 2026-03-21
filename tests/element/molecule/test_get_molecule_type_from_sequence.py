"""
Tests for get_molecule_type_from_sequence (0% coverage).
"""

from molsysmt.element.molecule._get_molecule_type_from_sequence import get_molecule_type_from_sequence


def test_dna_sequence():
    assert get_molecule_type_from_sequence('GATCGATC') == 'dna'


def test_rna_sequence():
    assert get_molecule_type_from_sequence('GAUCGAUC') == 'rna'


def test_protein_sequence():
    assert get_molecule_type_from_sequence('ACDEFGHIKLMNPQRSTVWY') == 'protein'


def test_single_dna_base():
    assert get_molecule_type_from_sequence('GGGG') == 'dna'


def test_mixed_sequence_is_protein():
    assert get_molecule_type_from_sequence('MNIFEML') == 'protein'
