"""Tests for the shared amino-acid residue-code authority."""

from molsysmt.element.group.amino_acid.codes import aa1_to_aa3, aa3_to_aa1
from molsysmt.element.group.amino_acid.get_1_letter_code_from_name import (
    get_1_letter_code_from_name,
)


def test_one_and_three_letter_tables_are_inverse():
    assert len(aa1_to_aa3) == len(aa3_to_aa1)
    assert {one: three for three, one in aa3_to_aa1.items()} == aa1_to_aa3
    assert aa1_to_aa3["G"] == "GLY"
    assert aa1_to_aa3["B"] == "ASX"


def test_group_name_to_one_letter_uses_the_shared_table():
    assert get_1_letter_code_from_name("GLY") == "G"
    assert get_1_letter_code_from_name("ASX") == "B"
