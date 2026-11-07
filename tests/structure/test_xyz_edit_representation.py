"""Check geometric truth independently of the accepted XYZ storage rank and dtype."""

from importlib.util import find_spec

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.native import MolSys

ROOT_HALF = np.sqrt(0.5)
ROTATION = np.array([[ROOT_HALF, -ROOT_HALF, 0], [ROOT_HALF, ROOT_HALF, 0], [0, 0, 1]])
SHIFT = np.array([0.25, -0.5, 0.75])


def source_values(rank, dtype):
    if rank == 1:
        return np.array([1, 0, 0], dtype=dtype)
    points = np.array([[1, 0, 0], [2, 1, 0], [0, 2, 1]], dtype=dtype)
    if rank == 2:
        return points
    return np.stack([points, points + 1, points + 2])


def normalized(values):
    return values.reshape((-1, 1 if values.ndim == 1 else values.shape[-2], 3))


def scopes(rank, subset):
    atoms = [0] if rank == 1 else [2, 0]
    structures = [2, 0] if rank == 3 else [0]
    return (atoms, structures) if subset else ("all", "all")


def transformed(before, operation, selection, structure_indices):
    atoms = list(range(before.shape[1])) if selection == "all" else selection
    structures = (
        list(range(before.shape[0]))
        if structure_indices == "all"
        else structure_indices
    )
    chosen = before[structures][:, atoms]
    if operation == "rotate":
        changed = np.stack(
            (
                (chosen[..., 0] - chosen[..., 1]) / np.sqrt(2),
                (chosen[..., 0] + chosen[..., 1]) / np.sqrt(2),
                chosen[..., 2],
            ),
            axis=-1,
        )
    else:
        changed = chosen + SHIFT
    result = before.copy()
    result[np.ix_(structures, atoms, np.arange(3))] = changed
    return result


def parameters(operation):
    return (
        {"rotation": ROTATION}
        if operation == "rotate"
        else {"translation": puw.quantity(SHIFT, "nm")}
    )


@pytest.mark.parametrize("rank", [1, 2, 3])
@pytest.mark.parametrize("dtype", [np.int32, np.int64, np.float32, np.float64])
@pytest.mark.parametrize("operation", ["rotate", "translate"])
@pytest.mark.parametrize("subset", [False, True])
@pytest.mark.parametrize("in_place", [False, True])
def test_transform_respects_xyz_shape_precision_and_owner(
    rank, dtype, operation, subset, in_place
):
    original = source_values(rank, dtype)
    source = puw.quantity(original.copy(), "nm", form="pint")
    before = normalized(original).astype(np.float64)
    selection, structures = scopes(rank, subset)
    call = getattr(msm.structure, operation)
    kwargs = dict(
        selection=selection,
        structure_indices=structures,
        in_place=in_place,
        **parameters(operation),
    )
    if in_place and np.issubdtype(dtype, np.integer):
        with pytest.raises(StructuralInconsistencyError, match="integer"):
            call(source, **kwargs)
        np.testing.assert_array_equal(puw.get_value(source), original)
        return
    output = call(source, **kwargs)
    if in_place:
        assert output is None
        output = source
    else:
        np.testing.assert_array_equal(puw.get_value(source), original)
        assert not np.shares_memory(puw.get_value(source), puw.get_value(output))
    actual = puw.get_value(output, to_unit="nm")
    assert actual.shape == original.shape
    assert actual.dtype.kind == "f"
    assert puw.get_form(output) == "pint"
    if np.issubdtype(dtype, np.floating):
        assert actual.dtype == dtype
    np.testing.assert_allclose(
        normalized(actual),
        transformed(before, operation, selection, structures),
        rtol=0,
        atol=1e-6 if dtype == np.float32 else 1e-12,
    )


@pytest.mark.parametrize("rank", [1, 2, 3])
@pytest.mark.parametrize("operation", ["rotate", "translate"])
@pytest.mark.parametrize(
    "backend,module",
    [
        ("pint", "pint"),
        ("openmm.unit", "openmm"),
        ("unyt", "unyt"),
        ("astropy.units", "astropy"),
    ],
)
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize(
    "policy_form,policy_unit", [("pint", "nm"), ("openmm.unit", "angstrom")]
)
def test_xyz_edit_preserves_quantity_owner_across_application_policy(
    rank, operation, backend, module, in_place, policy_form, policy_unit
):
    if find_spec(module) is None:
        pytest.skip(f"Optional quantity backend: {module}")
    if policy_form == "openmm.unit" and find_spec("openmm") is None:
        pytest.skip("Optional application quantity backend: openmm")
    original = source_values(rank, np.float64)
    source = puw.quantity(original.copy() * 10, "angstrom", form=backend)
    selection, structures = scopes(rank, True)
    with puw.context(default_form=policy_form, standard_units=[policy_unit, "ps"]):
        output = getattr(msm.structure, operation)(
            source,
            selection=selection,
            structure_indices=structures,
            in_place=in_place,
            **parameters(operation),
        )
    if in_place:
        assert output is None
        output = source
    else:
        np.testing.assert_array_equal(puw.get_value(source), original * 10)
    assert puw.get_form(output) == backend
    assert puw.has_unit(output, "angstrom")
    np.testing.assert_allclose(
        normalized(puw.get_value(output, to_unit="nm")),
        transformed(normalized(original), operation, selection, structures),
        rtol=0,
        atol=1e-12,
    )


@pytest.mark.parametrize("rank", [1, 2, 3])
@pytest.mark.parametrize("operation", ["rotate", "translate"])
def test_integer_readonly_xyz_can_produce_a_correct_independent_result(rank, operation):
    source = puw.quantity(source_values(rank, np.int64), "nm", form="pint")
    puw.get_value(source).setflags(write=False)
    before = puw.get_value(source).copy()
    output = getattr(msm.structure, operation)(source, **parameters(operation))
    np.testing.assert_array_equal(puw.get_value(source), before)
    assert not puw.get_value(source).flags.writeable
    np.testing.assert_allclose(
        normalized(puw.get_value(output, to_unit="nm")),
        transformed(normalized(before).astype(float), operation, "all", "all"),
        rtol=0,
        atol=1e-12,
    )


@pytest.mark.parametrize("operation", ["rotate", "translate"])
def test_independent_composite_edit_promotes_only_integer_xyz_owner(operation):
    xyz = puw.quantity(source_values(3, np.int64), "nm")
    topology = MolSys(n_atoms=3).topology
    source = [topology, xyz]
    before = puw.get_value(xyz).copy()
    output = getattr(msm.structure, operation)(source, **parameters(operation))
    assert msm.get_form(output) == msm.get_form(source)
    assert output[0] is not topology
    assert output[1] is not xyz
    np.testing.assert_array_equal(puw.get_value(xyz), before)
    np.testing.assert_allclose(
        puw.get_value(output[1]),
        transformed(before.astype(float), operation, "all", "all"),
        rtol=0,
        atol=1e-12,
    )


@pytest.mark.parametrize("rank", [1, 2, 3])
def test_basic_copy_retains_integer_xyz_storage_without_transform_promotion(rank):
    source = puw.quantity(source_values(rank, np.int32), "nm")
    output = msm.copy(source)
    assert puw.get_value(output).dtype == np.int32
    assert output.shape == source.shape
    np.testing.assert_array_equal(puw.get_value(output), puw.get_value(source))
    assert not np.shares_memory(puw.get_value(source), puw.get_value(output))
