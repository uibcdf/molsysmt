"""Tests for the shared amino-acid residue-code authority."""

import pytest

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
    assert get_1_letter_code_from_name("XLE") == "J"
    assert get_1_letter_code_from_name("XAA") == "X"
    assert get_1_letter_code_from_name("SEC") == "U"
    assert get_1_letter_code_from_name("PYL") == "O"


@pytest.mark.parametrize(("name", "expected"), aa3_to_aa1.items())
def test_every_declared_canonical_and_ambiguity_code_is_reachable(name, expected):
    assert get_1_letter_code_from_name(name) == expected


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("MSE", "M"),
        ("SEP", "S"),
        ("TPO", "T"),
        ("PTR", "Y"),
        ("DAL", "A"),
        ("HIP", "H"),
        ("HIA", "H"),
        ("ASH", "D"),
        ("DGL", "E"),
        ("UNK", "X"),
        ("XPL", "O"),
    ],
)
def test_supported_modified_and_protonation_labels_keep_their_codes(name, expected):
    assert get_1_letter_code_from_name(name) == expected


@pytest.mark.parametrize("name", ["xle", "ala", "Ala", "HOH", "UNKNOWN", "", None])
def test_unsupported_and_case_sensitive_inputs_keep_explicit_errors(name):
    with pytest.raises(KeyError):
        get_1_letter_code_from_name(name)
