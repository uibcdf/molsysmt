"""Comparing packed SVD plane kernels with independent analytical geometry."""

import molsysmt._rust as rust
import numpy as np
import pytest


def _fit(coordinates, groups, threads=1):
    offsets = np.concatenate(([0], np.cumsum([len(group) for group in groups]))).astype(np.int64)
    positions = np.concatenate(groups).astype(np.int64)
    return rust.get_least_squares_planes(coordinates, offsets, positions, threads)


@pytest.mark.parametrize("threads", [1, 4])
@pytest.mark.parametrize("scale", [1e-100, 1., 1e100])
def test_rotated_ragged_overlapping_groups_against_known_planes_and_nonmutation(threads, scale):
    u = np.array([1., -1., 0.]) / np.sqrt(2)
    v = np.array([1., 1., -2.]) / np.sqrt(6)
    normal = np.cross(u, v)
    angles = np.arange(6) * np.pi / 3
    xyz = .14 * (np.cos(angles)[:, None] * u + np.sin(angles)[:, None] * v)
    shifts = np.array([[.3, -.2, .8], [0., 0., 0.], [.2, -.1, .1]])
    coordinates = (xyz[None] + shifts[:, None]) * scale
    before = coordinates.copy()
    centers, normals, rms, maximum = _fit(coordinates, [np.arange(6), np.arange(3)], threads)
    assert centers.shape == normals.shape == (3, 2, 3)
    assert rms.shape == maximum.shape == (3, 2)
    np.testing.assert_allclose(centers[:, 0] / scale, shifts, atol=1e-14)
    np.testing.assert_allclose(np.abs(normals @ normal), 1., atol=1e-13)
    np.testing.assert_allclose(rms / scale, 0, atol=1e-14)
    np.testing.assert_allclose(maximum / scale, 0, atol=1e-14)
    np.testing.assert_array_equal(coordinates, before)


def test_warped_cloud_against_covariance_oracle_and_projected_distances():
    rng = np.random.default_rng(85)
    coordinates = rng.normal(size=(3, 17, 3)) * [.5, .3, .02]
    centers, normals, rms, maximum = _fit(coordinates, [np.arange(17)])
    for frame, xyz in enumerate(coordinates):
        centered = xyz - xyz.mean(axis=0)
        _, axes = np.linalg.eigh(centered.T @ centered)
        expected = axes[:, 0]
        np.testing.assert_allclose(centers[frame, 0], xyz.mean(axis=0), atol=1e-14)
        assert abs(np.dot(normals[frame, 0], expected)) == pytest.approx(1., abs=1e-13)
        residual = centered @ expected
        assert rms[frame, 0] == pytest.approx(np.sqrt(np.mean(residual ** 2)), rel=1e-12)
        assert maximum[frame, 0] == pytest.approx(np.max(np.abs(residual)), rel=1e-12)


def test_rotated_warped_hexagon_normal_and_maximum_against_independent_oracle():
    # Nearly equal in-plane singular values exposed inaccurate right vectors
    # in the first Nalgebra prototype, despite an accurate minimum singular value.
    axes, _ = np.linalg.qr(np.random.default_rng(824).normal(size=(3, 3)))
    phase = np.arange(6) * np.pi / 3
    xyz = .14 * (np.cos(phase)[:, None] * axes[:, 0] + np.sin(phase)[:, None] * axes[:, 1])
    xyz[0] += .01 * axes[:, 2]
    xyz += [0., .4, -.2]
    centered = xyz - xyz.mean(axis=0)
    _, vectors = np.linalg.eigh(centered.T @ centered)
    normal = vectors[:, 0]
    normal *= np.sign(normal[np.argmax(np.abs(normal))])
    _, normals, _, maximum = _fit(xyz[None], [np.arange(6)])
    np.testing.assert_allclose(normals[0, 0], normal, rtol=0, atol=1e-13)
    np.testing.assert_allclose(maximum[0, 0], np.max(np.abs(centered @ normal)), rtol=1e-12, atol=1e-14)


@pytest.mark.parametrize("width", [1., 1e-5, 1e-10])
def test_thin_plane_uses_rectangular_svd_without_squaring_condition_number(width):
    angle = .37
    rotate = np.array([[np.cos(angle), 0., np.sin(angle)], [0., 1., 0.], [-np.sin(angle), 0., np.cos(angle)]])
    xyz = np.array([[-1., -width, 0.], [1., -width, 0.], [1., width, 0.], [-1., width, 0.]]) @ rotate.T
    centers, normals, rms, maximum = _fit(xyz[None], [np.arange(4)])
    assert abs(np.dot(normals[0, 0], rotate[:, 2])) == pytest.approx(1., abs=1e-12)
    np.testing.assert_allclose(centers, 0, atol=1e-14)
    np.testing.assert_allclose(rms, 0, atol=1e-14)
    np.testing.assert_allclose(maximum, 0, atol=1e-14)


@pytest.mark.parametrize("xyz", [
    np.zeros((4, 3)), np.array([[0., 0., 0.], [1., 0., 0.], [2., 0., 0.], [3., 0., 0.]]),
    np.array([[1., 1., 1.], [1., -1., -1.], [-1., 1., -1.], [-1., -1., 1.]]),
    np.array([[-1., -1e-13, 0.], [1., -1e-13, 0.], [1., 1e-13, 0.], [-1., 1e-13, 0.]]),
])
def test_degenerate_clouds_rejected_without_partial_output(xyz):
    with pytest.raises(ValueError):
        _fit(xyz[None], [np.arange(len(xyz))], 4)


@pytest.mark.parametrize("case", ["shape", "finite", "offset_start", "offset_end", "offset_order", "short", "negative", "range", "threads"])
def test_extension_boundary_rejects_malformed_inputs_before_indexing(case):
    coords = np.array([[[0., 0., 0.], [1., 0., 0.], [0., 1., 0.]]])
    offsets = np.array([0, 3], dtype=np.int64)
    atoms = np.arange(3, dtype=np.int64)
    threads = 1
    if case == "shape":
        coords = np.ones((1, 3, 2))
    elif case == "finite":
        coords[0, 0, 0] = np.nan
    elif case == "offset_start":
        offsets[0] = 1
    elif case == "offset_end":
        offsets[1] = 4
    elif case == "offset_order":
        offsets = np.array([0, 3, 2, 3], dtype=np.int64)
    elif case == "short":
        offsets = np.array([0, 2], dtype=np.int64)
        atoms = atoms[:2]
    elif case == "negative":
        atoms[0] = -1
    elif case == "range":
        atoms[0] = 3
    else:
        threads = 0
    with pytest.raises(ValueError):
        rust.get_least_squares_planes(coords, offsets, atoms, threads)


@pytest.mark.parametrize("frames,groups", [(0, [np.arange(3)]), (3, [])])
def test_typed_empty_axes(frames, groups):
    offsets = np.array([0, 3] if groups else [0], dtype=np.int64)
    positions = np.arange(3, dtype=np.int64) if groups else np.empty(0, dtype=np.int64)
    result = rust.get_least_squares_planes(np.zeros((frames, 3, 3)), offsets, positions, 1)
    assert result[0].shape == result[1].shape == (frames, len(groups), 3)
    assert result[2].shape == result[3].shape == (frames, len(groups))
    assert all(array.dtype == np.float64 for array in result)


def test_seeded_ragged_kernel_parity_and_thread_determinism():
    rng = np.random.default_rng(91)
    coordinates = rng.normal(size=(7, 28, 3))
    groups = [np.arange(6), np.arange(5, 13), np.arange(13, 28)]
    # Independent NumPy factorization; never call the production Rust wrapper.
    reference = (np.empty((7, 3, 3)), np.empty((7, 3, 3)), np.empty((7, 3)), np.empty((7, 3)))
    for frame, xyz in enumerate(coordinates):
        for group, atoms in enumerate(groups):
            center = xyz[atoms].mean(axis=0)
            centered = xyz[atoms] - center
            _, _, axes = np.linalg.svd(centered, full_matrices=False)
            normal = axes[-1]
            residual = centered @ normal
            reference[0][frame, group] = center
            reference[1][frame, group] = normal
            reference[2][frame, group] = np.sqrt(np.mean(residual ** 2))
            reference[3][frame, group] = np.max(np.abs(residual))
    serial = _fit(coordinates, groups)
    parallel = _fit(coordinates, groups, 4)
    for first, second in zip(serial, parallel):
        np.testing.assert_array_equal(first, second)
    np.testing.assert_allclose(np.abs(np.sum(serial[1] * reference[1], axis=-1)), 1, rtol=0, atol=1e-13)
    for index in (0, 2, 3):
        np.testing.assert_allclose(serial[index], reference[index], rtol=1e-12, atol=1e-14)


def test_adapter_preserves_strided_coordinate_storage_and_session_thread_policy(monkeypatch):
    from molsysmt import configure
    from molsysmt._private import rust_backend

    coordinates = np.array([[[0., 0., 0.], [1., 0., 0.], [0., 1., 0.]]] * 3)[::-1]
    assert not coordinates.flags.c_contiguous
    original = rust.get_least_squares_planes
    observed_threads = []

    def record(xyz, offsets, positions, threads):
        assert np.shares_memory(xyz, coordinates)
        observed_threads.append(threads)
        return original(xyz, offsets, positions, threads)

    monkeypatch.setattr(rust, "get_least_squares_planes", record)
    monkeypatch.setattr(configure, "parallel_mode", True)
    monkeypatch.setattr(configure, "num_threads", 4)
    result = rust_backend.get_least_squares_planes(coordinates, np.array([0, 3]), np.arange(3))
    np.testing.assert_allclose(result[1][:, 0], np.tile([0., 0., 1.], (3, 1)), atol=1e-14)
    assert observed_threads == [4]
