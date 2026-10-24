"""Check weighted PCA against an independent population-covariance oracle."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError, ArgumentLengthError
from molsysmt.native import MolSys, Structures

XYZ = np.array(
    [
        [[0.0, 1.0, 2.0], [2.0, 0.0, 1.0], [1.0, 3.0, 0.0]],
        [[1.0, 2.0, 0.0], [0.0, 4.0, 2.0], [3.0, 1.0, 2.0]],
        [[3.0, 0.0, 1.0], [1.0, 2.0, 0.0], [2.0, 0.0, 4.0]],
        [[2.0, 3.0, 4.0], [4.0, 1.0, 3.0], [0.0, 2.0, 1.0]],
    ]
)


def system(unit="nm"):
    return Structures(
        coordinates=puw.convert(puw.quantity(XYZ.copy(), "nm"), to_unit=unit)
    )


def covariance(coordinates, weights):
    # Explicit Cartesian blocks, population normalization, no weight-sum normalization.
    flat = np.concatenate([coordinates[:, :, axis] for axis in range(3)], axis=1)
    weighted = (flat - flat.mean(axis=0)) * np.sqrt(np.tile(weights, 3))
    return weighted.T @ weighted / len(flat), weighted


def assert_eigensystem(vectors, values, expected, weighted):
    raw = puw.get_value(values, to_unit="nm**2")
    reference = np.linalg.eigvalsh(expected)[::-1]
    assert vectors.shape == expected.shape
    assert raw.shape == (len(expected),)
    np.testing.assert_allclose(raw, reference, atol=1e-12)
    np.testing.assert_allclose(vectors @ vectors.T, np.eye(len(raw)), atol=1e-12)
    # This remains meaningful for repeated eigenvalues and a degenerate null space.
    np.testing.assert_allclose(expected @ vectors.T, vectors.T * raw, atol=1e-12)
    np.testing.assert_allclose(vectors.T @ np.diag(raw) @ vectors, expected, atol=1e-12)
    projections = weighted @ vectors.T
    np.testing.assert_allclose(np.mean(projections**2, axis=0), raw, atol=1e-12)
    assert np.all(np.diff(raw) <= 1e-12)


@pytest.mark.parametrize("form", ["structures", "molsys", "h5msm"])
@pytest.mark.parametrize("indices", [[0, 1, 2, 3], [3, 0, 3, 1], [2]])
@pytest.mark.parametrize(
    "kind",
    ["none", "list", "tuple", "int", "float32", "float64", "strided", "readonly"],
)
def test_weight_containers_dtypes_and_source_axes(form, indices, kind, tmp_path):
    source = system("angstrom")
    if form != "structures":
        molsys = MolSys(n_atoms=3)
        molsys.structures = source
        source = molsys
        if form == "h5msm":
            source = msm.convert(source, to_form=tmp_path / "pca.h5msm")
    selection = [2, 0, 2]
    expected_weights = np.ones(3) if kind == "none" else np.array([1.0, 4.0, 0.0])
    weights = {
        "none": lambda: None,
        "list": lambda: expected_weights.tolist(),
        "tuple": lambda: tuple(expected_weights),
        "int": lambda: expected_weights.astype(np.int64),
        "float32": lambda: expected_weights.astype(np.float32),
        "float64": lambda: expected_weights.copy(),
        "strided": lambda: np.repeat(expected_weights, 2)[::2],
        "readonly": lambda: expected_weights.copy(),
    }[kind]()
    if kind == "readonly":
        weights.flags.writeable = False
    before = None if weights is None else np.array(weights, copy=True)
    vectors, values = msm.structure.principal_component_analysis(
        source,
        selection=selection,
        structure_indices=indices,
        weights=weights,
        use_gpu=False,
    )
    expected, weighted = covariance(XYZ[indices][:, selection], expected_weights)
    assert_eigensystem(vectors, values, expected, weighted)
    if weights is not None:
        np.testing.assert_array_equal(weights, before)
    np.testing.assert_array_equal(selection, [2, 0, 2])
    coords = msm.get(source, coordinates=True)
    np.testing.assert_allclose(puw.get_value(coords, to_unit="nm"), XYZ)


@pytest.mark.parametrize("storage", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("presentation", ["nm", "angstrom", "pm"])
def test_squared_units_follow_policy_without_changing_covariance(storage, presentation):
    policy = list(puw.configure.get_standard_units())
    with puw.context(standard_units=[presentation, "ps", "radians"]):
        vectors, values = msm.structure.principal_component_analysis(
            system(storage),
            selection=[2, 0],
            structure_indices=[3, 0, 3],
            weights=[1.0, 4.0],
            use_gpu=False,
        )
        assert puw.get_unit(values) == puw.unit(presentation) ** 2
        expected, weighted = covariance(XYZ[[3, 0, 3]][:, [2, 0]], [1.0, 4.0])
        assert_eigensystem(vectors, values, expected, weighted)
    assert list(puw.configure.get_standard_units()) == policy


@pytest.mark.parametrize("weights", [[1.0], [1.0, 2.0, 3.0]])
def test_bad_weight_lengths_reject_before_kernel(weights, monkeypatch):
    from molsysmt._private import rust_backend

    def forbidden(*args, **kwargs):
        pytest.fail("Invalid weights reached the native kernel")

    monkeypatch.setattr(rust_backend, "principal_component_analysis", forbidden)
    with pytest.raises(ArgumentLengthError):
        msm.structure.principal_component_analysis(
            system(), selection=[0, 2], weights=weights, use_gpu=False
        )


@pytest.mark.parametrize(
    "weights",
    [
        [[1.0, 2.0]],
        [[1.0], [2.0]],
        [0.0, 0.0],
        [-1.0, 2.0],
        [np.nan, 2.0],
        [1.0, np.inf],
        [1.0, -np.inf],
        [1.0 + 2.0j, 2.0],
        "masses",
        puw.quantity([1.0, 2.0], "nm"),
    ],
)
def test_invalid_weights_reject_before_kernel(weights, monkeypatch):
    from molsysmt._private import rust_backend

    def forbidden(*args, **kwargs):
        pytest.fail("Invalid weights reached the native kernel")

    monkeypatch.setattr(rust_backend, "principal_component_analysis", forbidden)
    with pytest.raises(ArgumentError):
        msm.structure.principal_component_analysis(
            system(), selection=[0, 2], weights=weights, use_gpu=False
        )


@pytest.mark.parametrize("empty", ["atoms", "structures"])
def test_empty_observation_axes_reject_before_kernel(empty, monkeypatch):
    from molsysmt._private import rust_backend

    def forbidden(*args, **kwargs):
        pytest.fail("Empty observations reached the native kernel")

    monkeypatch.setattr(rust_backend, "principal_component_analysis", forbidden)
    with pytest.raises(ArgumentError):
        msm.structure.principal_component_analysis(
            system(),
            selection=[] if empty == "atoms" else [0, 2],
            structure_indices=[] if empty == "structures" else "all",
            use_gpu=False,
        )


def test_dimensionless_quantity_weights_preserve_their_numeric_meaning():
    weights = puw.quantity([100.0, 400.0], "percent")
    vectors, values = msm.structure.principal_component_analysis(
        system(), selection=[0, 2], weights=weights, use_gpu=False
    )
    expected, weighted = covariance(XYZ[:, [0, 2]], [1.0, 4.0])
    assert_eigensystem(vectors, values, expected, weighted)
    np.testing.assert_array_equal(puw.get_value(weights), [100.0, 400.0])


@pytest.mark.parametrize("bad", [np.nan, np.inf, -np.inf])
def test_nonfinite_coordinates_reject_before_kernel(bad, monkeypatch):
    from molsysmt._private import rust_backend

    def forbidden(*args, **kwargs):
        pytest.fail("Nonfinite observations reached the native kernel")

    monkeypatch.setattr(rust_backend, "principal_component_analysis", forbidden)
    coordinates = XYZ.copy()
    coordinates[1, 0, 2] = bad
    source = Structures(coordinates=puw.quantity(coordinates, "nm"))
    with pytest.raises(ArgumentError):
        msm.structure.principal_component_analysis(source, use_gpu=False)


def test_scaling_weights_scales_eigenvalues_without_weight_sum_normalization():
    vectors, values = msm.structure.principal_component_analysis(
        system(), weights=[2.0, 4.0, 8.0], use_gpu=False
    )
    expected, weighted = covariance(XYZ, [1.0, 2.0, 4.0])
    assert_eigensystem(vectors, values, 2.0 * expected, weighted * np.sqrt(2.0))
