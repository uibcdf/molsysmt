"""Check empty, varying, selected, and periodic Buch observations."""

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
            ],
            "nanometers",
        )
    )
    return builder.build()


def test_buch_returns_aligned_variable_counts_and_empty_frames():
    atoms, distances = msm.interactions.hbonds.get_buch_hbonds(
        _varying_system(),
        structure_indices=[2, 1, 0, 2],
        pbc=False,
    )
    assert isinstance(atoms, list)
    assert isinstance(distances, list)
    assert [frame.shape for frame in atoms] == [(2, 3), (0, 3), (1, 3), (2, 3)]
    assert [frame.shape for frame in distances] == [(2,), (0,), (1,), (2,)]
    assert atoms[0].tolist() == [[0, 1, 2], [0, 1, 3]]
    assert atoms[2].tolist() == [[0, 1, 2]]
    for frame, expected in zip(distances, ([0.2, 0.21], [], [0.2], [0.2, 0.21])):
        np.testing.assert_allclose(puw.get_value(frame, to_unit="nanometers"), expected)

    empty, empty_distances = msm.interactions.hbonds.get_buch_hbonds(
        _varying_system(),
        structure_indices=[1],
        pbc=False,
    )
    assert empty.shape == (1, 0, 3)
    assert empty.dtype == np.int64
    assert empty_distances.shape == (1, 0)


def test_buch_between_selections_preserves_variable_counts_with_one_donor_side():
    molsys = _varying_system()
    atoms, distances = msm.interactions.hbonds.get_buch_hbonds(
        molsys,
        selection=[0, 1],
        selection_2=[2, 3],
        structure_indices=[2, 1, 0],
        pbc=False,
    )
    assert [len(frame) for frame in atoms] == [2, 0, 1]
    assert [len(frame) for frame in distances] == [2, 0, 1]
    # The reverse search has no donors in its first selection.
    reversed_atoms, _ = msm.interactions.hbonds.get_buch_hbonds(
        molsys,
        selection=[2, 3],
        selection_2=[0, 1],
        structure_indices=[2, 1, 0],
        pbc=False,
    )
    for forward, reverse in zip(atoms, reversed_atoms):
        np.testing.assert_array_equal(forward, reverse)


def test_buch_analysis_keeps_coverage_roles_and_actual_participant_universe(tmp_path):
    molsys = _varying_system()
    analysis = msm.interactions.hbonds.get_buch_hbonds(
        molsys,
        selection=[0, 2],
        structure_indices=[2, 1, 0, 2],
        pbc=False,
        output_type="molsysmt.Interactions",
    )
    assert isinstance(analysis, msm.Interactions)
    assert analysis.n_interactions == 2
    np.testing.assert_array_equal(analysis.evaluated_structure_indices, [2, 1, 0])
    np.testing.assert_array_equal(analysis.evaluation_scope["atom_indices"], [0, 1, 2])
    assert analysis.query(structure_indices=[1]).n_interactions == 0
    assert analysis.query(atom_indices=[1]).n_interactions == 2
    assert analysis.query(atom_indices=[0, 2], mode="internal").n_interactions == 0
    assert analysis.query(atom_indices=[0, 1, 2], mode="internal").n_interactions == 2
    assert [part["role"] for part in analysis.relation(0)["participants"]] == [
        "donor",
        "hydrogen",
        "acceptor",
    ]
    assert analysis.parameters["distance_definition"] == "hydrogen_acceptor"
    assert analysis.to_dict()["image_vectors"] is None

    molsys.interactions = {"buch": analysis}
    filename = tmp_path / "buch.h5msm"
    msm.h5msm.write(molsys, str(filename))
    restored = msm.h5msm.read(str(filename)).interactions["buch"]
    assert restored.method == "molsysmt.interactions.hbonds.get_buch_hbonds"
    assert restored.parameters == analysis.parameters
    np.testing.assert_array_equal(restored.evaluated_structure_indices, [2, 1, 0])


def test_buch_analysis_declares_both_directions_between_disjoint_selections():
    analysis = msm.interactions.hbonds.get_buch_hbonds(
        _varying_system(),
        selection=[0],
        selection_2=[2, 3],
        structure_indices=[2, 1, 0],
        pbc=False,
        output_type="molsysmt.Interactions",
    )
    assert analysis.evaluation_scope["mode"] == "between"
    np.testing.assert_array_equal(analysis.evaluation_scope["atom_indices"], [0, 1])
    np.testing.assert_array_equal(analysis.evaluation_scope["atom_indices_b"], [2, 3])
    assert analysis.n_interactions == 3
    assert analysis.between([0], [2, 3]).n_interactions == 3


def test_buch_analysis_identical_selections_do_not_duplicate_observations():
    analysis = msm.interactions.hbonds.get_buch_hbonds(
        _varying_system(),
        selection_2="all",
        pbc=False,
        output_type="molsysmt.Interactions",
    )
    assert analysis.evaluation_scope["mode"] == "internal"
    assert analysis.n_interactions == 3


@pytest.mark.parametrize(
    "box",
    [
        np.eye(3),
        np.asarray([[1, 0, 0], [0.48, 1, 0], [0.45, 0.43, 1]]),
        np.asarray([[2**-0.5, 2**-0.5, 0], [-(2**-0.5), 2**-0.5, 0], [0, 0, 1]]),
    ],
)
@pytest.mark.parametrize("acceptor_position", [0.25, -0.75])
def test_buch_periodic_images_preserve_donor_hydrogen_acceptor_chain(
    box, acceptor_position
):
    builder = msm.MolSysBuilder()
    donor = builder.add_atom(atom_name="N", atom_type="N")
    hydrogen = builder.add_atom(atom_name="H", atom_type="H")
    acceptor = builder.add_atom(atom_name="O", atom_type="O")
    builder.add_group([donor, hydrogen], group_name="ALA")
    builder.add_group([acceptor], group_name="ALA")
    builder.add_bond(donor, hydrogen)
    coordinates = (
        np.asarray([[0.95, 0, 0], [0.05, 0, 0], [acceptor_position, 0, 0]]) @ box
    )
    builder.set_coordinates(puw.quantity(coordinates, "nanometers"))
    builder.set_box(puw.quantity(box, "nanometers"))
    analysis = msm.interactions.hbonds.get_buch_hbonds(
        builder.build(),
        output_type="molsysmt.Interactions",
    )
    observed = analysis.to_dict()
    assert analysis.n_interactions == 1
    assert observed["measure_units"] == {"distance": "nm"}
    np.testing.assert_allclose(observed["measurements"]["distance"], [0.2])
    acceptor_image = 1 if acceptor_position > 0 else 2
    np.testing.assert_array_equal(
        observed["image_vectors"], [[0, 0, 0], [1, 0, 0], [acceptor_image, 0, 0]]
    )
    observed_coordinates = coordinates + observed["image_vectors"] @ box
    np.testing.assert_allclose(
        np.linalg.norm(observed_coordinates[1] - observed_coordinates[0]), 0.1
    )
    np.testing.assert_allclose(
        np.linalg.norm(observed_coordinates[2] - observed_coordinates[1]), 0.2
    )


def test_buch_analysis_rejects_unsupported_role_and_scope_contracts():
    molsys = _varying_system()
    with pytest.raises(NotImplementedMethodError):
        msm.interactions.hbonds.get_buch_hbonds(
            molsys,
            donors=[[0, 1]],
            output_type="molsysmt.Interactions",
        )
    with pytest.raises(NotImplementedMethodError):
        msm.interactions.hbonds.get_buch_hbonds(
            molsys,
            selection=[0, 1, 2],
            selection_2=[2, 3],
            output_type="molsysmt.Interactions",
        )


def test_buch_distance_units_are_explicit_under_a_nondefault_session():
    molsys = _varying_system()
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
            "radians",
        ]
    )
    _, distances = msm.interactions.hbonds.get_buch_hbonds(molsys, pbc=False)
    assert all(puw.get_unit(frame) == puw.unit("nanometers") for frame in distances)
    np.testing.assert_allclose(puw.get_value(distances[0], to_unit="nanometers"), [0.2])
    analysis = msm.interactions.hbonds.get_buch_hbonds(
        molsys,
        pbc=False,
        output_type="molsysmt.Interactions",
    )
    assert analysis.to_dict()["measure_units"] == {"distance": "nm"}
    np.testing.assert_allclose(
        analysis.to_dict()["measurements"]["distance"], [0.2, 0.2, 0.21]
    )


def test_buch_bundled_trajectory_matches_direct_distance_criterion():
    molsys = msm.convert(
        msm.systems["pentalanine"]["traj_pentalanine.h5msm"],
        to_form="molsysmt.MolSys",
        structure_indices=[0, 1, 2, 50, 99],
    )
    atoms, distances = msm.interactions.hbonds.get_buch_hbonds(molsys, pbc=False)
    coordinates = puw.get_value(msm.get(molsys, coordinates=True), to_unit="nanometers")
    donors = msm.interactions.hbonds.get_donor_atoms(molsys)
    acceptors = msm.interactions.hbonds.get_acceptor_atoms(molsys)
    assert len(donors) and len(acceptors)
    assert len(atoms[0]) == len(atoms[1]) == 0
    assert any(len(frame) for frame in atoms)
    for frame, triples, observed in zip(coordinates, atoms, distances):
        expected = {}
        for donor, hydrogen in donors:
            for acceptor in acceptors:
                distance = np.linalg.norm(frame[hydrogen] - frame[acceptor])
                if donor != acceptor and distance <= 0.23:
                    expected[(int(donor), int(hydrogen), int(acceptor))] = distance
        actual = dict(
            zip(map(tuple, triples), puw.get_value(observed, to_unit="nanometers"))
        )
        assert actual.keys() == expected.keys()
        for triple in expected:
            np.testing.assert_allclose(actual[triple], expected[triple], atol=1e-12)


def test_buch_analysis_does_not_publish_inconsistent_periodic_evidence(monkeypatch):
    molsys = _varying_system()
    molsys.structures.box = puw.quantity(
        np.repeat(np.eye(3)[None], 3, axis=0), "nanometers"
    )

    def inconsistent_images(first, second, boxes, frames):
        return np.zeros(len(first)), np.zeros((len(first), 3), dtype=np.int32)

    monkeypatch.setattr(
        "molsysmt._private.rust_backend.get_mic_pair_observations", inconsistent_images
    )
    with pytest.raises(InternalAlgorithmError):
        msm.interactions.hbonds.get_buch_hbonds(
            molsys,
            pbc=True,
            output_type="molsysmt.Interactions",
        )
