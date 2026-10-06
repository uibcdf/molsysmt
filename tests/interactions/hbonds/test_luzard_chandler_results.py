"""Check sparse angular observations against explicit molecular geometry."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import InternalAlgorithmError, NotImplementedMethodError


def _varying_system():
    builder = msm.MolSysBuilder()
    atoms = [
        builder.add_atom(atom_name=name, atom_type=kind)
        for name, kind in (("N", "N"), ("H", "H"), ("O", "O"), ("O", "O"))
    ]
    builder.add_group(atoms[:2], group_name="ALA")
    builder.add_group(atoms[2:], group_name="ALA")
    builder.add_bond(atoms[0], atoms[1])
    builder.set_coordinates(
        puw.quantity(
            [
                [[0, 0, 0], [0.1, 0, 0], [0.3, 0, 0], [0.8, 0, 0]],
                [[0, 0, 0], [0.1, 0, 0], [0.7, 0, 0], [0.8, 0, 0]],
                [[0, 0, 0], [0.1, 0, 0], [0.3, 0, 0], [0.31, 0, 0]],
                [[0, 0, 0], [0.1, 0, 0], [0, 0.3, 0], [0.8, 0, 0]],
            ],
            "nm",
        )
    )
    return builder.build()


def test_luzard_chandler_preserves_variable_counts_and_empty_frames():
    atoms, distances, angles = msm.interactions.hbonds.get_luzard_chandler_hbonds(
        _varying_system(), structure_indices=[2, 1, 0, 3, 2], pbc=False
    )
    assert all(isinstance(value, list) for value in (atoms, distances, angles))
    assert [frame.shape for frame in atoms] == [(2, 3), (0, 3), (1, 3), (0, 3), (2, 3)]
    assert [frame.shape for frame in distances] == [(2,), (0,), (1,), (0,), (2,)]
    assert [frame.shape for frame in angles] == [(2,), (0,), (1,), (0,), (2,)]
    assert atoms[0].tolist() == [[0, 1, 2], [0, 1, 3]]
    assert atoms[2].tolist() == [[0, 1, 2]]
    for observed, expected, observed_angles in zip(
        distances, ([0.3, 0.31], [], [0.3], [], [0.3, 0.31]), angles
    ):
        assert puw.get_unit(observed) == puw.unit("nm")
        assert puw.get_unit(observed_angles) == puw.unit("radians")
        np.testing.assert_allclose(puw.get_value(observed, to_unit="nm"), expected)
        np.testing.assert_allclose(puw.get_value(observed_angles, to_unit="radians"), 0)

    for frame in (1, 3):
        empty, empty_distances, empty_angles = (
            msm.interactions.hbonds.get_luzard_chandler_hbonds(
                _varying_system(), structure_indices=frame, pbc=False
            )
        )
        assert empty.shape == (1, 0, 3)
        assert empty.dtype == np.int64
        assert empty_distances.shape == empty_angles.shape == (1, 0)


def test_luzard_chandler_between_selections_handles_a_donor_free_direction():
    molsys = _varying_system()
    method = msm.interactions.hbonds.get_luzard_chandler_hbonds
    forward = method(molsys, selection=[0], selection_2=[2, 3], pbc=False)
    reverse = method(molsys, selection=[2, 3], selection_2=[0], pbc=False)
    assert [len(frame) for frame in forward[0]] == [1, 0, 2, 0]
    for actual, expected in zip(forward[0], reverse[0]):
        np.testing.assert_array_equal(actual, expected)
    empty = method(molsys, selection=[2], selection_2=[3], pbc=False)
    assert empty[0].shape == (4, 0, 3)
    assert empty[1].shape == empty[2].shape == (4, 0)


def test_luzard_chandler_analysis_records_scope_coverage_angles_and_roles(tmp_path):
    molsys = _varying_system()
    analysis = msm.interactions.hbonds.get_luzard_chandler_hbonds(
        molsys,
        selection=[0, 2],
        structure_indices=[2, 1, 0, 3, 2],
        pbc=False,
        output_type="molsysmt.Interactions",
    )
    assert isinstance(analysis, msm.Interactions)
    assert not molsys.interactions
    assert analysis.n_interactions == 2
    np.testing.assert_array_equal(analysis.evaluated_structure_indices, [2, 1, 0, 3])
    np.testing.assert_array_equal(analysis.evaluation_scope["atom_indices"], [0, 1, 2])
    assert analysis.query(atom_indices=[1]).n_interactions == 2
    assert (
        analysis.query(atom_indices=[0, 2], mode="within_selection").n_interactions == 0
    )
    assert (
        analysis.query(atom_indices=[0, 1, 2], mode="within_selection").n_interactions
        == 2
    )
    for frame in (1, 3):
        assert analysis.query(structure_indices=[frame]).n_interactions == 0
        np.testing.assert_array_equal(
            analysis.query(structure_indices=[frame]).to_dict()[
                "evaluated_structure_indices"
            ],
            [frame],
        )
    assert [part["role"] for part in analysis.relation(0)["participants"]] == [
        "donor",
        "hydrogen",
        "acceptor",
    ]
    assert analysis.measure_units == {"distance": "nm", "angle": "rad"}
    assert analysis.parameters["distance_definition"] == "donor_acceptor"
    assert analysis.parameters["angle_definition"] == "hydrogen_donor_acceptor"
    assert analysis.parameters["angle_comparison"] == "strictly_less_than"
    assert analysis.software == {"molsysmt": msm.__version__}
    assert analysis.to_dict()["image_vectors"] is None
    molsys.interactions = {"luzard_chandler": analysis}
    filename = tmp_path / "angular_observations.h5msm"
    msm.convert(molsys, to_form="file:h5msm", output_filename=filename)
    restored = msm.convert(filename).interactions["luzard_chandler"]
    assert restored.method == "molsysmt.interactions.hbonds.get_luzard_chandler_hbonds"
    assert restored.parameters == analysis.parameters
    assert restored.software == analysis.software
    np.testing.assert_array_equal(
        restored.query(structure_indices=[2, 1, 0, 3]).to_dict()[
            "evaluated_structure_indices"
        ],
        [2, 1, 0, 3],
    )
    np.testing.assert_array_equal(
        restored.measurements["angle"], analysis.measurements["angle"]
    )


@pytest.mark.parametrize("identical", [False, True])
def test_luzard_chandler_sparse_two_selection_scope_and_deduplication(identical):
    kwargs = (
        {"selection_2": "all"}
        if identical
        else {"selection": [0], "selection_2": [2, 3]}
    )
    analysis = msm.interactions.hbonds.get_luzard_chandler_hbonds(
        _varying_system(), pbc=False, output_type="molsysmt.Interactions", **kwargs
    )
    assert analysis.n_interactions == 3
    assert analysis.evaluation_scope["mode"] == ("internal" if identical else "between")
    if not identical:
        assert analysis.between_selections([0], [2, 3]).n_interactions == 3
        np.testing.assert_array_equal(analysis.evaluation_scope["atom_indices"], [0, 1])
        np.testing.assert_array_equal(
            analysis.evaluation_scope["atom_indices_b"], [2, 3]
        )


def _periodic_system(box):
    builder = msm.MolSysBuilder()
    donor = builder.add_atom(atom_name="N", atom_type="N")
    hydrogen = builder.add_atom(atom_name="H", atom_type="H")
    acceptor = builder.add_atom(atom_name="O", atom_type="O")
    builder.add_group([donor, hydrogen], group_name="ALA")
    builder.add_group([acceptor], group_name="ALA")
    builder.add_bond(donor, hydrogen)
    direction = box[0] / np.linalg.norm(box[0])
    transverse = np.cross([0, 0, 1], direction)
    angle = np.deg2rad(20)
    donor_position = 0.95 * box[0]
    coordinates = np.asarray(
        [
            donor_position,
            donor_position + 0.1 * direction - box[0],
            donor_position
            + 0.3 * (np.cos(angle) * direction + np.sin(angle) * transverse)
            - 2 * box[0],
        ]
    )
    builder.set_coordinates(puw.quantity(coordinates, "nm"))
    builder.set_box(puw.quantity(box, "nm"))
    return builder.build(), coordinates


@pytest.mark.parametrize(
    "box",
    [
        np.eye(3),
        np.asarray([[1, 0, 0], [0.48, 1, 0], [0.45, 0.43, 1]]),
        np.asarray([[2**-0.5, 2**-0.5, 0], [-(2**-0.5), 2**-0.5, 0], [0, 0, 1]]),
    ],
)
def test_luzard_chandler_periodic_images_reconstruct_distance_and_angle(box, tmp_path):
    molsys, coordinates = _periodic_system(box)
    analysis = msm.interactions.hbonds.get_luzard_chandler_hbonds(
        molsys, output_type="molsysmt.Interactions"
    )
    assert analysis.n_interactions == 1
    observed = analysis.to_dict()
    np.testing.assert_array_equal(
        observed["image_vectors"], [[0, 0, 0], [1, 0, 0], [2, 0, 0]]
    )
    unwrapped = coordinates + observed["image_vectors"] @ box
    dh = unwrapped[1] - unwrapped[0]
    da = unwrapped[2] - unwrapped[0]
    angle = np.arctan2(np.linalg.norm(np.cross(dh, da)), np.dot(dh, da))
    np.testing.assert_allclose(
        observed["measurements"]["distance"], [np.linalg.norm(da)]
    )
    np.testing.assert_allclose(observed["measurements"]["angle"], [angle])
    np.testing.assert_allclose(angle, np.deg2rad(20))
    assert observed["measure_units"] == {"distance": "nm", "angle": "rad"}
    molsys.interactions = {"angular": analysis}
    filename = tmp_path / "periodic.h5msm"
    msm.convert(molsys, to_form="file:h5msm", output_filename=filename)
    recovered = msm.convert(filename).interactions["angular"].to_dict()
    np.testing.assert_array_equal(recovered["image_vectors"], observed["image_vectors"])
    np.testing.assert_array_equal(
        recovered["measurements"]["angle"], observed["measurements"]["angle"]
    )


def test_luzard_chandler_rejects_inconsistent_periodic_angular_evidence(monkeypatch):
    molsys, _ = _periodic_system(np.eye(3))
    from molsysmt._private.rust_backend import get_mic_pair_observations

    calls = 0

    def wrong_hydrogen_image(first, second, boxes, frames):
        nonlocal calls
        distances, images = get_mic_pair_observations(first, second, boxes, frames)
        calls += 1
        if calls == 1:
            images[:, 1] = 1
        return distances, images

    monkeypatch.setattr(
        "molsysmt._private.rust_backend.get_mic_pair_observations", wrong_hydrogen_image
    )
    with pytest.raises(InternalAlgorithmError):
        msm.interactions.hbonds.get_luzard_chandler_hbonds(
            molsys, output_type="molsysmt.Interactions"
        )


def test_luzard_chandler_images_preserve_the_angle_kernel_half_box_tie():
    molsys, _ = _periodic_system(np.eye(3))
    molsys.structures.coordinates = puw.quantity(
        [[[0, 0, 0], [0.5, 0, 0], [-0.3, 0, 0]]], "nm"
    )
    analysis = msm.interactions.hbonds.get_luzard_chandler_hbonds(
        molsys, output_type="molsysmt.Interactions"
    )
    assert analysis.n_interactions == 1
    np.testing.assert_array_equal(
        analysis.to_dict()["image_vectors"], [[0, 0, 0], [-1, 0, 0], [0, 0, 0]]
    )
    np.testing.assert_allclose(analysis.measurements["distance"], [0.3])
    np.testing.assert_allclose(analysis.measurements["angle"], [0])


def test_luzard_chandler_units_do_not_follow_a_nondefault_session():
    puw.configure.set_standard_units(
        [
            "angstrom",
            "ps",
            "K",
            "mole",
            "dalton",
            "e",
            "kJ/mol",
            "kJ/(mol*nm)",
            "kJ/(mol*nm**2)",
            "degrees",
        ]
    )
    molsys, _ = _periodic_system(np.eye(3))
    _, distances, angles = msm.interactions.hbonds.get_luzard_chandler_hbonds(molsys)
    assert puw.get_unit(distances) == puw.unit("nm")
    assert puw.get_unit(angles) == puw.unit("radians")
    analysis = msm.interactions.hbonds.get_luzard_chandler_hbonds(
        molsys, output_type="molsysmt.Interactions"
    )
    np.testing.assert_allclose(analysis.measurements["distance"], [0.3])
    np.testing.assert_allclose(analysis.measurements["angle"], [np.deg2rad(20)])


def test_luzard_chandler_rejects_unsupported_sparse_role_and_scope_contracts():
    method = msm.interactions.hbonds.get_luzard_chandler_hbonds
    molsys = _varying_system()
    for kwargs in (
        {"donors": [[0, 1]]},
        {"structure_indices_2": [0]},
        {"selection": [0, 1, 2], "selection_2": [2, 3]},
    ):
        with pytest.raises(NotImplementedMethodError):
            method(molsys, output_type="molsysmt.Interactions", **kwargs)


def test_luzard_chandler_angular_cutoff_is_strict():
    method = msm.interactions.hbonds.get_luzard_chandler_hbonds
    molsys = _varying_system()
    rejected = method(
        molsys, structure_indices=[3], pbc=False, angle_threshold="90 degrees"
    )
    accepted = method(
        molsys, structure_indices=[3], pbc=False, angle_threshold="90.01 degrees"
    )
    assert rejected[0].shape == (1, 0, 3)
    assert accepted[0].tolist() == [[[0, 1, 2]]]
    np.testing.assert_allclose(
        puw.get_value(accepted[2], to_unit="radians"), [[np.pi / 2]]
    )


def test_luzard_chandler_empty_requests_and_role_free_selections_have_defined_shapes():
    method = msm.interactions.hbonds.get_luzard_chandler_hbonds
    molsys = _varying_system()
    empty = method(molsys, structure_indices=[], pbc=False)
    assert empty[0].shape == (0, 0, 3)
    assert empty[1].shape == empty[2].shape == (0, 0)
    analysis = method(molsys, structure_indices=[], output_type="molsysmt.Interactions")
    assert analysis.evaluated_structure_indices.shape == (0,)
    assert analysis.measurements["angle"].shape == (0,)
    role_free = method(
        molsys, selection=[2, 3], pbc=False, output_type="molsysmt.Interactions"
    )
    np.testing.assert_array_equal(role_free.evaluated_structure_indices, [0, 1, 2, 3])
    assert role_free.n_interactions == 0


def test_luzard_chandler_bundled_trajectory_matches_direct_criteria():
    molsys = msm.convert(
        msm.systems["pentalanine"]["traj_pentalanine.h5msm"],
        to_form="molsysmt.MolSys",
        structure_indices=[0, 1, 2, 50, 99],
    )
    atoms, distances, angles = msm.interactions.hbonds.get_luzard_chandler_hbonds(
        molsys, pbc=False
    )
    coordinates = puw.get_value(msm.get(molsys, coordinates=True), to_unit="nm")
    donors = msm.interactions.hbonds.get_donor_atoms(molsys)
    acceptors = msm.interactions.hbonds.get_acceptor_atoms(molsys)
    for frame, triples, observed_distances, observed_angles in zip(
        coordinates, atoms, distances, angles
    ):
        expected = {}
        for donor, hydrogen in donors:
            dh = frame[hydrogen] - frame[donor]
            for acceptor in acceptors:
                da = frame[acceptor] - frame[donor]
                distance = np.linalg.norm(da)
                if donor == acceptor or distance > 0.35:
                    continue
                angle = np.arctan2(np.linalg.norm(np.cross(dh, da)), np.dot(dh, da))
                if angle < np.deg2rad(30):
                    expected[(int(donor), int(hydrogen), int(acceptor))] = (
                        distance,
                        angle,
                    )
        actual = dict(
            zip(
                map(tuple, triples),
                zip(
                    puw.get_value(observed_distances, to_unit="nm"),
                    puw.get_value(observed_angles, to_unit="radians"),
                ),
            )
        )
        assert actual.keys() == expected.keys()
        for triple in expected:
            np.testing.assert_allclose(actual[triple], expected[triple], atol=1e-7)
