"""Reject physical quantities at positional correspondence-axis boundaries."""

import warnings

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from tests.build.test_merge_nonpolar_hydrogens import declared_methanol

CASES = [
    (family, argument)
    for family in ["correspondences", "rmsd"]
    for argument in [
        "selection",
        "reference_selection",
        "structure_indices",
        "reference_structure_indices",
    ]
    if family != "rmsd" or argument != "reference_structure_indices"
] + [("poses", "structure_indices"), ("names", "selection")]


@pytest.mark.parametrize("family,argument", CASES)
@pytest.mark.parametrize("unit", ["nm", "dimensionless"])
def test_public_positional_axes_reject_quantity_before_unit_stripping(
    family, argument, unit, monkeypatch
):
    source = declared_methanol()
    value = msm.pyunitwizard.quantity(np.array([0], dtype=int), unit)
    from molsysmt._private import atom_name_projection, pdbqt_poses
    from molsysmt.chemical_states import _atom_correspondences

    def forbidden(*args, **kwargs):
        raise AssertionError("A quantity-valued index reached scientific/label work")

    monkeypatch.setattr(_atom_correspondences, "ChemicalGraph", forbidden)
    monkeypatch.setattr(pdbqt_poses, "read_poses", forbidden)
    monkeypatch.setattr(atom_name_projection, "project", forbidden)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with pytest.raises(ArgumentError):
            if family == "correspondences":
                msm.chemical_states.get_atom_correspondences(
                    source, **{argument: value}
                )
            elif family == "rmsd":
                msm.structure.get_symmetry_corrected_rmsd(source, **{argument: value})
            elif family == "names":
                msm.build.project_atom_names(
                    source, target_form="file:pdbqt", **{argument: value}
                )
            else:
                msm.form.string_pdbqt_text.read_poses(
                    "pdbqt_text:END\n", source, {}, **{argument: value}
                )

    assert not caught


@pytest.mark.parametrize("unit", ["nm", "dimensionless"])
def test_flat_sequence_does_not_strip_units_from_quantity_members(unit):
    from molsysmt._private.argdigest.argument._correspondence_axes import flat_axis

    value = [msm.pyunitwizard.quantity(0, unit)]
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with pytest.raises(ArgumentError):
            flat_axis(value, "selection", "control")
    assert not caught


def test_plain_integer_axis_and_empty_axis_remain_supported():
    from molsysmt._private.argdigest.argument._correspondence_axes import flat_axis

    assert flat_axis(np.array([0, 2]), "selection", "control").tolist() == [0, 2]
    result = flat_axis([], "structure_indices", "control")
    assert result.dtype == np.int64 and result.shape == (0,)
