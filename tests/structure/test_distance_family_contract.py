"""Independent numerical and correspondence contracts for distance-family tools."""

from itertools import product

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import (
    ArgumentConflictError,
    ArgumentError,
    ArgumentLengthError,
    NotImplementedMethodError,
)
from molsysmt.native import MolSys, Structures

XYZ = np.array(
    [
        [
            [0.1, 0.2, 0.3],
            [1.2, 0.4, 0.2],
            [2.4, 1.1, 0.5],
            [3.1, 0.6, 2.1],
            [0.7, 2.2, 1.3],
            [4.3, 2.7, 0.4],
        ],
        [
            [0.4, 0.1, 0.7],
            [1.6, 0.8, 0.3],
            [2.1, 1.8, 0.2],
            [3.7, 0.2, 1.6],
            [0.2, 2.8, 1.7],
            [4.8, 2.1, 0.9],
        ],
        [
            [0.8, 0.3, 0.1],
            [1.1, 0.6, 0.9],
            [2.9, 1.4, 0.7],
            [3.4, 0.9, 2.8],
            [0.5, 2.4, 1.1],
            [4.1, 2.9, 0.6],
        ],
    ],
    dtype=float,
)
BOXES = {
    "none": None,
    "orthogonal": np.eye(3) * 6,
    "triclinic": np.array([[6.0, 0, 0], [1.0, 5.5, 0], [0.3, 0.7, 5.0]]),
}


def molecular(xyz=XYZ, box=None):
    result = MolSys(n_atoms=xyz.shape[1])
    result.topology.atoms["atom_type"] = ["C", "N", "O", "S", "H", "F"][: xyz.shape[1]]
    result.structures = Structures(
        coordinates=puw.quantity(xyz * 10, "angstrom"),
        box=None
        if box is None
        else puw.quantity(np.tile(box, (len(xyz), 1, 1)) * 10, "angstrom"),
    )
    return result


def distances(first, second, box=None):
    delta = second[:, None, :, :] - first[:, :, None, :]
    if box is None:
        return np.linalg.norm(delta, axis=-1)
    # Exhaustive nearby lattice images, independent of fractional MIC rounding.
    images = np.asarray(list(product(range(-2, 3), repeat=3))) @ box
    return np.sqrt(
        np.min(np.sum((delta[..., None, :] - images) ** 2, axis=-1), axis=-1)
    )


@pytest.fixture(params=["molsys", "structures", "h5msm"])
def stored(request, tmp_path):
    def make(box=None):
        source = molecular(box=box)
        if request.param == "molsys":
            return source
        if request.param == "structures":
            return source.structures
        filename = tmp_path / "source.h5msm"
        msm.convert(source, to_form=filename)
        return filename

    return make


@pytest.mark.parametrize("box_kind", ["none", "orthogonal", "triclinic"])
@pytest.mark.parametrize("mode", ["off", "auto", "force"])
@pytest.mark.parametrize(
    "populations", [([4, 0, 2], [1, 5]), ([2, 0, 2], [2, 4, 0]), ([5], [0, 1, 3, 2])]
)
def test_flat_populations_and_structure_axes(stored, box_kind, mode, populations):
    first, second = populations
    frames, other = [2, 0, 2], [0, 2, 1]
    box = BOXES[box_kind]
    source = stored(box)
    with msm.configure.context(chunk_size=1, chunk_memory_fraction=None):
        result = msm.structure.get_distances(
            source,
            selection=first,
            selection_2=second,
            structure_indices=frames,
            structure_indices_2=other,
            pbc=box is not None,
            heavy_mode=mode,
            output_indices="atom",
            output_structure_indices="structure",
        )
    for got, expected in zip(result[:-1], [first, second, frames, other]):
        np.testing.assert_array_equal(got, expected)
    np.testing.assert_allclose(
        puw.get_value(result[-1], to_unit="nm"),
        distances(XYZ[frames][:, first], XYZ[other][:, second], box),
        atol=1e-12,
    )


@pytest.mark.parametrize(
    "function",
    [
        "get_distances",
        "get_minimum_distances",
        "get_maximum_distances",
        "get_neighbors",
    ],
)
@pytest.mark.parametrize("two_sources", [False, True])
@pytest.mark.parametrize("sizes", [(2, 2), (2, 3)])
def test_independent_weighted_centers(function, two_sources, sizes):
    first = molecular()
    shifted = XYZ + np.array([10.0, -0.2, 0.7])
    second = molecular(shifted) if two_sources else None
    a, b = [4, 0][: sizes[0]], [1, 5, 3][: sizes[1]]
    wa, wb = np.array([1.0, 2.0]), np.array([1.0, 3.0, 2.0][: len(b)])
    options = dict(
        selection=a,
        selection_2=b,
        structure_indices=[2, 0, 2],
        structure_indices_2=[0, 2, 1],
        molecular_system_2=second,
        center_of_atoms=True,
        center_of_atoms_2=True,
        weights=wa,
        weights_2=wb,
        pbc=False,
    )
    reference = np.linalg.norm(
        np.average(XYZ[[2, 0, 2]][:, a], weights=wa, axis=1)
        - np.average(
            (shifted if two_sources else XYZ)[[0, 2, 1]][:, b], weights=wb, axis=1
        ),
        axis=1,
    )
    if function == "get_neighbors":
        options["n_neighbors"] = 1
    result = getattr(msm.structure, function)(first, **options)
    got = result if function == "get_distances" else result[1]
    np.testing.assert_allclose(
        puw.get_value(got, to_unit="nm").reshape(-1), reference, atol=1e-12
    )
    np.testing.assert_array_equal(wa, [1.0, 2.0])
    np.testing.assert_array_equal(wb, [1.0, 3.0, 2.0][: len(b)])
    np.testing.assert_allclose(
        puw.get_value(first.structures.coordinates, to_unit="nm"), XYZ
    )


@pytest.mark.parametrize("selection_2", [None, [3, 1, 5]])
@pytest.mark.parametrize("kind", ["count", "threshold"])
def test_neighbors_use_explicit_second_source_even_with_implicit_selections(
    selection_2, kind
):
    source = molecular()
    target_xyz = XYZ + np.array([10.0, 0.0, 0.0])
    target = molecular(target_xyz)
    first = [3, 1, 5]
    second = first if selection_2 is None else selection_2
    options = {"n_neighbors": 2} if kind == "count" else {"threshold": "120 angstrom"}
    found, values = msm.structure.get_neighbors(
        source,
        selection=first,
        selection_2=selection_2,
        molecular_system_2=target,
        structure_indices=[2, 0, 2],
        structure_indices_2=[0, 2, 1],
        pbc=False,
        **options,
    )
    reference = distances(XYZ[[2, 0, 2]][:, first], target_xyz[[0, 2, 1]][:, second])
    raw = puw.get_value(values, to_unit="nm")
    for s in range(3):
        for i in range(3):
            expected = np.argsort(reference[s, i], kind="stable")
            expected = (
                expected[:2]
                if kind == "count"
                else expected[reference[s, i, expected] <= 12]
            )
            np.testing.assert_array_equal(found[s, i], expected)
            np.testing.assert_allclose(raw[s, i], reference[s, i, expected])


@pytest.mark.parametrize("name", ["get_minimum_distances", "get_maximum_distances"])
@pytest.mark.parametrize("entities", [(True, True), (False, True), (True, False)])
@pytest.mark.parametrize("paired", [False, True])
def test_extrema_indices_values_and_first_occurrence_ties(name, entities, paired):
    first, second = [4, 0, 2], [1, 5, 3]
    options = dict(
        selection=first,
        selection_2=second,
        structure_indices=[2, 0, 2],
        structure_indices_2=[0, 2, 1],
        pbc=False,
        pairs=paired,
        as_entity=entities[0],
        as_entity_2=entities[1],
    )
    if paired and entities != (True, True):
        with pytest.raises(ArgumentConflictError):
            getattr(msm.structure, name)(molecular(), **options)
        return
    actual_indices, actual_values = getattr(msm.structure, name)(molecular(), **options)
    reference = distances(XYZ[[2, 0, 2]][:, first], XYZ[[0, 2, 1]][:, second])
    choose = np.argmin if name == "get_minimum_distances" else np.argmax
    if paired:
        reference = np.diagonal(reference, axis1=1, axis2=2)
        expected_indices = choose(reference, axis=1)
        expected_values = np.take_along_axis(
            reference, expected_indices[:, None], axis=1
        )[:, 0]
    elif entities == (True, True):
        flat = choose(reference.reshape(3, -1), axis=1)
        expected_indices = np.column_stack(np.unravel_index(flat, (3, 3)))
        expected_values = reference[
            np.arange(3), expected_indices[:, 0], expected_indices[:, 1]
        ]
    else:
        axis = 2 if entities == (False, True) else 1
        expected_indices = choose(reference, axis=axis)
        expected_values = np.take_along_axis(
            reference, np.expand_dims(expected_indices, axis), axis=axis
        ).squeeze(axis)
    np.testing.assert_array_equal(actual_indices, expected_indices)
    np.testing.assert_allclose(
        puw.get_value(actual_values, to_unit="nm"), expected_values
    )
    equal = molecular(np.zeros((1, 3, 3)))
    tied_indices, _ = getattr(msm.structure, name)(
        equal,
        selection=[2, 0],
        selection_2=[1, 2],
        pbc=False,
        as_entity=entities[0],
        as_entity_2=entities[1],
        pairs=paired,
    )
    assert np.all(tied_indices == 0)


@pytest.mark.parametrize(
    "name",
    [
        "get_distances",
        "get_minimum_distances",
        "get_maximum_distances",
        "get_neighbors",
    ],
)
@pytest.mark.parametrize(
    "weights", [[0.0, 0.0], [-1.0, 2.0], [1.0, np.nan], [1.0], [[1.0, 2.0]]]
)
def test_invalid_center_weights(name, weights):
    kwargs = dict(
        selection=[0, 1],
        selection_2=[2, 3],
        center_of_atoms=True,
        center_of_atoms_2=True,
        weights=weights,
        weights_2=[1.0, 3.0],
        pbc=False,
    )
    if name == "get_neighbors":
        kwargs["n_neighbors"] = 1
    with pytest.raises((ArgumentError, ArgumentLengthError)):
        getattr(msm.structure, name)(molecular(), **kwargs)


@pytest.mark.parametrize("kind", ["count", "threshold", "zero_threshold"])
@pytest.mark.parametrize("fast", [False, True])
def test_self_exclusion_is_by_identity_with_coincident_points_and_ties(kind, fast):
    xyz = np.array([[[0.0, 0, 0], [0.0, 0, 0], [1.0, 0, 0], [-1.0, 0, 0]]])
    source = molecular(xyz)
    # Pair output selects the matrix fallback without substituting its geometry.
    kwargs = (
        {}
        if fast
        else {"output_type": "pairs", "output_indices": "selection", "sorted": False}
    )
    kwargs.update(
        {"n_neighbors": 1}
        if kind == "count"
        else {"threshold": "0 nm" if kind == "zero_threshold" else "1 nm"}
    )
    result = msm.structure.get_neighbors(source, pbc=False, **kwargs)
    matrix = distances(xyz, xyz)[0]
    expected = []
    for i in range(4):
        valid = np.array([j for j in range(4) if j != i])
        valid = valid[np.lexsort((valid, matrix[i, valid]))]
        valid = (
            valid[:1]
            if kind == "count"
            else valid[matrix[i, valid] <= (0 if kind == "zero_threshold" else 1)]
        )
        expected.append(valid)
    if fast:
        for i in range(4):
            np.testing.assert_array_equal(result[0][0, i], expected[i])
    else:
        assert result[0][0] == [
            [i, int(j)] for i, neighbors in enumerate(expected) for j in neighbors
        ]


@pytest.mark.parametrize("count", [0, 2, 3, -1])
def test_neighbor_count_limits_are_explicit(count):
    source = molecular(np.zeros((1, 3, 3)))
    if count < 0 or count > 2:
        with pytest.raises(ArgumentError):
            msm.structure.get_neighbors(source, n_neighbors=count, pbc=False)
    else:
        indices, values = msm.structure.get_neighbors(
            source, n_neighbors=count, pbc=False
        )
        assert indices.shape == (1, 3, count)
        assert puw.get_value(values).shape == (1, 3, count)


@pytest.mark.parametrize(
    "extra",
    [
        {"pairs": True},
        {"unique_pairs": True},
        {"mutual_only": True},
        {"output_indices": "atom"},
        {"output_structure_indices": "structure"},
    ],
)
def test_unsupported_neighbor_combinations_reject(extra):
    with pytest.raises(NotImplementedMethodError):
        msm.structure.get_neighbors(molecular(), n_neighbors=1, pbc=False, **extra)


@pytest.mark.parametrize("periodic", ["none", "orthogonal", "triclinic"])
@pytest.mark.parametrize("kind", ["count", "threshold", "csr", "pairs"])
@pytest.mark.parametrize("self_search", [False, True])
def test_neighbor_membership_indices_units_and_routes(
    stored, periodic, kind, self_search
):
    box = BOXES[periodic]
    source = stored(box)
    first = [4, 0, 2]
    second = first if self_search else [1, 5]
    kwargs = dict(
        selection=first,
        selection_2=None if self_search else second,
        structure_indices=[2, 0, 2],
        pbc=box is not None,
    )
    kwargs.update(
        {"n_neighbors": 1} if kind == "count" else {"threshold": "18 angstrom"}
    )
    if kind == "csr":
        kwargs["output_type"] = "csr"
    if kind == "pairs":
        kwargs.update(output_type="pairs", output_indices="atom")
    result = msm.structure.get_neighbors(source, **kwargs)
    matrix = distances(XYZ[[2, 0, 2]][:, first], XYZ[[2, 0, 2]][:, second], box)
    expected_pairs = []
    for structure in range(3):
        pair_rows = []
        for query in range(3):
            candidates = np.array(
                [j for j in range(len(second)) if not (self_search and j == query)],
                dtype=int,
            )
            candidates = candidates[
                np.lexsort((candidates, matrix[structure, query, candidates]))
            ]
            candidates = (
                candidates[:1]
                if kind == "count"
                else candidates[matrix[structure, query, candidates] <= 1.8]
            )
            pair_rows.extend([[first[query], second[j]] for j in candidates])
            if kind in ("count", "threshold"):
                got_indices = result[0][structure, query]
                got_values = puw.get_value(result[1], to_unit="nm")[structure, query]
            elif kind == "csr":
                row = structure * 3 + query
                low, high = result[0][row : row + 2]
                got_indices = result[1][low:high]
                got_values = puw.get_value(result[2], to_unit="nm")[low:high]
            else:
                continue
            np.testing.assert_array_equal(got_indices, candidates)
            np.testing.assert_allclose(got_values, matrix[structure, query, candidates])
        expected_pairs.append(sorted(pair_rows))
    if kind == "pairs":
        assert result[0] == expected_pairs
        for structure, rows in enumerate(result[0]):
            expected = [
                matrix[structure, first.index(i), second.index(j)] for i, j in rows
            ]
            np.testing.assert_allclose(
                puw.get_value(result[1][structure], to_unit="nm") if rows else [],
                expected,
            )


@pytest.mark.parametrize(
    "name",
    [
        "get_distances",
        "get_minimum_distances",
        "get_maximum_distances",
        "get_neighbors",
    ],
)
def test_nested_centers_and_masses(name):
    source = molecular()
    groups, other = [[4, 0], [2, 1, 3]], [[5, 1], [0, 3]]
    masses = puw.get_value(
        msm.physchem.get_mass(source, element="atom", selection="all")
    )
    a = np.stack(
        [np.average(XYZ[:, g], axis=1, weights=masses[g]) for g in groups], axis=1
    )
    b = np.stack(
        [np.average(XYZ[:, g], axis=1, weights=masses[g]) for g in other], axis=1
    )
    expected = distances(a, b)
    options = dict(
        selection=groups,
        selection_2=other,
        weights="masses",
        weights_2="masses",
        pbc=False,
    )
    if name == "get_neighbors":
        options["n_neighbors"] = 1
    result = getattr(msm.structure, name)(source, **options)
    if name == "get_distances":
        got = result
    elif name == "get_neighbors":
        np.testing.assert_array_equal(result[0][..., 0], np.argmin(expected, axis=2))
        got = result[1][..., 0]
        expected = np.min(expected, axis=2)
    else:
        choose = np.argmin if name == "get_minimum_distances" else np.argmax
        index = choose(expected.reshape(3, -1), axis=1)
        np.testing.assert_array_equal(
            result[0], np.column_stack(np.unravel_index(index, (2, 2)))
        )
        got = result[1]
        expected = expected.reshape(3, -1)[np.arange(3), index]
    np.testing.assert_allclose(puw.get_value(got, to_unit="nm"), expected)


@pytest.mark.parametrize("paired", [False, True])
@pytest.mark.parametrize("index_mode", ["atom", "selection"])
@pytest.mark.parametrize("frame_mode", [None, "structure", "selection"])
def test_dictionary_values_keep_positional_second_structure_correspondence(
    paired, index_mode, frame_mode
):
    a, b = [4, 0], [1, 5]
    frames, other = [2, 0, 2], [0, 2, 1]
    result = msm.structure.get_distances(
        molecular(),
        selection=a,
        selection_2=b,
        structure_indices=frames,
        structure_indices_2=other,
        pairs=paired,
        pbc=False,
        output_type="dictionary",
        output_indices=index_mode,
        output_structure_indices=frame_mode,
    )
    matrix = distances(XYZ[frames][:, a], XYZ[other][:, b])
    for first in range(2):
        for second in [first] if paired else range(2):
            entries = (
                result[first]
                if paired and index_mode == "selection"
                else result[a[first] if index_mode == "atom" else first][
                    b[second] if index_mode == "atom" else second
                ]
            )
            if frame_mode is None:
                np.testing.assert_allclose(
                    puw.get_value(entries, to_unit="nm"), matrix[:, first, second]
                )
            else:
                for s in range(3):
                    key, otherkey = (
                        (s, s) if frame_mode == "selection" else (frames[s], other[s])
                    )
                    np.testing.assert_allclose(
                        puw.get_value(entries[key][otherkey], to_unit="nm"),
                        matrix[s, first, second],
                    )


@pytest.mark.parametrize("mode", ["off", "force"])
@pytest.mark.parametrize("sizes", [(1, 3), (3, 1), (2, 3)])
def test_incompatible_structure_lists_reject_without_implicit_broadcast(mode, sizes):
    with pytest.raises(ArgumentError):
        msm.structure.get_distances(
            molecular(),
            selection=[0],
            selection_2=[1],
            structure_indices=list(range(sizes[0])),
            structure_indices_2=list(range(sizes[1])),
            heavy_mode=mode,
            pbc=False,
        )


@pytest.mark.parametrize(
    "name",
    [
        "get_distances",
        "get_minimum_distances",
        "get_maximum_distances",
        "get_neighbors",
    ],
)
def test_two_sources_with_implicit_axes_and_distinct_units(name):
    source = molecular()
    second = molecular(XYZ + 10)
    kwargs = dict(selection=[4, 0], molecular_system_2=second, pbc=False)
    if name == "get_neighbors":
        kwargs["n_neighbors"] = 1
    expected = distances(XYZ[:, [4, 0]], (XYZ + 10)[:, [4, 0]])
    result = getattr(msm.structure, name)(source, **kwargs)
    if name == "get_neighbors":
        expected = expected.min(axis=2)
        result = result[1][..., 0]
    elif name != "get_distances":
        expected = (expected.min if name == "get_minimum_distances" else expected.max)(
            axis=(1, 2)
        )
        result = result[1]
    np.testing.assert_allclose(puw.get_value(result, to_unit="nm"), expected)


@pytest.mark.parametrize("mode", ["off", "force"])
@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
def test_application_units_preserve_physical_magnitudes(mode, unit):
    source = molecular()
    before = list(puw.configure.get_standard_units())
    with puw.context(standard_units=[unit, "ps", "radians"]):
        result = msm.structure.get_distances(
            source,
            selection=[4, 0],
            selection_2=[1, 5],
            structure_indices=[2, 0],
            pbc=False,
            heavy_mode=mode,
        )
        assert puw.get_unit(result) == puw.unit(unit)
        np.testing.assert_allclose(
            puw.get_value(result, to_unit="nm"),
            distances(XYZ[[2, 0]][:, [4, 0]], XYZ[[2, 0]][:, [1, 5]]),
        )
    assert list(puw.configure.get_standard_units()) == before


@pytest.mark.parametrize(
    "name", ["get_minimum_distances", "get_maximum_distances", "get_neighbors"]
)
def test_automatic_disk_distance_intermediates_are_retired(name, monkeypatch):
    from molsysmt._private.execution import PersistentResultHandle

    xyz = np.tile(XYZ, (30, 1, 1))
    source = molecular(xyz)
    retired = []
    cleanup = PersistentResultHandle.cleanup

    def retire(handle):
        retired.append(handle._path)
        return cleanup(handle)

    monkeypatch.setattr(PersistentResultHandle, "cleanup", retire)
    options = dict(selection=[4, 0, 2], selection_2=[1, 3], pbc=False)
    if name == "get_neighbors":
        options["n_neighbors"] = 1
    expected = distances(xyz[:, [4, 0, 2]], xyz[:, [1, 3]])
    with msm.configure.context(
        max_ram_usage=4096, chunk_memory_fraction=None, chunk_size=2
    ):
        result = getattr(msm.structure, name)(source, **options)
    assert retired and all(not path.exists() for path in retired)
    if name == "get_neighbors":
        expected = expected.min(axis=2)
        got = result[1][..., 0]
    else:
        expected = (expected.min if name == "get_minimum_distances" else expected.max)(
            axis=(1, 2)
        )
        got = result[1]
    np.testing.assert_allclose(puw.get_value(got, to_unit="nm"), expected)


@pytest.mark.parametrize("mode", ["off", "force"])
def test_missing_box_follows_documented_vacuum_fallback(mode):
    result = msm.structure.get_distances(
        molecular(), selection=[4, 0], selection_2=[1], pbc=True, heavy_mode=mode
    )
    np.testing.assert_allclose(
        puw.get_value(result, to_unit="nm"), distances(XYZ[:, [4, 0]], XYZ[:, [1]])
    )


@pytest.mark.parametrize(
    "name",
    [
        "get_distances",
        "get_minimum_distances",
        "get_maximum_distances",
        "get_neighbors",
    ],
)
def test_singular_periodic_boxes_reject(name):
    from molsysmt._private.smonitor import StructuralInconsistencyError

    options = {"n_neighbors": 1} if name == "get_neighbors" else {}
    with pytest.raises(StructuralInconsistencyError):
        getattr(msm.structure, name)(
            molecular(box=np.zeros((3, 3))), pbc=True, **options
        )


@pytest.mark.parametrize("shape", [(3, 0, 6), (3, 6, 0), (0, 2, 3)])
@pytest.mark.parametrize("mode", ["off", "force"])
def test_empty_distance_axes_have_defined_shapes(shape, mode):
    ns, na, nb = shape
    result = msm.structure.get_distances(
        molecular(),
        selection=list(range(na)),
        selection_2=list(range(nb)),
        structure_indices=list(range(ns)),
        pbc=False,
        heavy_mode=mode,
    )
    assert result.shape == shape
    assert puw.get_value(result).dtype == np.float64


@pytest.mark.parametrize("name", ["get_minimum_distances", "get_maximum_distances"])
def test_empty_extremum_is_an_explicit_error(name):
    with pytest.raises(ArgumentError):
        getattr(msm.structure, name)(
            molecular(), selection=[], selection_2=[0], pbc=False
        )


@pytest.mark.parametrize(
    "options",
    [
        {"threshold": "1 nm"},
        {"n_neighbors": 0},
        {"threshold": "1 nm", "output_type": "csr"},
    ],
)
@pytest.mark.parametrize("empty_side", ["first", "second"])
def test_empty_neighbor_populations_are_typed(options, empty_side):
    first, second = ([], [0, 1]) if empty_side == "first" else ([0, 1], [])
    result = msm.structure.get_neighbors(
        molecular(), selection=first, selection_2=second, pbc=False, **options
    )
    if options.get("output_type") == "csr":
        np.testing.assert_array_equal(
            result[0], np.zeros(3 * len(first) + 1, dtype=int)
        )
        assert result[1].dtype == np.int64 and result[1].size == 0
    else:
        assert result[0].shape[:2] == (3, len(first))
        if options.get("n_neighbors") == 0:
            assert result[0].shape == (3, len(first), 0)
        else:
            assert all(len(row) == 0 for row in result[0].ravel())


@pytest.mark.parametrize("flags", [{"mutual_only": True}, {"unique_pairs": True}, {}])
def test_pair_filters_preserve_directed_endpoint_roles(flags):
    source = molecular(np.array([[[0.0, 0, 0], [1.0, 0, 0], [2.0, 0, 0], [5.0, 0, 0]]]))
    pairs, values = msm.structure.get_neighbors(
        source,
        n_neighbors=1,
        output_type="pairs",
        output_indices="atom",
        pbc=False,
        **flags,
    )
    expected = (
        [[0, 1]]
        if flags.get("mutual_only")
        else [[0, 1], [2, 1], [3, 2]]
        if flags.get("unique_pairs")
        else [[0, 1], [1, 0], [2, 1], [3, 2]]
    )
    assert pairs == [expected]
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm")[0]
    np.testing.assert_allclose(
        puw.get_value(values[0], to_unit="nm"),
        [np.linalg.norm(xyz[i] - xyz[j]) for i, j in expected],
    )


def test_repeated_self_selection_excludes_physical_self_occurrences():
    source = molecular()
    indices, values = msm.structure.get_neighbors(
        source, selection=[2, 0, 2], n_neighbors=1, pbc=False
    )
    np.testing.assert_array_equal(
        indices, np.tile(np.array([[[1], [0], [1]]]), (3, 1, 1))
    )
    assert np.all(puw.get_value(values) > 0)


@pytest.mark.parametrize(
    "centers", [(False, False), (True, False), (False, True), (True, True)]
)
@pytest.mark.parametrize(
    "name",
    [
        "get_distances",
        "get_minimum_distances",
        "get_maximum_distances",
        "get_neighbors",
    ],
)
@pytest.mark.parametrize("separate", [False, True])
def test_endpoint_parameters_remain_independent_for_mixed_centers(
    centers, name, separate
):
    source = molecular()
    other = molecular(XYZ + 4) if separate else None
    wa, wb = np.array([0.0, 3.0]), np.array([1.0, 2.0, 4.0])
    a, b = [0, 4], [3, 1, 5]
    left = XYZ[:, a]
    right = (XYZ + 4 if separate else XYZ)[:, b]
    if centers[0]:
        left = np.average(left, weights=wa, axis=1)[:, None]
    if centers[1]:
        right = np.average(right, weights=wb, axis=1)[:, None]
    reference = distances(left, right)
    kwargs = dict(
        selection=a,
        selection_2=b,
        molecular_system_2=other,
        center_of_atoms=centers[0],
        center_of_atoms_2=centers[1],
        weights=wa if centers[0] else None,
        weights_2=wb if centers[1] else None,
        pbc=False,
    )
    if name == "get_neighbors":
        kwargs["n_neighbors"] = 1
    result = getattr(msm.structure, name)(source, **kwargs)
    if name == "get_distances":
        got = result
    elif name == "get_neighbors":
        reference = reference.min(axis=2)
        got = result[1][..., 0]
    else:
        reference = (
            reference.min if name == "get_minimum_distances" else reference.max
        )(axis=(1, 2))
        got = result[1]
    np.testing.assert_allclose(puw.get_value(got, to_unit="nm"), reference)


@pytest.mark.parametrize(
    "name",
    [
        "get_distances",
        "get_minimum_distances",
        "get_maximum_distances",
        "get_neighbors",
    ],
)
def test_raw_endpoint_weights_are_not_silently_ignored(name):
    kwargs = {"n_neighbors": 1} if name == "get_neighbors" else {}
    with pytest.raises(ArgumentError):
        getattr(msm.structure, name)(
            molecular(), selection=[0, 1], weights=[1, 3], pbc=False, **kwargs
        )


def test_paired_atom_populations_must_have_equal_lengths():
    with pytest.raises(ArgumentError):
        msm.structure.get_distances(
            molecular(), selection=[0, 1], selection_2=[3], pairs=True, pbc=False
        )


@pytest.mark.parametrize("cutoff", ["-1 nm", "nan nm", "inf nm"])
def test_neighbor_threshold_must_be_finite_and_nonnegative(cutoff):
    with pytest.raises(ArgumentError):
        msm.structure.get_neighbors(molecular(), threshold=cutoff, pbc=False)


def test_disk_dictionary_output_rejects_and_retires_the_backing_file(monkeypatch):
    from molsysmt._private.execution import PersistentResultHandle

    retired = []
    cleanup = PersistentResultHandle.cleanup

    def retire(handle):
        retired.append(handle._path)
        return cleanup(handle)

    monkeypatch.setattr(PersistentResultHandle, "cleanup", retire)
    with msm.configure.context(max_ram_usage=4096, chunk_memory_fraction=None):
        with pytest.raises(NotImplementedMethodError):
            msm.structure.get_distances(
                molecular(np.tile(XYZ, (30, 1, 1))),
                selection=[4, 0, 2],
                selection_2=[1, 3],
                pbc=False,
                output_type="dictionary",
            )
    assert retired and all(not path.exists() for path in retired)


@pytest.mark.parametrize("route", [False, True])
@pytest.mark.parametrize("box_kind", ["none", "orthogonal", "triclinic"])
@pytest.mark.parametrize("paired", [False, True])
@pytest.mark.parametrize("implicit", [False, True])
def test_contact_maps_keep_both_structure_axes(
    stored, route, box_kind, paired, implicit
):
    a, b = [4, 0, 2], [1, 5, 3]
    if implicit:
        b = a
    frames, other = [2, 0, 2], [0, 2, 1]
    kwargs = dict(
        selection=a,
        selection_2=None if implicit and not paired else b,
        structure_indices=frames,
        structure_indices_2=other,
        pairs=paired,
        pbc=box_kind != "none",
        threshold="18 angstrom",
        cell_list=route,
        use_gpu=False,
    )
    expected = distances(XYZ[frames][:, a], XYZ[other][:, b], BOXES[box_kind]) <= 1.8
    if paired:
        expected = np.diagonal(expected, axis1=1, axis2=2)
    actual = msm.structure.get_contacts(stored(BOXES[box_kind]), **kwargs)
    assert actual.dtype == np.bool_
    np.testing.assert_array_equal(actual, expected)


@pytest.mark.parametrize("route", [False, True])
@pytest.mark.parametrize("paired", [False, True])
@pytest.mark.parametrize("output", ["pairs", "sorted pairs"])
def test_contact_pair_indices_preserve_selected_atom_roles(route, paired, output):
    source = molecular()
    a, b = [4, 0], [1, 5]
    matrix = distances(XYZ[:, a], XYZ[:, b]) <= 1.8
    if paired:
        matrix = np.diagonal(matrix, axis1=1, axis2=2)
    actual = msm.structure.get_contacts(
        source,
        selection="atom_index in [4, 0]",
        selection_2="atom_index in [1, 5]",
        threshold="1.8 nm",
        pairs=paired,
        pbc=False,
        output_type=output,
        output_indices="atom",
        cell_list=route,
        use_gpu=False,
    )
    # Expressions select source order, while literal index lists preserve order.
    a, b = [0, 4], [1, 5]
    matrix = distances(XYZ[:, a], XYZ[:, b]) <= 1.8
    if paired:
        matrix = np.diagonal(matrix, axis1=1, axis2=2)
    expected = []
    for s in range(3):
        expected.append(
            [[a[i], b[i]] for i in np.flatnonzero(matrix[s])]
            if paired
            else [[a[i], b[j]] for i, j in np.argwhere(matrix[s])]
        )
    assert actual == expected


@pytest.mark.parametrize("route", [False, True])
@pytest.mark.parametrize("output", ["numpy.ndarray", "pairs", "sorted pairs"])
def test_empty_contact_populations_and_zero_structures(route, output):
    for first, second, frames in [([], [0], [0, 2]), ([0], [], [0, 2]), ([0], [1], [])]:
        result = msm.structure.get_contacts(
            molecular(),
            selection=first,
            selection_2=second,
            structure_indices=frames,
            pbc=False,
            cell_list=route,
            use_gpu=False,
            output_type=output,
            output_indices="atom",
        )
        if output == "numpy.ndarray":
            assert (
                result.shape == (len(frames), len(first), len(second))
                and result.dtype == np.bool_
            )
        else:
            assert result == [[] for _ in frames]


@pytest.mark.parametrize("route", [False, True])
def test_contacts_use_independent_numeric_group_weights(route):
    result = msm.structure.get_contacts(
        molecular(),
        selection=[0, 4],
        selection_2=[1, 3, 5],
        center_of_atoms=True,
        center_of_atoms_2=True,
        weights=[1, 2],
        weights_2=[1, 3, 2],
        threshold="2 nm",
        pbc=False,
        cell_list=route,
        use_gpu=False,
    )
    a = np.average(XYZ[:, [0, 4]], weights=[1, 2], axis=1)
    b = np.average(XYZ[:, [1, 3, 5]], weights=[1, 3, 2], axis=1)
    np.testing.assert_array_equal(result[:, 0, 0], np.linalg.norm(b - a, axis=1) <= 2)


@pytest.mark.parametrize("route", [False, True])
@pytest.mark.parametrize("cutoff", [0.0, 1.0])
def test_contact_cutoff_is_inclusive_and_self_map_contains_diagonal(route, cutoff):
    xyz = np.array([[[0.0, 0, 0], [0.0, 0, 0], [1.0, 0, 0]]])
    result = msm.structure.get_contacts(
        molecular(xyz),
        threshold=puw.quantity(cutoff, "nm"),
        pbc=False,
        cell_list=route,
        use_gpu=False,
    )
    np.testing.assert_array_equal(result, distances(xyz, xyz) <= cutoff)


@pytest.mark.parametrize("route", [False, True])
def test_contact_structure_zero_is_a_real_secondary_index(route):
    result = msm.structure.get_contacts(
        molecular(),
        selection=[4, 0],
        selection_2=[1, 5],
        structure_indices=[2],
        structure_indices_2=[0],
        threshold="2 nm",
        pbc=False,
        cell_list=route,
        use_gpu=False,
    )
    np.testing.assert_array_equal(
        result, distances(XYZ[[2]][:, [4, 0]], XYZ[[0]][:, [1, 5]]) <= 2
    )


@pytest.mark.parametrize("indices", ["selection", "atom"])
def test_contact_pairs_across_structures_keep_all_directed_entries(indices):
    a = [2, 0]
    result = msm.structure.get_contacts(
        molecular(),
        selection=a,
        structure_indices=[2, 0],
        structure_indices_2=[0, 2],
        threshold="100 nm",
        pbc=False,
        output_type="pairs",
        output_indices=indices,
        use_gpu=False,
    )
    labels = [0, 1] if indices == "selection" else a
    assert result == [[[i, j] for i in labels for j in labels] for _ in range(2)]


@pytest.mark.parametrize("cutoff", ["-1 nm", "nan nm", "inf nm"])
def test_contact_cutoff_validation_is_shared_by_cpu_routes(cutoff):
    with pytest.raises(ArgumentError):
        msm.structure.get_contacts(
            molecular(), threshold=cutoff, pbc=False, use_gpu=False, cell_list=True
        )


def test_contact_output_budget_and_disk_intermediate_lifecycle(monkeypatch):
    from molsysmt._private.execution import PersistentResultHandle
    from molsysmt._private.smonitor import MemoryBudgetExceededError

    source = molecular(np.tile(XYZ, (30, 1, 1)))
    with msm.configure.context(max_ram_usage=64):
        with pytest.raises(MemoryBudgetExceededError):
            msm.structure.get_contacts(
                source, threshold="1 nm", pbc=False, use_gpu=False, cell_list=True
            )
    retired = []
    cleanup = PersistentResultHandle.cleanup

    def retire(handle):
        retired.append(handle._path)
        return cleanup(handle)

    monkeypatch.setattr(PersistentResultHandle, "cleanup", retire)
    with msm.configure.context(max_ram_usage=4096, chunk_memory_fraction=None):
        result = msm.structure.get_contacts(
            source,
            selection=[4, 0, 2],
            selection_2=[1, 3],
            threshold="2 nm",
            pbc=False,
            use_gpu=False,
            cell_list=False,
        )
    assert retired and all(not path.exists() for path in retired)
    np.testing.assert_array_equal(
        result,
        distances(
            np.tile(XYZ, (30, 1, 1))[:, [4, 0, 2]], np.tile(XYZ, (30, 1, 1))[:, [1, 3]]
        )
        <= 2,
    )


@pytest.mark.parametrize(
    "name",
    [
        "get_distances",
        "get_minimum_distances",
        "get_maximum_distances",
        "get_neighbors",
    ],
)
def test_two_native_sources_can_have_different_atom_and_structure_inventories(name):
    target_xyz = XYZ[:2, :3] + np.array([10.0, 0.5, -0.2])
    source, target = molecular(), molecular(target_xyz)
    kwargs = dict(
        selection=[2, 0],
        molecular_system_2=target,
        structure_indices=[2, 0, 2],
        structure_indices_2=[1, 0, 1],
        pbc=False,
    )
    expected = distances(XYZ[[2, 0, 2]][:, [2, 0]], target_xyz[[1, 0, 1]][:, [2, 0]])
    if name == "get_neighbors":
        kwargs["n_neighbors"] = 1
    result = getattr(msm.structure, name)(source, **kwargs)
    if name == "get_distances":
        got = result
    elif name == "get_neighbors":
        expected = expected.min(axis=2)
        got = result[1][..., 0]
    else:
        expected = (expected.min if name == "get_minimum_distances" else expected.max)(
            axis=(1, 2)
        )
        got = result[1]
    np.testing.assert_allclose(puw.get_value(got, to_unit="nm"), expected)


@pytest.mark.parametrize(
    "name",
    [
        "get_distances",
        "get_minimum_distances",
        "get_maximum_distances",
        "get_neighbors",
        "get_contacts",
    ],
)
@pytest.mark.parametrize("first_center", [False, True])
@pytest.mark.parametrize("second_weights", [None, [1.0, 3.0]])
def test_implicit_second_center_inherits_selected_atoms_but_keeps_its_model(
    name, first_center, second_weights
):
    selected = [4, 0]
    first = XYZ[:, selected]
    if first_center:
        first = np.mean(first, axis=1)[:, None]
    second = (
        np.mean(XYZ[:, selected], axis=1)
        if second_weights is None
        else np.average(XYZ[:, selected], axis=1, weights=second_weights)
    )[:, None]
    expected = distances(first, second)
    kwargs = dict(
        selection=selected,
        center_of_atoms=first_center,
        center_of_atoms_2=True,
        weights_2=second_weights,
        pbc=False,
    )
    if name == "get_neighbors":
        kwargs["n_neighbors"] = 1
    if name == "get_contacts":
        kwargs.update(threshold="1 nm", use_gpu=False, cell_list=True)
    result = getattr(msm.structure, name)(molecular(), **kwargs)
    if name == "get_distances":
        got = result
    elif name == "get_contacts":
        np.testing.assert_array_equal(result, expected <= 1)
        return
    elif name == "get_neighbors":
        expected = expected.min(axis=2)
        got = result[1][..., 0]
    else:
        expected = (expected.min if name == "get_minimum_distances" else expected.max)(
            axis=(1, 2)
        )
        got = result[1]
    np.testing.assert_allclose(puw.get_value(got, to_unit="nm"), expected)
