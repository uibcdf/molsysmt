"""Protect original-frame pose comparisons and declared geometric clustering."""

from copy import deepcopy

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    ArgumentError,
    MemoryBudgetExceededError,
    StructuralInconsistencyError,
    UnsupportedHeavyOperationError,
)
from molsysmt.native import Structures

puw = msm.pyunitwizard


def population(n=4, unit="nm"):
    molsys = Structures()
    xyz = np.zeros((n, 2, 3))
    xyz[:, :, 0] = np.arange(n)[:, None]
    xyz[:, 1, 1] = 0.5
    molsys.coordinates = puw.convert(puw.quantity(xyz, "nm"), to_unit=unit)
    return molsys


def chain():
    return puw.quantity([[0.0, 1.0, 2.0], [1.0, 0.0, 1.0], [2.0, 1.0, 0.0]], "nm")


def test_original_positions_order_repetitions_witnesses_and_no_mutation():
    molsys = population()
    before = puw.get_value(molsys.coordinates).copy()
    result = msm.structure.get_pairwise_rmsd(
        molsys,
        selection=[1, 0],
        structure_indices=[3, 0, 2, 3],
        member_keys=["pose-d", "pose-a", "pose-c", "pose-d-again"],
    )
    expected = np.abs(np.subtract.outer([3.0, 0.0, 2.0, 3.0], [3.0, 0.0, 2.0, 3.0]))
    np.testing.assert_allclose(puw.get_value(result["rmsd"], to_unit="nm"), expected)
    assert result["structure_indices"].tolist() == [3, 0, 2, 3]
    assert result["atom_indices"].tolist() == [0, 1]
    assert result["pair_indices"].tolist() == [
        [1, 0],
        [2, 0],
        [3, 0],
        [2, 1],
        [3, 1],
        [3, 2],
    ]
    assert result["correspondence_indices"].tolist() == [-1] * 6
    assert result["n_near_optimal_correspondences"].tolist() == [1] * 6
    assert result["alignment"] == result["periodic_imaging"] == "none"
    assert not result["chemistry_checked"] and result["correspondences"] is None
    puw.get_value(result["rmsd"])[0, 1] = 999
    np.testing.assert_array_equal(puw.get_value(molsys.coordinates), before)


@pytest.mark.parametrize("unit", ["nm", "pm", "angstrom"])
def test_units_and_session_output_policy(unit):
    with puw.context(standard_units=["angstrom", "ps"]):
        pairwise = msm.structure.get_pairwise_rmsd(
            population(unit=unit), selection="all"
        )
        np.testing.assert_allclose(puw.get_value(pairwise["rmsd"])[0], [0, 10, 20, 30])
        clustered = msm.structure.get_distance_clusters(
            pairwise["rmsd"], "11 angstrom", member_keys=pairwise["member_keys"]
        )
        assert clustered["cluster_indices"].tolist() == [0, 0, 1, 1]
        np.testing.assert_allclose(
            puw.get_value(clustered["cluster_diameters"]), [10, 10]
        )


@pytest.mark.parametrize("indices", [[], [2]])
def test_empty_and_singleton_are_typed(indices):
    result = msm.structure.get_pairwise_rmsd(
        population(), selection="all", structure_indices=indices
    )
    assert result["rmsd"].shape == (len(indices), len(indices))
    assert result["pair_indices"].shape == (0, 2)
    assert result["correspondence_indices"].dtype == np.int64
    clusters = msm.structure.get_distance_clusters(result["rmsd"], "0 nm")
    assert clusters["cluster_offsets"].tolist() == ([0] if not indices else [0, 1])
    assert clusters["representative_indices"].tolist() == ([] if not indices else [0])


def test_linkage_chain_exact_cutoff_ties_and_representatives():
    matrix = chain()
    original = puw.get_value(matrix).copy()
    complete = msm.structure.get_distance_clusters(
        matrix, "1 nm", member_keys=["a", "b", "c"]
    )
    single = msm.structure.get_distance_clusters(
        matrix, "1 nm", method="single_linkage"
    )
    assert complete["cluster_indices"].tolist() == [0, 0, 1]
    assert complete["cluster_offsets"].tolist() == [0, 2, 3]
    assert complete["member_indices"].tolist() == [0, 1, 2]
    assert complete["representative_indices"].tolist() == [0, 2]
    assert single["cluster_indices"].tolist() == [0, 0, 0]
    assert single["representative_indices"].tolist() == [1]
    assert puw.get_value(single["cluster_diameters"], to_unit="nm").tolist() == [2.0]
    first = msm.structure.get_distance_clusters(
        matrix, "1 nm", method="single_linkage", representative="first"
    )
    assert first["representative_indices"].tolist() == [0]
    below = msm.structure.get_distance_clusters(
        matrix, puw.quantity(np.nextafter(1.0, 0.0), "nm")
    )
    assert below["cluster_indices"].tolist() == [0, 1, 2]
    puw.get_value(complete["cluster_diameters"])[:] = 99
    np.testing.assert_array_equal(puw.get_value(matrix), original)


def test_duplicate_members_and_detached_keys():
    keys = ["first", "second", "third"]
    result = msm.structure.get_distance_clusters(
        puw.quantity(np.zeros((3, 3)), "nm"), "0 nm", member_keys=keys
    )
    assert result["cluster_indices"].tolist() == [0, 0, 0]
    assert result["representative_indices"].tolist() == [0]
    result["member_keys"][0] = "changed"
    assert keys[0] == "first"


@pytest.mark.parametrize(
    "matrix",
    [
        [[0, 1], [2, 0]],
        [[1, 0], [0, 0]],
        [[0, -1], [-1, 0]],
        [[0, np.nan], [np.nan, 0]],
        [[0, np.inf], [np.inf, 0]],
    ],
)
def test_invalid_distances_are_not_repaired(matrix):
    with pytest.raises(StructuralInconsistencyError):
        msm.structure.get_distance_clusters(puw.quantity(matrix, "nm"), "1 nm")


@pytest.mark.parametrize(
    "kwargs",
    [
        {"cutoff_distance": "-1 nm"},
        {"cutoff_distance": "nan nm"},
        {"cutoff_distance": "1 ps"},
        {"cutoff_distance": puw.quantity([1], "nm")},
        {"method": "average"},
        {"representative": "best_score"},
        {"member_keys": ["a", "a", "b"]},
        {"member_keys": ["a"]},
        {"max_work": True},
        {"max_work": 0},
    ],
)
def test_cluster_public_arguments_reject_unsupported_claims(kwargs):
    with pytest.raises(ArgumentError):
        msm.structure.get_distance_clusters(
            chain(), **({"cutoff_distance": "1 nm"} | kwargs)
        )


@pytest.mark.parametrize(
    "distances",
    [
        np.zeros((2, 2)),
        puw.quantity([1, 2], "nm"),
        puw.quantity(np.zeros((2, 3)), "nm"),
        puw.quantity(np.zeros((2, 2)), "ps"),
    ],
)
def test_matrix_units_and_shape_are_explicit(distances):
    with pytest.raises(ArgumentError):
        msm.structure.get_distance_clusters(distances, "1 nm")


@pytest.mark.parametrize(
    "indices", [[True], [[0]], [0.5], [-1], [5], puw.quantity([0], "dimensionless")]
)
def test_structure_indices_are_positions(indices):
    with pytest.raises(ArgumentError):
        msm.structure.get_pairwise_rmsd(
            population(), selection="all", structure_indices=indices
        )


def test_nonfinite_coordinates_are_rejected_even_for_singleton():
    molsys = population()
    xyz = puw.get_value(molsys.coordinates).copy()
    xyz[0, 0, 0] = np.nan
    molsys.coordinates = puw.quantity(xyz, "nm")
    with pytest.raises(StructuralInconsistencyError):
        msm.structure.get_pairwise_rmsd(molsys, selection="all", structure_indices=[0])
    # Empty request promises no coordinate evaluation, not a false finite claim.
    result = msm.structure.get_pairwise_rmsd(
        molsys, selection="all", structure_indices=[]
    )
    assert result["execution"]["execution"] == "empty"


def test_work_and_memory_rejection_precede_coordinate_delivery(monkeypatch):
    import molsysmt._private.execution.projected_geometry as delivery

    molsys = population(32)
    monkeypatch.setattr(
        delivery,
        "execute_projected_geometry",
        lambda *a, **k: pytest.fail("coordinate read before budget rejection"),
    )
    with pytest.raises(UnsupportedHeavyOperationError):
        msm.structure.get_pairwise_rmsd(molsys, selection="all", max_work=10)
    with pytest.raises(UnsupportedHeavyOperationError):
        msm.structure.get_distance_clusters(chain(), "1 nm", max_work=1)
    monkeypatch.setattr(msm.configure, "max_ram_usage", 100)
    with pytest.raises(MemoryBudgetExceededError):
        msm.structure.get_pairwise_rmsd(molsys, selection="all")
    with pytest.raises(MemoryBudgetExceededError):
        msm.structure.get_distance_clusters(chain(), "1 nm")


def benzene():
    from rdkit import Chem

    molsys = msm.convert(Chem.MolFromSmiles("c1ccccc1"), to_form="molsysmt.MolSys")
    phase = np.arange(6) * 2 * np.pi / 6
    xyz = np.column_stack((np.cos(phase), np.sin(phase), np.zeros(6))) * 0.14
    molsys.structures.append(
        coordinates=puw.quantity(
            [xyz, xyz[np.roll(np.arange(6), -1)], xyz + [0, 0, 0.2]], "nm"
        )
    )
    return molsys


def test_symmetry_matches_analytic_geometry_and_public_single_reference():
    molsys = benzene()
    result = msm.structure.get_pairwise_rmsd(molsys, method="symmetry_corrected")
    expected = [[0, 0, 0.2], [0, 0, 0.2], [0.2, 0.2, 0]]
    np.testing.assert_allclose(
        puw.get_value(result["rmsd"], to_unit="nm"), expected, atol=1e-14
    )
    assert result["chemistry_checked"]
    for pair, winner, tie_count in zip(
        result["pair_indices"],
        result["correspondence_indices"],
        result["n_near_optimal_correspondences"],
    ):
        query, reference = pair
        single = msm.structure.get_symmetry_corrected_rmsd(
            molsys, structure_indices=[query], reference_structure_index=int(reference)
        )
        assert winner == single["correspondence_indices"][0]
        assert tie_count == single["n_near_optimal_correspondences"][0]


def test_closed_candidate_scope_and_detached_evidence():
    molsys = benzene()
    identity = np.column_stack((np.arange(6), np.arange(6)))
    cached = msm.chemical_states.get_atom_correspondences(
        molsys, candidate_atom_correspondences=identity
    )
    result = msm.structure.get_pairwise_rmsd(
        molsys, method="symmetry_corrected", correspondences=cached
    )
    assert result["search_scope"] == "supplied_atom_correspondences"
    assert puw.get_value(result["rmsd"], to_unit="nm")[0, 1] == pytest.approx(0.14)
    result["correspondences"]["atom_correspondences"][:] = -1
    assert np.all(cached["atom_correspondences"] >= 0)


@pytest.mark.parametrize("include_identity", [False, True])
def test_directional_or_nonreflexive_candidate_sets_are_refused(include_identity):
    molsys = benzene()
    rotation = np.column_stack((np.arange(6), np.roll(np.arange(6), -1)))
    maps = [rotation]
    if include_identity:
        maps.append(np.column_stack((np.arange(6), np.arange(6))))
    cached = msm.chemical_states.get_atom_correspondences(
        molsys, candidate_atom_correspondences=maps
    )
    with pytest.raises(ArgumentError):
        msm.structure.get_pairwise_rmsd(
            molsys, method="symmetry_corrected", correspondences=cached
        )


def test_mutated_chemistry_cache_is_not_trusted():
    molsys = benzene()
    cached = msm.chemical_states.get_atom_correspondences(molsys)
    bad = deepcopy(cached)
    bad["atom_correspondences"][0, 0, 1] = 100
    with pytest.raises(ArgumentError):
        msm.structure.get_pairwise_rmsd(
            molsys, method="symmetry_corrected", correspondences=bad
        )


def test_anchored_maps_are_built_once_and_scope_is_retained(monkeypatch):
    molsys = benzene()
    cached = msm.chemical_states.get_atom_correspondences(
        molsys, fixed_atom_correspondence=[[0, 0]]
    )
    monkeypatch.setattr(
        msm.chemical_states,
        "get_atom_correspondences",
        lambda *a, **k: pytest.fail("repeated chemical search"),
    )
    result = msm.structure.get_pairwise_rmsd(
        molsys, method="symmetry_corrected", correspondences=cached
    )
    assert result["search_scope"] == "anchored_chemical_correspondences"
    assert result["execution"]["estimated_work"] == 3 * 6 * len(
        cached["atom_correspondences"]
    )


@pytest.mark.parametrize("selection", [[], [0, 0], [100]])
def test_atom_population_requires_unique_existing_atoms(selection):
    with pytest.raises(ArgumentError):
        msm.structure.get_pairwise_rmsd(population(), selection=selection)


def test_h5msm_selected_chunks_match_native_without_whole_coordinate_read(
    tmp_path, monkeypatch
):
    import h5py

    molsys = benzene()
    path = str(tmp_path / "poses.h5msm")
    msm.convert(molsys, to_form=path)
    original = h5py.Dataset.__getitem__
    reads = []

    def guarded(dataset, key):
        if dataset.name.endswith("/coordinates"):
            reads.append(key)
            assert key != () and key is not Ellipsis
            rows = key[0] if isinstance(key, tuple) else key
            if isinstance(rows, slice):
                assert len(range(*rows.indices(dataset.shape[0]))) <= 1
            elif not np.isscalar(rows):
                assert len(rows) <= 1
        return original(dataset, key)

    monkeypatch.setattr(h5py.Dataset, "__getitem__", guarded)
    with msm.configure.context(chunk_size=1):
        observed = msm.structure.get_pairwise_rmsd(
            path,
            structure_indices=[2, 0, 2],
            method="symmetry_corrected",
            heavy_mode="force",
        )
    expected = msm.structure.get_pairwise_rmsd(
        molsys, structure_indices=[2, 0, 2], method="symmetry_corrected"
    )
    np.testing.assert_allclose(
        puw.get_value(observed["rmsd"]), puw.get_value(expected["rmsd"])
    )
    assert observed["execution"]["execution"] == "chunked" and reads
    assert observed["execution"]["n_blocks"] == 3


def test_prepared_atom_reordering_does_not_change_pairwise_geometry():
    molsys = benzene()
    changed = msm.permute_atoms(molsys, [4, 0, 2, 1, 5, 3])
    first = msm.structure.get_pairwise_rmsd(molsys, method="symmetry_corrected")
    second = msm.structure.get_pairwise_rmsd(changed, method="symmetry_corrected")
    np.testing.assert_allclose(
        puw.get_value(first["rmsd"]), puw.get_value(second["rmsd"]), atol=1e-14
    )


def test_attribution_is_per_operation_and_survives_absence(monkeypatch):
    from molsysmt import _ackredit

    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    absent = msm.structure.get_distance_clusters(chain(), "1 nm")
    events = []

    class Provider:
        def scope(self, target):
            from contextlib import nullcontext

            return nullcontext()

        def register_item(self, **record):
            events.append(("register", record))

        def track_item(self, item, **context):
            events.append(("track", item, context))

    monkeypatch.setattr(_ackredit, "backend", Provider)
    present = msm.structure.get_distance_clusters(chain(), "1 nm")
    assert present["references"] == absent["references"]
    assert len([event for event in events if event[0] == "track"]) == 3
    assert {
        item["id"].split(":")[1]
        for item in present["attribution"]["items"]
        if item["type"] == "software"
    } == {"molsysmt", "numpy"}
    assert present["references"][0]["id"] == "arxiv:1109.2378"
    events.clear()
    msm.structure.get_pairwise_rmsd(population(32), selection="all")
    assert len([event for event in events if event[0] == "track"]) == 1


def test_cubic_clustering_matches_independent_set_definition():
    # The independent oracle recomputes cross-member distances, without the
    # production recurrence or retained matrix-row labels.
    values = np.abs(
        np.subtract.outer([0.0, 0.2, 0.9, 1.4, 2.8], [0.0, 0.2, 0.9, 1.4, 2.8])
    )
    for method in ("complete_linkage", "single_linkage"):
        for cutoff in (0.0, 0.5, 1.0, 3.0):
            clusters = [[i] for i in range(len(values))]
            while len(clusters) > 1:
                choices = []
                for i, first in enumerate(clusters):
                    for j in range(i + 1, len(clusters)):
                        cross = [values[a, b] for a in first for b in clusters[j]]
                        distance = (
                            max(cross) if method == "complete_linkage" else min(cross)
                        )
                        choices.append((distance, min(first), min(clusters[j]), i, j))
                distance, _, _, i, j = min(choices)
                if distance > cutoff:
                    break
                clusters[i] = sorted(clusters[i] + clusters.pop(j))
            result = msm.structure.get_distance_clusters(
                puw.quantity(values, "nm"), puw.quantity(cutoff, "nm"), method=method
            )
            actual = [
                result["member_indices"][a:b].tolist()
                for a, b in zip(
                    result["cluster_offsets"][:-1], result["cluster_offsets"][1:]
                )
            ]
            assert actual == clusters


def test_positional_path_does_not_import_the_optional_chemistry_engine():
    import subprocess
    import sys

    script = """
import sys
import numpy as np
import molsysmt as msm
from molsysmt.native import Structures
molsys = Structures(coordinates=msm.pyunitwizard.quantity(np.zeros((2, 2, 3)), 'nm'))
result = msm.structure.get_pairwise_rmsd(molsys, selection='all')
assert 'rdkit' not in sys.modules
assert not result['chemistry_checked']
assert set(result['software']) == {'molsysmt'}
"""
    process = subprocess.run(
        [sys.executable, "-c", script], text=True, capture_output=True, timeout=30
    )
    assert process.returncode == 0, process.stdout + process.stderr


def test_finite_input_overflow_is_a_failed_comparison():
    coordinates = np.zeros((2, 1, 3))
    coordinates[0, 0, 0] = np.finfo(np.float64).max
    coordinates[1, 0, 0] = -np.finfo(np.float64).max
    molsys = Structures(coordinates=puw.quantity(coordinates, "nm"))
    with pytest.raises(StructuralInconsistencyError):
        msm.structure.get_pairwise_rmsd(molsys, selection="all")
