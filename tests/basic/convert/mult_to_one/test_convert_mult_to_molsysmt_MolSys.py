"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed

import numpy as np

import molsysmt as msm
from molsysmt import systems


def test_convert_file_prmtop_and_file_inpcrd_to_molsysmt_MolSys():
    prmtop_file = systems["pentalanine"]["pentalanine.prmtop"]
    inpcrd_file = systems["pentalanine"]["pentalanine.inpcrd"]
    molsys = msm.convert([prmtop_file, inpcrd_file], to_form="molsysmt.MolSys")
    form = msm.get_form(molsys)
    n_atoms, n_structures, box = msm.get(
        molsys, n_atoms=True, n_structures=True, box=True
    )
    n_atoms_prmtop = msm.get(prmtop_file, n_atoms=True)
    n_structures_inpcrd, box_inpcrd = msm.get(inpcrd_file, n_structures=True, box=True)
    assert "molsysmt.MolSys" == form
    assert n_atoms == n_atoms_prmtop
    assert n_structures == n_structures_inpcrd
    assert np.allclose(box, box_inpcrd)


def test_convert_file_psf_and_file_dcd_to_molsysmt_MolSys():
    psf_file = systems["POPC membrane"]["popc_membrane.psf"]
    dcd_file = systems["POPC membrane"]["popc_membrane.dcd"]
    molsys = msm.convert([psf_file, dcd_file], to_form="molsysmt.MolSys")
    form = msm.get_form(molsys)
    n_atoms, n_structures = msm.get(molsys, n_atoms=True, n_structures=True)
    assert "molsysmt.MolSys" == form
    assert n_atoms == 78974
    assert n_structures == 5


def test_convert_file_gro_and_file_xtc_to_molsysmt_MolSys():
    molsys_1 = systems["nglview"]["md_1u19.gro"]
    molsys_2 = systems["nglview"]["md_1u19.xtc"]
    molsys = msm.convert([molsys_1, molsys_2], to_form="molsysmt.MolSys")
    form = msm.get_form(molsys)
    assert "molsysmt.MolSys" == form


def test_convert_single_state_topology_and_trajectory_reconciles_structure_association():
    topology = systems["chicken villin HP35"]["traj_chicken_villin_HP35_solvated.h5msm"]
    trajectory = systems["chicken villin HP35"]["traj_chicken_villin_HP35_solvated.dcd"]

    molsys = msm.convert([topology, trajectory], to_form="molsysmt.MolSys")

    assert molsys.structures.n_structures == 20
    assert molsys._structure_chemical_state_indices is None
    np.testing.assert_array_equal(
        molsys._get_structure_chemical_state_indices(),
        np.zeros(20, dtype=np.int64),
    )


def test_selected_trajectory_positions_never_index_the_reference_only_provider():
    reference = systems["chicken villin HP35"][
        "traj_chicken_villin_HP35_solvated.h5msm"
    ]
    trajectory = systems["chicken villin HP35"]["traj_chicken_villin_HP35_solvated.dcd"]
    positions = [11, 2, 11]
    expected = msm.pyunitwizard.get_value(
        msm.get(trajectory, structure_indices=positions, coordinates=True), to_unit="nm"
    )
    for items in ([reference, trajectory], [trajectory, reference]):
        output = msm.convert(
            items, structure_indices=positions, to_form="molsysmt.MolSys"
        )
        assert output.structures.n_structures == 3
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(output.structures.coordinates, to_unit="nm"),
            expected,
        )
        assert output.structures.time is None and output.structures.structure_id is None
        np.testing.assert_array_equal(
            output._get_structure_chemical_state_indices(), [0, 0, 0]
        )


def test_query_precedence_uses_the_last_eligible_on_axis_provider():
    from molsysmt.native import Structures

    puw = msm.pyunitwizard
    first = Structures(coordinates=puw.quantity(np.ones((2, 1, 3)), "nm"))
    second = Structures(coordinates=puw.quantity(np.full((2, 1, 3), 4.0), "nm"))
    for providers, expected in (([first, second], 4.0), ([second, first], 1.0)):
        owner, form = msm.where_is_attribute(providers, "coordinates")
        assert owner is providers[-1] and form == "molsysmt.Structures"
        np.testing.assert_array_equal(
            puw.get_value(msm.get(providers, coordinates=True), to_unit="nm"),
            np.full((2, 1, 3), expected),
        )


def test_off_axis_state_links_are_unknown_even_when_selected_counts_match():
    import pandas as pd

    from molsysmt.native import MolSys, Structures

    puw = msm.pyunitwizard
    reference = MolSys(n_atoms=2)
    reference.structures = Structures(
        coordinates=puw.quantity(np.zeros((1, 2, 3)), "nm")
    )
    reference.chemical_states.append_state()
    msm.set(reference, structure_chemical_state_index=[0])
    trajectory = Structures(coordinates=puw.quantity(np.ones((3, 2, 3)), "nm"))
    for providers in ([reference, trajectory], [trajectory, reference]):
        for positions in ([2], [2, 0, 2]):
            output = msm.convert(providers, structure_indices=positions)
            assert output.chemical_states.n_chemical_states == 2
            links = output._get_structure_chemical_state_indices()
            assert len(links) == len(positions) and pd.isna(links).all()
            np.testing.assert_array_equal(
                puw.get_value(output.structures.coordinates, to_unit="nm"),
                np.ones((len(positions), 2, 3)),
            )
    assert reference.structures.n_structures == 1
    np.testing.assert_array_equal(
        reference._get_structure_chemical_state_indices(), [0]
    )


def test_off_axis_analyses_require_explicit_structure_correspondence():
    import pytest

    from molsysmt._private.smonitor import StructuralInconsistencyError
    from molsysmt.native import MolSys, Structures

    puw = msm.pyunitwizard
    reference = MolSys(n_atoms=2)
    reference.structures = Structures(
        coordinates=puw.quantity(np.zeros((1, 2, 3)), "nm")
    )
    analysis = msm.Interactions.from_records(
        [],
        n_atoms=2,
        n_structures=1,
        evaluated_structure_indices=[0],
        method="synthetic.off-axis-reference",
    )
    reference.interactions = {"reference": analysis}
    trajectory = Structures(coordinates=puw.quantity(np.ones((3, 2, 3)), "nm"))
    for providers in ([reference, trajectory], [trajectory, reference]):
        for positions in ([2], [2, 0, 2]):
            with pytest.raises(
                StructuralInconsistencyError, match="reference interaction analyses"
            ):
                msm.convert(providers, structure_indices=positions)
    assert reference.interactions["reference"] is analysis
    np.testing.assert_array_equal(analysis.evaluated_structure_indices, [0])
    assert reference.structures.n_structures == 1
