"""Checking label decoding independently of chemical type assignment."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError


def test_named_autodock_dictionary_and_empty_input():
    decode = msm.element.atom.get_atom_type_from_atom_ff_type
    assert decode("A") == "C"
    assert decode(["NA", "OA", "SA", "HD", "Cl", "Ca", "Zn"]) == [
        "N",
        "O",
        "S",
        "H",
        "Cl",
        "Ca",
        "Zn",
    ]
    assert decode(np.array(["C", "A"])) == ["C", "C"]
    assert decode([]) == []


@pytest.mark.parametrize(
    "labels", ["G0", "CG0", "W", "ca", "UNK", None, 3, [["A"]], ["A", None]]
)
def test_rejects_pseudoatoms_custom_labels_and_bad_shapes(labels):
    with pytest.raises(ArgumentError):
        msm.element.atom.get_atom_type_from_atom_ff_type(labels)


@pytest.mark.parametrize("scheme", ["amber", None])
def test_scheme_is_explicit_and_validated_even_for_empty_input(scheme):
    with pytest.raises(ArgumentError):
        msm.element.atom.get_atom_type_from_atom_ff_type([], typing_scheme=scheme)
