"""
Contract and parity tests for molsysmt.StructuresDict form.

Oracle: builder_pdb_molsys (4 atoms, 1 frame).
Parity means that Structures → StructuresDict → Structures round-trip
preserves n_atoms, n_structures, and all coordinate values.
"""

import pytest
import numpy as np
import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import Structures


@pytest.fixture()
def source_structures(builder_pdb_molsys):
    return builder_pdb_molsys.structures


@pytest.fixture()
def structures_dict(source_structures):
    return msm.convert(source_structures, to_form='molsysmt.StructuresDict')


@pytest.fixture()
def rebuilt_structures(structures_dict):
    return msm.convert(structures_dict, to_form='molsysmt.Structures')


@pytest.fixture()
def thermodynamic_structures():
    return Structures(
        coordinates=puw.quantity(np.arange(18).reshape(3, 2, 3), 'nm'),
        temperature=puw.quantity([290000.0, 300000.0, 310000.0], 'mK'),
        potential_energy=puw.quantity([-1.0, -2.0, -3.0], 'kcal/mol'),
        kinetic_energy=puw.quantity([0.1, 0.2, 0.3], 'kcal/mol'),
        skip_digestion=True,
    )


# ---------------------------------------------------------------------------
# Contract: molsysmt.StructuresDict can be created and queried
# ---------------------------------------------------------------------------

def test_structures_dict_is_dict(structures_dict):
    assert isinstance(structures_dict, dict)


def test_structures_dict_n_atoms(structures_dict):
    assert msm.get(structures_dict, element='system', n_atoms=True) == 4


def test_structures_dict_atom_indices(structures_dict):
    assert msm.get(structures_dict, element='atom', atom_index=True) == [0, 1, 2, 3]
    assert msm.get(
        structures_dict,
        element='atom',
        selection=[3, 1],
        atom_index=True,
    ) == [3, 1]


def test_structures_dict_n_structures(structures_dict):
    assert msm.get(structures_dict, element='system', n_structures=True) == 1


def test_structures_dict_optional_atom_fields(structures_dict):
    structures_dict['occupancy'] = np.array([[1.0, 0.8, 0.6, 0.4]])
    structures_dict['alternate_location'] = [
        {
            1: {'location_id': np.array(['A', 'B'])},
            3: {'location_id': np.array(['A', 'B'])},
        }
    ]

    occupancy = msm.get(
        structures_dict,
        element='atom',
        selection=[1, 3],
        occupancy=True,
    )
    alternate_location = msm.get(
        structures_dict,
        element='atom',
        selection=[1],
        alternate_location=True,
    )

    assert np.allclose(occupancy, [[0.8, 0.4]])
    assert list(alternate_location[0]) == ['1']


def test_structures_dict_thermodynamic_series_are_queryable(
    thermodynamic_structures,
):
    structures_dict, report = msm.convert(
        thermodynamic_structures,
        to_form='molsysmt.StructuresDict',
        return_report=True,
    )

    assert report.outcome == 'equivalent'
    assert report.audited_scopes == ('all',)
    assert report.is_exhaustive
    for attribute in (
        'temperature',
        'potential_energy',
        'kinetic_energy',
        'total_energy',
    ):
        assert msm.has_attribute(structures_dict, attribute)

    assert np.allclose(
        puw.get_value(msm.get(structures_dict, temperature=True), to_unit='K'),
        [290.0, 300.0, 310.0],
    )
    assert np.allclose(
        puw.get_value(
            msm.get(structures_dict, total_energy=True),
            to_unit='kJ/mol',
        ),
        [-3.7656, -7.5312, -11.2968],
    )


def test_structures_dict_thermodynamic_selection_preserves_requested_order(
    thermodynamic_structures,
):
    structures_dict = msm.convert(
        thermodynamic_structures,
        to_form='molsysmt.StructuresDict',
        structure_indices=[2, 0, 2],
    )
    rebuilt = msm.convert(
        structures_dict,
        to_form='molsysmt.Structures',
        structure_indices=[1, 0, 1],
    )

    assert np.allclose(
        puw.get_value(rebuilt.temperature, to_unit='K'),
        [290.0, 310.0, 290.0],
    )
    assert np.allclose(
        puw.get_value(rebuilt.potential_energy, to_unit='kJ/mol'),
        [-4.184, -12.552, -4.184],
    )
    assert np.allclose(
        puw.get_value(rebuilt.kinetic_energy, to_unit='kJ/mol'),
        [0.4184, 1.2552, 0.4184],
    )


def test_structures_dict_does_not_synthesize_absent_thermodynamic_series(
    structures_dict,
):
    for attribute in (
        'temperature',
        'potential_energy',
        'kinetic_energy',
        'total_energy',
    ):
        assert attribute not in structures_dict
        assert not msm.has_attribute(structures_dict, attribute)


def test_structures_dict_to_molsys_keeps_selected_atom_and_structure_axes(
    thermodynamic_structures,
):
    structures_dict = msm.convert(
        thermodynamic_structures,
        to_form='molsysmt.StructuresDict',
    )
    molsys = msm.convert(
        structures_dict,
        to_form='molsysmt.MolSys',
        selection=[1, 0],
        structure_indices=[2, 0, 2],
    )

    assert molsys.topology.n_atoms == 2
    assert molsys.structures.n_atoms == 2
    assert molsys.structures.n_structures == 3
    assert np.allclose(
        puw.get_value(molsys.structures.temperature, to_unit='K'),
        [310.0, 290.0, 310.0],
    )
    assert np.allclose(
        puw.get_value(molsys.structures.coordinates, to_unit='nm'),
        puw.get_value(
            thermodynamic_structures.coordinates[[2, 0, 2]][:, [1, 0], :],
            to_unit='nm',
        ),
    )


def test_structures_dict_to_topology_uses_selected_atom_count(
    thermodynamic_structures,
):
    structures_dict = msm.convert(
        thermodynamic_structures,
        to_form='molsysmt.StructuresDict',
    )
    topology = msm.convert(
        structures_dict,
        to_form='molsysmt.Topology',
        selection=[1, 0],
    )

    assert topology.n_atoms == 2


# ---------------------------------------------------------------------------
# Parity: Structures → StructuresDict → Structures preserves data
# ---------------------------------------------------------------------------

def test_parity_atom_count(rebuilt_structures, source_structures):
    assert rebuilt_structures.n_atoms == source_structures.n_atoms


def test_parity_structure_count(rebuilt_structures, source_structures):
    assert rebuilt_structures.n_structures == source_structures.n_structures


def test_parity_coordinates(rebuilt_structures, source_structures):
    rebuilt_coords = puw.get_value(rebuilt_structures.coordinates, to_unit='nm')
    source_coords = puw.get_value(source_structures.coordinates, to_unit='nm')
    assert np.allclose(rebuilt_coords, source_coords)


def test_parity_thermodynamic_series(thermodynamic_structures):
    structures_dict = msm.convert(
        thermodynamic_structures,
        to_form='molsysmt.StructuresDict',
    )
    rebuilt = msm.convert(
        structures_dict,
        to_form='molsysmt.Structures',
    )

    assert np.allclose(
        puw.get_value(rebuilt.temperature, to_unit='K'),
        [290.0, 300.0, 310.0],
    )
    assert np.allclose(
        puw.get_value(rebuilt.potential_energy, to_unit='kJ/mol'),
        [-4.184, -8.368, -12.552],
    )
    assert np.allclose(
        puw.get_value(rebuilt.kinetic_energy, to_unit='kJ/mol'),
        [0.4184, 0.8368, 1.2552],
    )


def test_roundtrip_preserves_builder_truth(builder_structures, tmp_path):
    structures_dict = msm.convert(builder_structures, to_form='molsysmt.StructuresDict')
    rebuilt = msm.convert(structures_dict, to_form='molsysmt.Structures')

    assert rebuilt.n_atoms == 4
    assert rebuilt.n_structures == 1
    rebuilt_coords = puw.get_value(rebuilt.coordinates, to_unit='nm')
    source_coords = puw.get_value(builder_structures.coordinates, to_unit='nm')
    assert np.allclose(rebuilt_coords, source_coords)
