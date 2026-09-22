"""Check copying a three-letter amino-acid sequence."""

from molsysmt.form.string_amino_acids_3.copy import copy


def test_copy_returns_sequence_without_recursion():
    """The adapter delegates to the standard shallow copy function."""
    assert copy("ALA") == "ALA"
