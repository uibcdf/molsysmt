"""Valid sparse cutoffs must not allocate empty spatial volume."""

import os
import subprocess
import sys

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import Structures


@pytest.mark.skipif(
    sys.platform != "linux",
    reason="Linux address-space protected original allocation guard",
)
def test_two_atom_tiny_cutoff_under_protected_address_space(tmp_path):
    code = """
import resource
import numpy as np
import molsysmt as msm
from molsysmt.native import Structures
source = Structures(coordinates=msm.pyunitwizard.quantity(np.array([[[0.,0,0],[1.,1,1]]]), 'nm'))
resource.setrlimit(resource.RLIMIT_CORE, (0,0))
resource.setrlimit(resource.RLIMIT_AS, (2*1024**3,2*1024**3))
values = msm.structure.get_neighbors(source, selection=[0], selection_2=[1], structure_indices=[0], threshold='0.001 nm', pbc=False, output_type='csr')
assert values[0].tolist() == [0,0]
assert values[1].size == 0
print('BOUNDED_SPARSE_NEIGHBOR_OK')
"""
    log = tmp_path / "protected-native-query.log"
    with log.open("w") as stream:
        result = subprocess.run(
            [sys.executable, "-c", code],
            env={
                **os.environ,
                "RAYON_NUM_THREADS": "1",
                "OPENBLAS_NUM_THREADS": "1",
                "OMP_NUM_THREADS": "1",
            },
            stdout=stream,
            stderr=subprocess.STDOUT,
            timeout=30,
        )
    assert result.returncode == 0, log.read_text()[-1800:]
    assert "BOUNDED_SPARSE_NEIGHBOR_OK" in log.read_text()


def _ensemble(periodic):
    if periodic == "vacuum":
        xyz = np.array(
            [[0, 0, 0], [1, 1, 1], [0.0002, 0, 0], [1.0004, 1, 1], [9, 3, 6]],
            dtype=float,
        )
        boxes = None
    else:
        box = np.diag([3.0, 3.0, 3.0])
        if periodic == "triclinic":
            box[1, 0], box[2, 0], box[2, 1] = 0.7, 0.4, 0.6
        frac = np.array(
            [
                [0.0001, 0.0001, 0.0001],
                [0.9999, 0.0001, 0.0001],
                [0.3, 0.5, 0.7],
                [0.3001, 0.5, 0.7],
                [0.1, 0.2, 0.3],
            ]
        )
        xyz = frac @ box
        boxes = msm.pyunitwizard.quantity(np.repeat(box[None], 3, axis=0), "nm")
    middle = np.arange(15, dtype=float).reshape(5, 3) * 0.13
    coordinates = np.stack([xyz, middle, xyz + 0.01])
    return Structures(
        coordinates=msm.pyunitwizard.quantity(coordinates, "nm"), box=boxes
    )


def _oracle(source, selection, references, structures, periodic, cutoff):
    from itertools import product

    xyz = msm.pyunitwizard.get_value(source.coordinates, to_unit="nm")
    boxes = (
        None
        if source.box is None
        else msm.pyunitwizard.get_value(source.box, to_unit="nm")
    )
    offsets, indices, distances = [0], [], []
    self_mode = references is None
    references = selection if self_mode else references
    shifts = np.array(list(product(range(-2, 3), repeat=3)))
    for frame in structures:
        for iq, atom in enumerate(selection):
            pairs = []
            for j, ref in enumerate(references):
                if self_mode and j == iq:
                    continue
                delta = xyz[frame, ref] - xyz[frame, atom]
                value = (
                    np.linalg.norm(delta)
                    if not periodic
                    else np.min(
                        np.linalg.norm(delta[None] - shifts @ boxes[frame], axis=1)
                    )
                )
                if value <= cutoff:
                    pairs.append((float(value), j))
            for value, j in sorted(pairs):
                indices.append(j)
                distances.append(value)
            offsets.append(len(indices))
    return offsets, indices, distances


@pytest.mark.parametrize("periodic", ["vacuum", "orthogonal", "triclinic"])
@pytest.mark.parametrize("units", ["nm", "pm"])
@pytest.mark.parametrize("self_mode", [False, True])
def test_small_cutoff_matches_independent_geometry_and_array_csr(
    periodic, units, self_mode
):
    source = _ensemble(periodic)
    frames = [2, 0, 2, 1]
    selection = [0, 1, 2, 3, 4] if self_mode else [2, 0, 2]
    references = None if self_mode else [3, 1, 3, 4]
    before = msm.pyunitwizard.get_value(source.coordinates, to_unit="nm").copy()
    expected = _oracle(
        source, selection, references, frames, periodic != "vacuum", 0.001
    )
    with msm.pyunitwizard.context(
        standard_units=[units, "ps", "Da", "K", "e", "radians"]
    ):
        csr = msm.structure.get_neighbors(
            source,
            selection=selection,
            selection_2=references,
            structure_indices=frames,
            threshold="0.001 nm",
            pbc=periodic != "vacuum",
            output_type="csr",
            parallel=True,
            num_threads=2,
        )
        array = msm.structure.get_neighbors(
            source,
            selection=selection,
            selection_2=references,
            structure_indices=frames,
            threshold="0.001 nm",
            pbc=periodic != "vacuum",
        )
        assert csr[0].dtype == csr[1].dtype == np.int64
        np.testing.assert_array_equal(csr[0], expected[0])
        np.testing.assert_array_equal(csr[1], expected[1])
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(csr[2], to_unit="nm"),
            expected[2],
            atol=2e-13,
            rtol=0,
        )
        assert array[0].shape == (4, len(selection))
        values = msm.pyunitwizard.get_value(array[1], to_unit="nm")
        for frame in range(4):
            for atom in range(len(selection)):
                row = frame * len(selection) + atom
                sl = slice(csr[0][row], csr[0][row + 1])
                np.testing.assert_array_equal(array[0][frame, atom], csr[1][sl])
                np.testing.assert_allclose(
                    values[frame, atom], expected[2][sl], atol=2e-13, rtol=0
                )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(source.coordinates, to_unit="nm"), before
    )


def test_sparse_wide_extents_do_not_require_empty_volume_storage():
    source = Structures(
        coordinates=msm.pyunitwizard.quantity([[[0, 0, 0], [1e12, 1e12, 1e12]]], "nm")
    )
    result = msm.structure.get_neighbors(
        source,
        selection=[0],
        selection_2=[1],
        threshold="1e-12 nm",
        pbc=False,
        output_type="csr",
    )
    assert result[0].tolist() == [0, 0]
    assert result[1].size == result[2].size == 0


def test_budget_refusal_names_the_configured_numerical_limit(monkeypatch):
    source = _ensemble("vacuum")
    monkeypatch.setattr(msm.configure, "max_ram_usage", 1024)
    with pytest.raises(msm.MemoryBudgetExceededError, match="numerical budget"):
        msm.structure.get_neighbors(source, threshold="0.001 nm", pbc=False)


def test_resident_output_is_charged_from_actual_hits(monkeypatch):
    monkeypatch.setattr(msm.configure, "max_ram_usage", 1 << 18)
    sparse = Structures(
        coordinates=msm.pyunitwizard.quantity(
            np.arange(900, dtype=float).reshape(1, 300, 3) * 10, "nm"
        )
    )
    result = msm.structure.get_neighbors(
        sparse, threshold="0.01 nm", pbc=False, output_type="csr", num_threads=1
    )
    assert result[0].shape == (301,)
    assert result[1].size == 0
    dense = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((1, 300, 3)), "nm")
    )
    with pytest.raises(msm.MemoryBudgetExceededError, match="CSR output"):
        msm.structure.get_neighbors(
            dense, threshold="0.01 nm", pbc=False, num_threads=1
        )


@pytest.mark.parametrize("threshold", ["-0.1 nm", "nan nm", "inf nm"])
def test_invalid_cutoff_refuses_before_native_storage(threshold):
    with pytest.raises(msm.ArgumentError):
        msm.structure.get_neighbors(_ensemble("vacuum"), threshold=threshold, pbc=False)


def test_zero_cutoff_and_empty_selections_keep_the_existing_contract():
    source = Structures(
        coordinates=msm.pyunitwizard.quantity([[[0, 0, 0], [0, 0, 0], [1, 1, 1]]], "nm")
    )
    result, _ = msm.structure.get_neighbors(source, threshold="0 nm", pbc=False)
    assert result[0, 0].tolist() == [1]
    assert result[0, 1].tolist() == [0]
    assert result[0, 2].size == 0
    csr = msm.structure.get_neighbors(
        source, selection=[], threshold="0.001 nm", pbc=False, output_type="csr"
    )
    assert csr[0].tolist() == [0]
    assert csr[1].size == csr[2].size == 0


@pytest.mark.parametrize("periodic", ["vacuum", "orthogonal", "triclinic"])
def test_contacts_share_the_bounded_search_and_exact_criterion(periodic):
    source = _ensemble(periodic)
    frames, first, second = [2, 0, 2, 1], [2, 0], [3, 1, 4]
    expected = _oracle(source, first, second, frames, periodic != "vacuum", 0.001)
    matrix = np.zeros((4, 2, 3), dtype=bool)
    for row in range(8):
        matrix[
            row // 2,
            row % 2,
            np.asarray(expected[1][expected[0][row] : expected[0][row + 1]], dtype=int),
        ] = True
    actual = msm.structure.get_contacts(
        source,
        selection=first,
        selection_2=second,
        structure_indices=frames,
        threshold="0.001 nm",
        pbc=periodic != "vacuum",
        cell_list=True,
        use_gpu=False,
    )
    np.testing.assert_array_equal(actual, matrix)


@pytest.mark.parametrize(
    "fault",
    ["cutoff_zero", "cutoff_nan", "coordinates_nan", "structures", "xyz", "box_shape"],
)
def test_compiled_boundary_rejects_invalid_layout_or_nonfinite_values_cleanly(fault):
    from molsysmt import _rust

    query = np.zeros((1, 2, 3))
    reference = np.ones((1, 2, 3))
    box, cutoff = None, 0.001
    if fault == "cutoff_zero":
        cutoff = 0.0
    if fault == "cutoff_nan":
        cutoff = float("nan")
    if fault == "coordinates_nan":
        query[0, 0, 0] = float("nan")
    if fault == "structures":
        reference = np.ones((2, 2, 3))
    if fault == "xyz":
        query = np.zeros((1, 2, 2))
    if fault == "box_shape":
        box = np.zeros((2, 3, 3))
    with pytest.raises(ValueError):
        _rust.neighbor_list_csr_multi(
            query, reference, box, cutoff, False, True, 1, memory_budget=1 << 20
        )


def test_contact_map_reservation_precedes_allocation_and_preserves_sparse_admission(
    monkeypatch,
):
    source = Structures(
        coordinates=msm.pyunitwizard.quantity(
            np.arange(900, dtype=float).reshape(1, 300, 3) * 10, "nm"
        )
    )
    monkeypatch.setattr(msm.configure, "max_ram_usage", 1 << 18)
    matrix = msm.structure.get_contacts(
        source,
        threshold="0.01 nm",
        pbc=False,
        cell_list=True,
        use_gpu=False,
        num_threads=1,
    )
    assert matrix.shape == (1, 300, 300)
    assert matrix.sum() == 300
    # The same finite input cannot reserve its map plus search workspace here.
    monkeypatch.setattr(msm.configure, "max_ram_usage", 100000)
    original = np.zeros

    def guarded(shape, *args, **kwargs):
        if shape == (1, 300, 300) and kwargs.get("dtype") is bool:
            pytest.fail("Contact map must not allocate before native budget admission")
        return original(shape, *args, **kwargs)

    monkeypatch.setattr(np, "zeros", guarded)
    with pytest.raises(msm.MemoryBudgetExceededError):
        msm.structure.get_contacts(
            source,
            threshold="0.01 nm",
            pbc=False,
            cell_list=True,
            use_gpu=False,
            num_threads=1,
        )


@pytest.mark.parametrize("periodic", [False, True])
def test_empty_structure_selection_has_typed_offsets_with_or_without_pbc(periodic):
    source = _ensemble("triclinic")
    result = msm.structure.get_neighbors(
        source,
        structure_indices=[],
        threshold="0.001 nm",
        pbc=periodic,
        output_type="csr",
    )
    assert result[0].tolist() == [0]
    assert result[0].dtype == result[1].dtype == np.int64
    assert result[1].size == result[2].size == 0
