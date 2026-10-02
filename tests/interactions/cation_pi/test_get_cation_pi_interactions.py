"""Protect attributed cation-pi geometry, source axes, image and persistence contracts."""

import numpy as np
import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import (
    ArgumentError,
    MemoryBudgetExceededError,
    NotImplementedMethodError,
    StructuralInconsistencyError,
    UnsupportedHeavyOperationError,
)


def _hexagon():
    angles = np.arange(6) * np.pi / 3
    return np.column_stack((0.14 * np.cos(angles), 0.14 * np.sin(angles), np.zeros(6)))


def _system(
    points=((0.0, 0.0, 0.35),), *, smiles="c1ccccc1.[NH4+]", box=None, ring=None
):
    molecule = Chem.MolFromSmiles(smiles)
    xyz = np.asarray(
        [
            np.vstack(
                (_hexagon() if ring is None else ring, np.asarray(point).reshape(-1, 3))
            )
            for point in points
        ]
    )
    molsys = msm.convert(molecule, to_form="molsysmt.MolSys")
    assert xyz.shape[1] == len(molsys.topology.atoms)
    molsys.structures.append(
        coordinates=puw.quantity(xyz, "nm"),
        box=None if box is None else puw.quantity(np.asarray(box), "nm"),
    )
    molsys.structures.structure_id = np.asarray(
        [f"structure-{90 - i}" for i in range(len(xyz))]
    )
    return molsys


def _calculate(source, *, method="prolif", **kwargs):
    options = dict(pbc=False, method=method)
    if method != "prolif":
        options.update(
            distance_threshold=".45 nm",
            angle_threshold="30 degrees",
            offset_threshold=".2 nm",
            planarity_threshold=".02 nm",
        )
    options.update(kwargs)
    return msm.interactions.cation_pi.get_cation_pi_interactions(source, **options)


def _assert_same(actual, expected):
    for name in (
        "participant_atoms",
        "participant_atom_offsets",
        "occurrence_structures",
        "occurrence_relations",
        "evaluated_structure_indices",
        "atom_source_indices",
        "structure_source_indices",
        "image_vectors",
    ):
        np.testing.assert_array_equal(getattr(actual, name), getattr(expected, name))
    assert (
        actual.relation_types == expected.relation_types
        and actual.participant_roles == expected.participant_roles
    )
    assert (
        actual.measure_units == expected.measure_units
        and actual.software == expected.software
    )
    np.testing.assert_array_equal(
        np.asarray(actual.evidence_labels)[actual.occurrence_evidence],
        np.asarray(expected.evidence_labels)[expected.occurrence_evidence],
    )
    for name, column in expected.measurements.items():
        np.testing.assert_allclose(
            actual.measurements[name], column, atol=1e-12, rtol=0
        )


@pytest.mark.parametrize("method", ["prolif", "centroid_angle_offset"])
def test_cation_pi_retains_roles_sparse_frames_coverage_and_producer(method):
    molsys = _system([(0, 0, 0.35), (0, 0, 2), (0.1, 0, -0.35)])
    result = _calculate(molsys, method=method, structure_indices=[2, 0, 2, 1])
    assert result.n_interactions == 2 and result.relation_types == ("cation_pi",)
    assert result.participant_roles == ("cation", "ring")
    assert result.relation(0)["participants"][0]["atom_indices"].tolist() == [6]
    assert result.evaluated_structure_indices.tolist() == [0, 1, 2]
    assert result.occurrence_structures.tolist() == [0, 2]
    assert result.query(structure_indices=1).n_interactions == 0
    assert result.query(atom_indices=6, structure_indices=[2, 0, 2]).n_interactions == 2
    assert result.query(atom_indices=6, mode="internal").n_interactions == 0
    assert result.query(atom_indices=6, mode="cross").n_interactions == 2
    assert (
        result.query(atom_indices=list(range(7)), mode="internal").n_interactions == 2
    )
    np.testing.assert_allclose(result.measurements["height"], [0.35, 0.35], atol=1e-12)
    np.testing.assert_allclose(
        result.measurements["distance"], [0.35, np.hypot(0.1, 0.35)], atol=1e-12
    )
    assert (
        result.measure_units["normal_angle"] == "radians"
        and result.measure_units["cation_charge"] == "e"
    )
    assert result.software["molsysmt"] == msm.__version__
    assert not molsys.interactions
    if method == "prolif":
        assert result.parameters["method_reference"]["version"] == "2.2.2"
        assert result.parameters["cutoff_roundoff"] == "none"
        assert result.parameters["exclude_direct_covalent"] is False
    else:
        assert result.parameters["method_reference"] is None


@pytest.mark.parametrize("method", ["prolif", "centroid_angle_offset"])
@pytest.mark.parametrize(
    ("mode", "first", "second", "count"),
    [
        ("internal", [6], None, 0),
        ("internal", list(range(7)), None, 1),
        ("incident", [6], None, 1),
        ("incident", list(range(6)), None, 1),
        ("between", [6], list(range(6)), 1),
        ("between", list(range(6)), [6], 1),
    ],
)
def test_selections_include_both_chemical_role_orientations(
    method, mode, first, second, count
):
    result = _calculate(
        _system(),
        method=method,
        selection=first,
        selection_2=second,
        selection_mode=mode,
    )
    assert result.n_interactions == count
    assert result.evaluation_mode == mode
    if count:
        assert result.participant_roles == ("cation", "ring")


@pytest.mark.parametrize("method", ["prolif", "centroid_angle_offset"])
@pytest.mark.parametrize(
    ("x", "z", "accepted"),
    [
        (0, 0.449, True),
        (0, 0.451, False),
        (0.17, 0.35, True),
        (0.23, 0.35, False),
        (0, -0.35, True),
        (0.35, 0, False),
        (0, 0, False),
    ],
)
def test_analytical_distance_and_normal_angle_near_misses(method, x, z, accepted):
    assert (
        bool(_calculate(_system([(x, 0, z)]), method=method).n_interactions) == accepted
    )


def test_prolif_interval_and_no_added_offset_or_planarity_filter():
    source = _system([(0.25, 0, 0.35)])
    interval = puw.quantity([30, 40], "degrees")
    assert _calculate(source, angle_threshold=interval).n_interactions == 1
    assert _calculate(source, angle_threshold="40 degrees").n_interactions == 1
    assert _calculate(source).n_interactions == 0
    assert (
        _calculate(
            source, method="centroid_angle_offset", angle_threshold="40 degrees"
        ).n_interactions
        == 0
    )
    warped = _hexagon()
    warped[:, 2] = np.array([1, -1, 1, -1, 1, -1]) * 0.03
    source = _system([(0, 0, 0.35)], ring=warped)
    assert _calculate(source, angle_threshold="89 degrees").n_interactions == 1
    assert _calculate(source, method="centroid_angle_offset").n_interactions == 0
    assert (
        _calculate(
            source, method="centroid_angle_offset", planarity_threshold=".04 nm"
        ).n_interactions
        == 1
    )


def test_prolif_resonance_atoms_are_distinct_from_whole_custom_centers():
    points = np.array([[0, 0, 0.32], [0, 0, 0.35], [0.025, 0, 0.38], [-0.025, 0, 0.38]])
    source = _system([points], smiles="c1ccccc1.NC(=[NH2+])N")
    known = _calculate(source)
    custom = _calculate(source, method="centroid_angle_offset")
    assert known.n_interactions == 3 and custom.n_interactions == 1
    assert sorted(known.measurements["cation_charge"].tolist()) == [0.0, 0.0, 1.0]
    assert custom.relation(0)["participants"][0]["atom_indices"].tolist() == [
        6,
        7,
        8,
        9,
    ]
    np.testing.assert_allclose(
        custom.measurements["height"], [points[:, 2].mean()], atol=1e-12
    )
    with pytest.raises(ArgumentError):
        _calculate(
            source,
            method="centroid_angle_offset",
            selection=[8],
            selection_mode="incident",
        )
    assert (
        _calculate(source, selection=[8], selection_mode="incident").n_interactions == 1
    )


@pytest.mark.parametrize("method", ["prolif", "centroid_angle_offset"])
def test_named_h5msm_dictionary_and_block_round_trip(method, tmp_path):
    source = _system([(0, 0, 0.35), (0, 0, 2), (0.1, 0, 0.35)])
    result = _calculate(source, method=method)
    dictionary = _calculate(
        source, method=method, output_type="molsysmt.InteractionsDict"
    )
    _assert_same(msm.convert(dictionary, to_form="molsysmt.Interactions"), result)
    source.interactions = {"cation": result}
    path = str(tmp_path / "cation.h5msm")
    msm.convert(source, to_form=path)
    saved = msm.convert(path, to_form="molsysmt.MolSys").interactions["cation"]
    _assert_same(saved, result)
    assert saved.parameters == result.parameters
    np.testing.assert_array_equal(
        saved.query().to_dict()["occurrence_indices"],
        result.query().to_dict()["occurrence_indices"],
    )
    with msm.configure.context(chunk_size=1):
        _assert_same(_calculate(path, method=method, heavy_mode="force"), result)
    alone = str(tmp_path / "analysis.h5msm")
    result.save(alone)
    _assert_same(msm.Interactions.load(alone), result)
    mapped = result.remap(atom_indices=[6, 5, 4, 3, 2, 1, 0], structure_indices=[2, 0])
    assert mapped.atom_source_indices.tolist() == [6, 5, 4, 3, 2, 1, 0]
    assert mapped.structure_source_indices.tolist() == [2, 0]
    assert mapped.query(atom_indices=0).n_interactions == 2


@pytest.mark.parametrize("method", ["prolif", "centroid_angle_offset"])
@pytest.mark.parametrize(
    "box",
    [
        np.eye(3) * 2,
        np.array([[0.0, 2, 0], [-2.0, 0, 0], [0, 0, 2.0]]),
        np.array([[2.0, 0, 0], [0.3, 2.0, 0], [0.1, 0.2, 2.0]]),
    ],
)
def test_periodic_ring_image_relative_to_cation(method, box):
    ring = _hexagon() + box[0]
    source = _system([(0, 0, 0.35)], ring=ring, box=[box])
    assert _calculate(source, method=method).n_interactions == 0
    result = _calculate(source, method=method, pbc=True)
    assert result.image_vectors.tolist() == [[0, 0, 0], [-1, 0, 0]]
    np.testing.assert_allclose(result.measurements["distance"], [0.35], atol=1e-12)
    ring[1] += box[0]
    source = _system([(0, 0, 0.35)], ring=ring, box=[box])
    with pytest.raises(NotImplementedMethodError):
        _calculate(source, method=method, pbc=True)


@pytest.mark.parametrize("method", ["prolif", "centroid_angle_offset"])
def test_unit_policy_and_coordinate_units_are_independent(method):
    source = _system([(0.1, 0, 0.35)])
    expected = _calculate(source, method=method)
    with puw.context(
        standard_units=[
            "angstrom",
            "degrees",
            "ps",
            "dalton",
            "e",
            "K",
            "mole",
            "kJ/mol",
            "kJ/(mol*nm)",
            "kJ/(mol*nm**2)",
        ]
    ):
        source.structures.coordinates = puw.convert(
            source.structures.coordinates, to_unit="angstrom"
        )
        actual = _calculate(
            source,
            method=method,
            distance_threshold="4.5 angstrom",
            angle_threshold=".5235987755982988 radians",
        )
        _assert_same(actual, expected)
        assert actual.measure_units["distance"] == "nm"


@pytest.mark.parametrize("method", ["prolif", "centroid_angle_offset"])
def test_invalid_coordinates_boxes_and_empty_results(method):
    source = _system([(0, 0, 5.0)])
    result = _calculate(source, method=method)
    assert result.evaluated_structure_indices.tolist() == [0]
    assert result.n_interactions == 0
    assert all(
        values.shape == (0,) and values.dtype == np.float64
        for values in result.measurements.values()
    )
    source.structures.coordinates = puw.quantity(np.full((1, 7, 3), np.nan), "nm")
    with pytest.raises(StructuralInconsistencyError):
        _calculate(source, method=method)
    source = _system(box=[np.zeros((3, 3))])
    with pytest.raises(StructuralInconsistencyError):
        _calculate(source, method=method, pbc=True)
    assert (
        _calculate(
            source, method=method, structure_indices=[]
        ).evaluated_structure_indices.size
        == 0
    )


@pytest.mark.parametrize("method", ["prolif", "centroid_angle_offset"])
def test_coordinate_file_route_does_not_load_saved_analyses(
    method, tmp_path, monkeypatch
):
    source = _system([(0, 0, 0.35), (0, 0, 2), (0.1, 0, 0.35)])
    source.interactions = {"already": _calculate(source, method=method)}
    path = str(tmp_path / "source.h5msm")
    msm.convert(source, to_form=path)
    from molsysmt.interactions.result import Interactions

    def reject(*args, **kwargs):
        raise AssertionError(
            "Saved analyses must not be materialized during a file calculation."
        )

    monkeypatch.setattr(Interactions, "_read_group", reject)
    with msm.configure.context(chunk_size=1):
        result = _calculate(
            path, method=method, structure_indices=[2, 0, 2], heavy_mode="force"
        )
    assert result.occurrence_structures.tolist() == [0, 2]
    assert result.execution_records[0]["details"]["execution_chunks"] == 2


@pytest.mark.parametrize("method", ["prolif", "centroid_angle_offset"])
def test_axis_and_projected_block_budget_refusals(method):
    source = _system()
    with msm.configure.context(max_ram_usage=1):
        with pytest.raises(MemoryBudgetExceededError):
            _calculate(source, method=method)
    with msm.configure.context(max_ram_usage=4096):
        with pytest.raises((UnsupportedHeavyOperationError, MemoryBudgetExceededError)):
            _calculate(source, method=method, heavy_mode="force")


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(distance_threshold="0 nm"),
        dict(distance_threshold="1 ps"),
        dict(angle_threshold="91 degrees"),
        dict(method="CAPTURE"),
        dict(offset_threshold=".1 nm"),
        dict(planarity_threshold=".01 nm"),
        dict(selection=[0]),
        dict(selection_2=[6]),
        dict(selection_mode="between", selection_2=[6]),
        dict(structure_indices=[3]),
    ],
)
def test_invalid_public_arguments_fail(kwargs):
    with pytest.raises(ArgumentError):
        _calculate(_system(), **kwargs)
