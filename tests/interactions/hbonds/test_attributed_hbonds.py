"""Verify sparse attributed hydrogen-bond scopes, images and persistence."""

import numpy as np
import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import (
    ArgumentError,
    MemoryBudgetExceededError,
    StructuralInconsistencyError,
)

METHODS = [
    "baker_hubbard",
    "wernet_nilsson",
    "cpptraj",
    "prolif",
    "mdanalysis_geometry",
]


def _system(*, n_frames=3, periodic=False):
    molecule = Chem.AddHs(Chem.MolFromSmiles("O.O"))
    xyz = np.array(
        [
            [0, 0, 0],
            [0.28, 0, 0],
            [0.1, 0, 0],
            [0, 0.1, 0],
            [0.28, 0.1, 0],
            [0.28, 0, 0.1],
        ]
    )
    if periodic:
        xyz = np.array(
            [
                [0.86, 0, 0],
                [0.14, 0, 0],
                [0.96, 0, 0],
                [0.86, 0.1, 0],
                [0.14, 0.1, 0],
                [0.14, 0, 0.1],
            ]
        )
    coordinates = np.repeat(xyz[None], n_frames, axis=0)
    if n_frames == 3:
        coordinates[1, [1, 4, 5]] += [0, 0.4, 0]
    native = msm.convert(molecule, to_form="molsysmt.MolSys")
    native.structures.append(
        coordinates=puw.quantity(coordinates, "nm"),
        box=puw.quantity(np.repeat(np.eye(3)[None], n_frames, axis=0), "nm")
        if periodic
        else None,
    )
    native.structures.structure_id = np.array(
        [f"frame-{100 - i}" for i in range(n_frames)]
    )
    return native


def _calculate(source, method, **kwargs):
    sites = (
        dict(donor_hydrogen_pairs=[[0, 2]], acceptor_atom_indices=[1])
        if method == "mdanalysis_geometry"
        else {}
    )
    sites.update(kwargs)
    return msm.interactions.hbonds.get_hbonds(source, method=method, **sites)


@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize(
    ("mode", "first", "second", "count"),
    [
        ("internal", [0, 2, 1], None, 2),
        ("internal", [0, 2], None, 0),
        ("incident", [2], None, 2),
        ("incident", [1], None, 2),
        ("between", [0, 2], [1], 2),
        ("between", [0], [2, 1], 2),
        ("between", [1], [0, 2], 2),
    ],
)
def test_three_role_scopes_and_nonconsecutive_frames(
    method, mode, first, second, count
):
    source = _system()
    result = _calculate(
        source,
        method,
        selection=first,
        selection_2=second,
        selection_mode=mode,
        structure_indices=[2, 0, 2],
        pbc=False,
    )
    assert result.n_interactions == count
    assert result.evaluated_structure_indices.tolist() == [0, 2]
    assert result.occurrence_structures.tolist() == ([0, 2] if count else [])
    if count:
        assert result.participant_atoms.tolist() == [0, 2, 1]
        assert result.participant_roles == ("donor", "hydrogen", "acceptor")
        np.testing.assert_allclose(result.measurements["dha_angle"], np.pi)
        np.testing.assert_allclose(
            result.measurements["hydrogen_acceptor_distance"], 0.18
        )
        assert result.query(atom_indices=[2], mode="incident").to_dict()[
            "occurrence_indices"
        ].tolist() == [0, 1]
    assert not source.interactions


@pytest.mark.parametrize("method", METHODS)
def test_empty_frames_units_typed_output_and_named_h5msm(method, tmp_path):
    source = _system()
    with puw.context(standard_units=["angstrom", "degrees", "ps", "e"]):
        result = _calculate(source, method, pbc=False)
    assert result.evaluated_structure_indices.tolist() == [0, 1, 2]
    assert result.query(structure_indices=[1]).to_dict()[
        "occurrence_indices"
    ].shape == (0,)
    assert result.measure_units["dha_angle"] == "radians"
    np.testing.assert_allclose(result.measurements["donor_acceptor_distance"], 0.28)
    source.interactions = {method: result}
    path = str(tmp_path / "named.h5msm")
    msm.convert(source, to_form=path)
    restored = msm.convert(path, to_form="molsysmt.MolSys").interactions[method]
    assert restored.parameters == result.parameters
    assert restored.software == result.software
    np.testing.assert_array_equal(
        restored.to_dict()["occurrence_indices"], result.to_dict()["occurrence_indices"]
    )
    dictionary = _calculate(
        source, method, pbc=False, output_type="molsysmt.InteractionsDict"
    )
    roundtrip = msm.convert(dictionary, to_form="molsysmt.Interactions")
    np.testing.assert_array_equal(roundtrip.participant_atoms, result.participant_atoms)


@pytest.mark.parametrize("method", METHODS)
def test_observed_periodic_triplet_reconstructs_every_stored_measure(method):
    source = _system(n_frames=1, periodic=True)
    result = _calculate(source, method)
    assert result.n_interactions == 1
    images = result.image_vectors
    assert images.tolist() == [[0, 0, 0], [0, 0, 0], [1, 0, 0]]
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm")[
        0, result.participant_atoms
    ] + images @ np.eye(3)
    np.testing.assert_allclose(
        np.linalg.norm(xyz[2] - xyz[0]),
        result.measurements["donor_acceptor_distance"][0],
    )
    np.testing.assert_allclose(
        np.linalg.norm(xyz[2] - xyz[1]),
        result.measurements["hydrogen_acceptor_distance"][0],
    )


def test_chunked_native_and_h5msm_never_materialize_full_trajectory(
    monkeypatch, tmp_path
):
    source = _system(n_frames=1000)
    path = str(tmp_path / "trajectory.h5msm")
    msm.convert(source, to_form=path)
    monkeypatch.setattr(msm.configure, "chunk_size", 7)
    monkeypatch.setattr(msm.configure, "max_ram_usage", 2_000_000)
    for input_system in (source, path):
        result = _calculate(
            input_system, "baker_hubbard", heavy_mode="force", pbc=False
        )
        assert result.n_interactions == 1000
        assert result.execution_records[0]["details"]["execution_chunks"] == 143
        assert result.execution_records[0]["details"]["execution"] == "chunked"
    from molsysmt.form import _h5msm05_modular

    monkeypatch.setattr(
        _h5msm05_modular,
        "read_molsys_file",
        lambda *args, **kwargs: pytest.fail("Full H5MSM load was attempted."),
    )
    selected = _calculate(
        path,
        "cpptraj",
        heavy_mode="force",
        pbc=False,
        structure_indices=[998, 1, 500, 1],
    )
    assert selected.occurrence_structures.tolist() == [1, 500, 998]


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(donor_hydrogen_pairs=[[0, 2]]),
        dict(donor_hydrogen_pairs=[[0, 1]], acceptor_atom_indices=[1]),
        dict(donor_hydrogen_pairs=[[0.0, 2.0]], acceptor_atom_indices=[1]),
        dict(donor_hydrogen_pairs=[[0, 2]], acceptor_atom_indices=[100]),
        dict(method="mdanalysis_geometry"),
        dict(distance_threshold="2 ps"),
        dict(angle_threshold="190 degrees"),
        dict(method="wernet_nilsson", angle_threshold="20 degrees"),
        dict(selection_mode="between", selection=[0], selection_2=[0]),
    ],
)
def test_invalid_public_inputs_raise_before_calculation(kwargs):
    with pytest.raises(ArgumentError):
        msm.interactions.hbonds.get_hbonds(_system(), **kwargs)


def test_periodic_reference_limits_are_explicit():
    source = _system(n_frames=1, periodic=True)
    coordinates = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    coordinates[0, 2, 0] = -0.04
    source.structures.coordinates = puw.quantity(coordinates, "nm")
    with pytest.raises(StructuralInconsistencyError, match="whole donor-H"):
        _calculate(source, "cpptraj")
    assert _calculate(source, "baker_hubbard").n_interactions == 1
    coordinates = coordinates.copy()
    coordinates[0, [0, 2, 1], 0] = [0, 0.4, 0.6]
    source.structures.coordinates = puw.quantity(coordinates, "nm")
    with pytest.raises(StructuralInconsistencyError, match="one observed triplet"):
        _calculate(source, "prolif", distance_threshold=".6 nm")


def test_resident_result_budget_fails_explicitly(monkeypatch):
    source = _system(n_frames=1000)
    monkeypatch.setattr(msm.configure, "max_ram_usage", 100_000)
    with pytest.raises(MemoryBudgetExceededError):
        _calculate(source, "baker_hubbard", heavy_mode="force", pbc=False)


@pytest.mark.parametrize(
    ("method", "count"),
    [
        ("baker_hubbard", 0),
        ("cpptraj", 1),
        ("mdanalysis_geometry", 0),
        ("prolif", 1),
    ],
)
def test_straight_angle_endpoint_preserves_strict_and_inclusive_rules(method, count):
    result = _calculate(
        _system(n_frames=1), method, angle_threshold="180 degrees", pbc=False
    )
    assert result.n_interactions == count


@pytest.mark.parametrize(
    ("pairs", "acceptors"),
    [
        ([[False, 2]], [1]),
        ([[0, 2]], [True, 1]),
        ([[0, 2]], np.array([2**63], dtype=np.uint64)),
    ],
)
def test_explicit_sites_reject_boolean_coercion_and_integer_overflow(pairs, acceptors):
    with pytest.raises(ArgumentError):
        _calculate(
            _system(n_frames=1),
            "mdanalysis_geometry",
            donor_hydrogen_pairs=pairs,
            acceptor_atom_indices=acceptors,
            pbc=False,
        )
