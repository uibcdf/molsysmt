"""Public output admission must include the requested Python representation."""

import gc
import tracemalloc

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import Structures


def test_empty_csr_fits_where_row_objects_do_not(monkeypatch):
    coordinates = np.zeros((100, 100, 3))
    coordinates[:, :, 0] = np.arange(100)
    source = Structures(coordinates=puw.quantity(coordinates, "nm"))
    monkeypatch.setattr(msm.configure, "max_ram_usage", 2_000_000)
    csr = msm.structure.get_neighbors(
        source, threshold="0.1 nm", pbc=False, output_type="csr", num_threads=1
    )
    assert csr[0].shape == (10_001,)
    assert csr[1].shape == (0,)
    with pytest.raises(
        msm.MemoryBudgetExceededError, match="Python compatibility output"
    ):
        msm.structure.get_neighbors(
            source, threshold="0.1 nm", pbc=False, num_threads=1
        )
    np.testing.assert_array_equal(puw.get_value(source.coordinates), coordinates)


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
def test_row_quantities_keep_units_values_and_storage_alive(unit):
    source = Structures(
        coordinates=puw.quantity(
            [[[0.0, 0.0, 0.0], [0.2, 0.0, 0.0], [0.4, 0.0, 0.0]]], "nm"
        )
    )
    with puw.context(standard_units=[unit, "ps", "radians"]):
        indices, distances = msm.structure.get_neighbors(
            source, threshold="0.3 nm", pbc=False
        )
        csr = msm.structure.get_neighbors(
            source, threshold="0.3 nm", pbc=False, output_type="csr"
        )
        assert puw.get_unit(distances) == puw.unit(unit)
        gc.collect()
        for atom in range(3):
            section = slice(csr[0][atom], csr[0][atom + 1])
            np.testing.assert_array_equal(indices[0, atom], csr[1][section])
            np.testing.assert_allclose(
                puw.get_value(distances, to_unit="nm")[0, atom],
                puw.get_value(csr[2], to_unit="nm")[section],
                atol=1e-15,
                rtol=0,
            )
        # Mutating a returned row cannot alter source coordinates or another row.
        values = puw.get_value(distances)
        before = values[0, 1].copy()
        values[0, 0][0] = 1000.0
        np.testing.assert_array_equal(values[0, 1], before)
    np.testing.assert_array_equal(
        puw.get_value(source.coordinates, to_unit="nm"),
        [[[0.0, 0.0, 0.0], [0.2, 0.0, 0.0], [0.4, 0.0, 0.0]]],
    )


@pytest.mark.parametrize("cell_list", [False, True])
def test_contact_map_fits_but_dense_boxed_pairs_are_refused(monkeypatch, cell_list):
    source = Structures(coordinates=puw.quantity(np.zeros((1, 128, 3)), "nm"))
    monkeypatch.setattr(msm.configure, "max_ram_usage", 1_000_000)
    matrix = msm.structure.get_contacts(
        source,
        threshold="1 nm",
        pbc=False,
        cell_list=cell_list,
        use_gpu=False,
        num_threads=1,
    )
    assert matrix.shape == (1, 128, 128) and matrix.all()
    with pytest.raises(
        msm.MemoryBudgetExceededError, match="Python compatibility output"
    ):
        msm.structure.get_contacts(
            source,
            threshold="1 nm",
            pbc=False,
            output_type="pairs",
            cell_list=cell_list,
            use_gpu=False,
            num_threads=1,
        )


@pytest.mark.parametrize("labels", ["selection", "atom"])
@pytest.mark.parametrize("sorted_pairs", [False, True])
def test_multiple_packing_blocks_keep_directed_labels_and_sort_order(
    labels, sorted_pairs
):
    n = 200
    source = Structures(coordinates=puw.quantity(np.zeros((2, n, 3)), "nm"))
    selection = list(range(n - 1, -1, -1))
    second = list(range(0, n, 2))
    output = msm.structure.get_contacts(
        source,
        selection=selection,
        selection_2=second,
        structure_indices=[1, 0],
        threshold="1 nm",
        pbc=False,
        output_type="sorted pairs" if sorted_pairs else "pairs",
        output_indices=labels,
        use_gpu=False,
    )
    expected = [[i, j] for i in range(n) for j in range(len(second))]
    if labels == "atom":
        expected = [[selection[i], second[j]] for i, j in expected]
    if sorted_pairs:
        expected.sort()
    assert output == [expected, expected]


def test_self_packing_crosses_blocks_without_diagonal_or_reversed_duplicates():
    n = 140
    source = Structures(coordinates=puw.quantity(np.zeros((1, n, 3)), "nm"))
    output = msm.structure.get_contacts(
        source, threshold="1 nm", pbc=False, output_type="pairs", use_gpu=False
    )
    assert output == [[[i, j] for i in range(n) for j in range(i + 1, n)]]


@pytest.mark.parametrize("neighbors", [0, 2, 3])
def test_fixed_count_outputs_preserve_numeric_shape_with_admission(neighbors):
    source = Structures(coordinates=puw.quantity(np.zeros((1, 4, 3)), "nm"))
    indices, distances = msm.structure.get_neighbors(
        source, n_neighbors=neighbors, pbc=False
    )
    assert indices.shape == distances.shape == (1, 4, neighbors)


def test_invalid_count_precedes_memory_admission(monkeypatch):
    source = Structures(coordinates=puw.quantity(np.zeros((1, 2, 3)), "nm"))
    monkeypatch.setattr(msm.configure, "max_ram_usage", 1000)
    with pytest.raises(msm.ArgumentError):
        msm.structure.get_neighbors(source, n_neighbors=10**9, pbc=False)


@pytest.mark.parametrize("layout", ["C", "F", "reversed"])
@pytest.mark.parametrize("shape", [(181, 193), (2, 17017), (0, 3), (3, 0)])
@pytest.mark.parametrize("strict_upper", [False, True])
def test_contact_slabs_preserve_row_order_for_layouts_and_wide_rows(
    layout, shape, strict_upper
):
    from molsysmt.structure._compatibility_output import _contact_blocks

    rows, columns = np.indices(shape)
    matrix = ((13 * rows + 17 * columns) % 101) == 0
    if layout == "F":
        matrix = np.asfortranarray(matrix)
    elif layout == "reversed":
        matrix = matrix[::-1, ::-1]
    actual = []
    for left, right in _contact_blocks(matrix, paired=False, strict_upper=strict_upper):
        actual.extend(zip(left.tolist(), right.tolist()))
    expected = [
        (i, j)
        for i in range(shape[0])
        for j in range(shape[1])
        if matrix[i, j] and (not strict_upper or i < j)
    ]
    assert actual == expected


@pytest.mark.parametrize("layout", ["C", "F", "reversed"])
def test_empty_contact_projection_never_copies_the_whole_map(layout):
    from molsysmt.structure._compatibility_output import contact_pairs

    matrix = np.zeros(
        (1, 2048, 2048), dtype=bool, order=layout if layout != "reversed" else "C"
    )
    if layout == "reversed":
        matrix = matrix[:, ::-1, ::-1]
    # Input is 4 MiB. A whole-map flattening copy must fail this peak check;
    # bounded slabs and row counting need much less temporary storage.
    gc.collect()
    tracemalloc.start()
    try:
        output = contact_pairs(
            matrix,
            paired=False,
            strict_upper=True,
            atom_indices=[],
            atom_indices_2=None,
            output_indices="selection",
            sorted_pairs=False,
            budget=8 * 1024**2,
            caller="contact projection memory regression",
        )
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    assert output == [[]]
    assert peak < 1024**2


def test_all_structure_pair_outputs_are_admitted_before_boxing(monkeypatch):
    from molsysmt.structure._compatibility_output import contact_pairs

    matrix = np.ones((2, 128, 128), dtype=bool)

    def unexpected_packing(*args, **kwargs):
        pytest.fail("An over-budget result must be refused before pair packing.")

    monkeypatch.setattr(np, "empty", unexpected_packing)
    with pytest.raises(
        msm.MemoryBudgetExceededError, match="Python compatibility output"
    ):
        contact_pairs(
            matrix,
            paired=False,
            strict_upper=True,
            atom_indices=[],
            atom_indices_2=None,
            output_indices="selection",
            sorted_pairs=False,
            budget=3_000_000,
            caller="contact projection admission regression",
        )


@pytest.mark.parametrize("layout", ["C", "F", "reversed"])
@pytest.mark.parametrize("labels", ["selection", "atom"])
@pytest.mark.parametrize("sorted_pairs", [False, True])
def test_paired_projection_crosses_blocks_with_noncontiguous_inputs(
    layout, labels, sorted_pairs
):
    from molsysmt.structure._compatibility_output import contact_pairs

    n = 40000
    matrix = np.arange(2 * n).reshape(2, n) % 17 == 0
    if layout == "F":
        matrix = np.asfortranarray(matrix)
    elif layout == "reversed":
        matrix = matrix[:, ::-1]
    query = np.arange(n - 1, -1, -1, dtype=np.int64) + 1000
    target = np.arange(n, dtype=np.int64) * 3
    expected = []
    for structure in range(2):
        entries = [
            [int(query[i]), int(target[i])] if labels == "atom" else i
            for i in range(n)
            if matrix[structure, i]
        ]
        expected.append(sorted(entries) if sorted_pairs else entries)
    output = contact_pairs(
        matrix,
        paired=True,
        strict_upper=False,
        atom_indices=query,
        atom_indices_2=target,
        output_indices=labels,
        sorted_pairs=sorted_pairs,
        budget=8 * 1024**2,
        caller="paired contact projection regression",
    )
    assert output == expected
