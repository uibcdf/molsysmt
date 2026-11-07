"""Protect transform ownership across borrowed XYZ and native coordinate storage."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import MolSys, Structures

XYZ = np.arange(36, dtype=float).reshape(3, 4, 3) / 10
QUARTER_TURN = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
SHIFT = np.array([0.25, 0.5, -0.75])


def system(form, unit):
    coordinates = puw.convert(puw.quantity(XYZ.copy(), "nm"), to_unit=unit)
    if form == "XYZ":
        return coordinates
    structures = Structures(coordinates=coordinates)
    if form == "Structures":
        return structures
    output = MolSys(n_atoms=4)
    output.structures = structures
    return output


def values(item):
    return puw.get_value(msm.get(item, element="atom", coordinates=True), to_unit="nm")


def parameters(operation):
    if operation == "rotate":
        return {"rotation": QUARTER_TURN}
    return {"translation": puw.quantity(SHIFT, "nm")}


@pytest.mark.parametrize("form", ["XYZ", "Structures", "MolSys"])
@pytest.mark.parametrize("unit", ["nm", "angstrom"])
@pytest.mark.parametrize("operation", ["rotate", "translate"])
@pytest.mark.parametrize("subset", [False, True])
@pytest.mark.parametrize("in_place", [False, True])
def test_transform_publishes_only_to_its_declared_owner(
    form, unit, operation, subset, in_place
):
    source = system(form, unit)
    before = values(source).copy()
    atoms, structures = ([3, 1], [2, 0]) if subset else (list(range(4)), list(range(3)))
    chosen = before[structures][:, atoms]
    expected = before.copy()
    transformed = (
        np.stack((-chosen[..., 1], chosen[..., 0], chosen[..., 2]), axis=-1)
        if operation == "rotate"
        else chosen + SHIFT
    )
    expected[np.ix_(structures, atoms, np.arange(3))] = transformed
    selection = atoms if subset else "all"
    structure_indices = structures if subset else "all"
    result = getattr(msm.structure, operation)(
        source,
        selection=selection,
        structure_indices=structure_indices,
        in_place=in_place,
        **parameters(operation),
    )
    if in_place:
        assert result is None
        output = source
    else:
        assert result is not source
        output = result
        np.testing.assert_array_equal(values(source), before)
        assert not np.shares_memory(values(output), values(source))
    np.testing.assert_allclose(values(output), expected, rtol=0, atol=1e-12)


@pytest.mark.parametrize("operation", ["rotate", "translate"])
def test_independent_transform_accepts_readonly_xyz_without_changing_it(operation):
    source = system("XYZ", "nm")
    puw.get_value(source).setflags(write=False)
    before = values(source).copy()
    output = getattr(msm.structure, operation)(source, **parameters(operation))
    assert np.all(np.isfinite(values(output)))
    np.testing.assert_array_equal(values(source), before)
    assert not puw.get_value(source).flags.writeable
    assert not np.shares_memory(values(output), values(source))


@pytest.mark.parametrize("form", ["XYZ", "Structures", "MolSys"])
@pytest.mark.parametrize("in_place", [False, True])
def test_rotation_protocol_failure_after_one_structure_preserves_source(form, in_place):
    class InterruptedRotation:
        def __init__(self):
            self.calls = 0

        def apply(self, coordinates):
            self.calls += 1
            coordinates += 1
            if self.calls == 2:
                raise RuntimeError("controlled second-structure failure")
            return coordinates

    source = system(form, "nm")
    before = values(source).copy()
    rotation = InterruptedRotation()
    with pytest.raises(RuntimeError, match="controlled second-structure failure"):
        msm.structure.rotate(source, rotation=rotation, in_place=in_place)
    assert rotation.calls == 2
    np.testing.assert_array_equal(values(source), before)


@pytest.mark.parametrize("unit", ["nm", "angstrom"])
def test_fixed_center_rotation_preserves_xyz_source_and_uses_captured_center(unit):
    source = system("XYZ", unit)
    before = values(source).copy()
    center = np.array([1.0, 1.0, 0.0])
    output = msm.structure.rotate(
        source, rotation=QUARTER_TURN, rotation_center=puw.quantity(center, "nm")
    )
    relative = before - center
    expected = (
        np.stack((-relative[..., 1], relative[..., 0], relative[..., 2]), axis=-1)
        + center
    )
    np.testing.assert_allclose(values(output), expected, rtol=0, atol=1e-12)
    np.testing.assert_array_equal(values(source), before)
