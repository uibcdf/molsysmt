"""Disulfide candidates are frame observations, not topology bond records."""

import numpy as np

import molsysmt as msm
from molsysmt import pyunitwizard as puw


def _two_frame_sulfur_system(with_bond=False):
    builder = msm.MolSysBuilder()
    first = builder.add_atom(atom_name="SG", atom_type="S")
    second = builder.add_atom(atom_name="SG", atom_type="S")
    other = builder.add_atom(atom_name="SD", atom_type="S")
    builder.add_group([first], group_name="CYS")
    builder.add_group([second], group_name="CYS")
    builder.add_group([other], group_name="MET")
    if with_bond:
        builder.add_bond(first, second)
    builder.set_coordinates(
        puw.quantity(
            np.array(
                [
                    [[0.0, 0.0, 0.0], [0.20, 0.0, 0.0], [0.10, 0.0, 0.0]],
                    [[0.0, 0.0, 0.0], [0.35, 0.0, 0.0], [0.10, 0.0, 0.0]],
                ]
            ),
            "nanometers",
        )
    )
    return builder.build()


def test_disulfide_candidates_are_aligned_with_requested_structures():
    molsys = _two_frame_sulfur_system()

    pairs, distances = msm.interactions.disulfides.get_disulfide_candidates(
        molsys, structure_indices=[1, 0], pbc=False
    )

    assert [value.shape for value in pairs] == [(0, 2), (1, 2)]
    assert pairs[1].tolist() == [[0, 1]]
    assert [puw.get_value(value, to_unit="nanometers").shape for value in distances] == [
        (0,),
        (1,),
    ]
    assert np.allclose(puw.get_value(distances[1], to_unit="nanometers"), [0.20])


def test_disulfide_candidates_remain_candidates_when_bond_is_recorded():
    molsys = _two_frame_sulfur_system(with_bond=True)

    pairs, _ = msm.interactions.disulfides.get_disulfide_candidates(
        molsys, structure_indices=0, pbc=False
    )

    assert pairs[0].tolist() == [[0, 1]]
    assert msm.build.get_disulfide_bonds(molsys, structure_index=0, pbc=False) == [[0, 1]]


def test_disulfide_candidates_respect_group_filter_and_selection():
    molsys = _two_frame_sulfur_system()

    excluded, _ = msm.interactions.disulfides.get_disulfide_candidates(
        molsys, selection=[0, 2], structure_indices=0, pbc=False
    )
    included, _ = msm.interactions.disulfides.get_disulfide_candidates(
        molsys, group_names=["CYS", "MET"], structure_indices=0, pbc=False
    )

    assert excluded[0].shape == (0, 2)
    assert included[0].shape == (3, 2)


def test_disulfide_candidates_apply_periodic_boundary_conditions(tmp_path):
    builder = msm.MolSysBuilder()
    first = builder.add_atom(atom_name="SG", atom_type="S")
    second = builder.add_atom(atom_name="SG", atom_type="S")
    builder.add_group([first], group_name="CYS")
    builder.add_group([second], group_name="CYS")
    builder.set_coordinates(
        puw.quantity([[0.95, 0.0, 0.0], [0.05, 0.0, 0.0]], "nanometers")
    )
    builder.set_box(puw.quantity(np.eye(3), "nanometers"))
    molsys = builder.build()

    without_pbc, _ = msm.interactions.disulfides.get_disulfide_candidates(
        molsys, pbc=False
    )
    with_pbc, distances = msm.interactions.disulfides.get_disulfide_candidates(
        molsys, pbc=True
    )

    assert without_pbc[0].shape == (0, 2)
    assert with_pbc[0].tolist() == [[0, 1]]
    assert np.allclose(puw.get_value(distances[0], to_unit="nanometers"), [0.10])

    analysis = msm.interactions.disulfides.get_disulfide_candidates(
        molsys, pbc=True, output_type="molsysmt.Interactions"
    )
    assert isinstance(analysis, msm.Interactions)
    observation = analysis.query(structure_indices=[0]).to_dict()
    assert observation["structure_indices"].tolist() == [0]
    assert observation["measure_units"] == {"distance": "nm"}
    np.testing.assert_allclose(observation["measurements"]["distance"], [0.10])
    np.testing.assert_array_equal(observation["image_vectors"], [[0, 0, 0], [1, 0, 0]])
    assert observation["evidence"].tolist() == ["geometric_proximity"]

    molsys.interactions = {"disulfide_candidates": analysis}
    filename = tmp_path / "disulfide_candidates.h5msm"
    msm.h5msm.write(molsys, str(filename))
    restored = msm.h5msm.read(str(filename)).interactions["disulfide_candidates"]
    np.testing.assert_array_equal(restored.to_dict()["image_vectors"],
                                  observation["image_vectors"])
    assert restored.method == analysis.method


def test_disulfide_analysis_preserves_empty_coverage_and_actual_atom_scope():
    molsys = _two_frame_sulfur_system()
    analysis = msm.interactions.disulfides.get_disulfide_candidates(
        molsys, selection=[0, 1], structure_indices=[1, 0, 1], pbc=False,
        output_type="molsysmt.Interactions",
    )

    assert isinstance(analysis, msm.Interactions)
    np.testing.assert_array_equal(analysis.evaluated_structure_indices, [1, 0])
    np.testing.assert_array_equal(analysis.evaluation_scope["atom_indices"], [0, 1])
    assert analysis.query(structure_indices=[1]).n_interactions == 0
    observed = analysis.query(structure_indices=[0]).to_dict()
    assert observed["structure_indices"].tolist() == [0]
    assert observed["image_vectors"] is None
    assert analysis.method == "molsysmt.interactions.disulfides.get_disulfide_candidates"
    assert np.isclose(analysis.parameters["max_bond_length_nm"], 0.205)
    assert analysis.parameters["group_names"] == ["CYS"]

    repeated = msm.interactions.disulfides.get_disulfide_candidates(
        molsys, structure_indices=[0, 0], pbc=False,
        output_type="molsysmt.Interactions",
    )
    assert repeated.n_interactions == 1


def test_disulfide_analysis_uses_rotated_box_image():
    builder = msm.MolSysBuilder()
    for _ in range(2):
        atom = builder.add_atom(atom_name="SG", atom_type="S")
        builder.add_group([atom], group_name="CYS")
    diagonal = 2**-0.5
    builder.set_coordinates(
        puw.quantity([[0.0, 0.0, 0.0], [diagonal + 0.10, diagonal, 0.0]],
                     "nanometers")
    )
    builder.set_box(puw.quantity(
        [[diagonal, diagonal, 0.0], [-diagonal, diagonal, 0.0], [0.0, 0.0, 1.0]],
        "nanometers",
    ))
    analysis = msm.interactions.disulfides.get_disulfide_candidates(
        builder.build(), output_type="molsysmt.Interactions"
    )

    observed = analysis.to_dict()
    assert observed["structure_indices"].tolist() == [0]
    np.testing.assert_allclose(observed["measurements"]["distance"], [0.10])
    np.testing.assert_array_equal(observed["image_vectors"], [[0, 0, 0], [-1, 0, 0]])
