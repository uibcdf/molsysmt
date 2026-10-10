"""Protecting full atom axes and manual mechanical type edits on MolSys."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import MolSys


@pytest.fixture(params=["full", "structures_only"])
def molsys(request):
    output = MolSys(n_atoms=4)
    output.structures.coordinates = puw.quantity(
        np.arange(24, dtype=float).reshape(2, 4, 3), "nm"
    )
    if request.param == "structures_only":
        output = MolSys._from_partial_domains(structures=output.structures)
    return output


def test_set_types_preserves_full_axis_and_unrelated_domains(molsys):
    coordinates = puw.get_value(molsys.structures.coordinates).copy()
    chemistry = molsys.chemical_states
    molsys.molecular_mechanics.partial_charge = [0.1, 0.2, 0.3, 0.4]

    assert msm.set(molsys, element="atom", atom_ff_type=["C", "O", "N", "H"]) is None

    assert msm.get(molsys, element="atom", atom_ff_type=True).tolist() == [
        "C",
        "O",
        "N",
        "H",
    ]
    assert molsys.molecular_mechanics.atoms_ff.index.tolist() == [0, 1, 2, 3]
    assert molsys.molecular_mechanics.partial_charge.tolist() == [0.1, 0.2, 0.3, 0.4]
    assert molsys.chemical_states is chemistry
    np.testing.assert_array_equal(
        puw.get_value(molsys.structures.coordinates), coordinates
    )


def test_subset_types_allocate_full_source_axis_in_selection_order(molsys):
    msm.set(molsys, element="atom", selection=[3, 1], atom_ff_type=["H", "O"])

    values = molsys.molecular_mechanics.atom_ff_type
    assert len(values) == 4
    assert values[1] == "O" and values[3] == "H"
    assert pd.isna(values[0]) and pd.isna(values[2])
    assert molsys.molecular_mechanics.atoms_ff.index.tolist() == [0, 1, 2, 3]


def test_clear_types_preserves_charges(molsys):
    molsys.molecular_mechanics.partial_charge = [0.1, 0.2, 0.3, 0.4]
    molsys.molecular_mechanics.atom_ff_type = ["C", "O", "N", "H"]

    msm.set(molsys, element="atom", atom_ff_type=None)

    assert molsys.molecular_mechanics.atom_ff_type is None
    assert molsys.molecular_mechanics.partial_charge.tolist() == [0.1, 0.2, 0.3, 0.4]


def test_empty_selection_does_not_allocate_storage(molsys):
    msm.set(molsys, element="atom", selection=[], atom_ff_type=[])

    assert molsys.molecular_mechanics.atoms_ff is None


@pytest.mark.parametrize(
    "selection,value",
    [
        ("all", ["C"]),
        ("all", [["C", "O"], ["N", "H"]]),
        ("all", "C"),
        ([3, 1], ["C"]),
        ([3, 1], None),
        ([4], ["C"]),
        ([-1], ["C"]),
    ],
)
def test_invalid_type_edit_fails_before_allocation(molsys, selection, value):
    with pytest.raises(ArgumentError):
        msm.set(molsys, element="atom", selection=selection, atom_ff_type=value)

    assert molsys.molecular_mechanics.atoms_ff is None


def test_inconsistent_mechanical_axis_fails_before_mutation(molsys):
    molsys.molecular_mechanics.partial_charge = [0.1, 0.2]
    original = molsys.molecular_mechanics.atoms_ff.copy(deep=True)

    with pytest.raises(StructuralInconsistencyError):
        msm.set(molsys, element="atom", atom_ff_type=["C", "O", "N", "H"])

    pd.testing.assert_frame_equal(molsys.molecular_mechanics.atoms_ff, original)
