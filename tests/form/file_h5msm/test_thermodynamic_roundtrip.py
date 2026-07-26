"""Testing H5MSM velocity and thermodynamic-series round trips."""

import numpy as np

import molsysmt as msm
from molsysmt.native import Structures


def test_dump_structures_updates_an_existing_h5msm_path(tmp_path):
    from molsysmt.form.molsysmt_Structures.to_file_h5msm import (
        dump_structures_to_h5msm,
    )
    from molsysmt.native import H5MSMFileHandler

    output = tmp_path / 'existing.h5msm'
    H5MSMFileHandler(output, io_mode='w').close()
    structures = Structures(
        coordinates=msm.pyunitwizard.quantity(
            np.zeros((1, 2, 3)), 'nanometer'
        ),
        skip_digestion=True,
    )

    dump_structures_to_h5msm(structures, output)

    restored = msm.convert(output, to_form='molsysmt.Structures')
    assert restored.coordinates.shape == (1, 2, 3)


def test_h5msm_preserves_noncanonical_input_units(tmp_path):
    puw = msm.pyunitwizard
    structures = Structures(
        coordinates=puw.quantity(np.zeros((2, 2, 3)), 'angstrom'),
        velocities=puw.quantity(np.ones((2, 2, 3)), 'angstrom/ps'),
        temperature=puw.quantity(np.array([290000.0, 310000.0]), 'mK'),
        potential_energy=puw.quantity(np.array([-1.0, -2.0]), 'kcal/mol'),
        kinetic_energy=puw.quantity(np.array([0.25, 0.5]), 'kcal/mol'),
        skip_digestion=True,
    )
    output = tmp_path / 'thermodynamics.h5msm'

    msm.convert(structures, to_form='file:h5msm', output_filename=output)

    assert msm.has_attribute(output, 'velocities')
    assert msm.has_attribute(output, 'temperature')
    assert msm.has_attribute(output, 'potential_energy')
    assert msm.has_attribute(output, 'kinetic_energy')
    assert msm.has_attribute(output, 'total_energy')
    np.testing.assert_allclose(
        puw.get_value(msm.get(output, velocities=True), to_unit='nm/ps'),
        0.1,
    )
    np.testing.assert_allclose(
        puw.get_value(msm.get(output, temperature=True), to_unit='K'),
        [290.0, 310.0],
    )
    np.testing.assert_allclose(
        puw.get_value(msm.get(output, potential_energy=True), to_unit='kJ/mol'),
        [-4.184, -8.368],
    )
    np.testing.assert_allclose(
        puw.get_value(msm.get(output, kinetic_energy=True), to_unit='kJ/mol'),
        [1.046, 2.092],
    )
    np.testing.assert_allclose(
        puw.get_value(msm.get(output, total_energy=True), to_unit='kJ/mol'),
        [-3.138, -6.276],
    )

    restored, report = msm.convert(
        output,
        to_form='molsysmt.Structures',
        return_report=True,
    )
    assert report.outcome == 'equivalent'
    assert report.audited_scopes == ('all',)
    assert report.is_exhaustive is True
    np.testing.assert_allclose(
        puw.get_value(restored.velocities, to_unit='nm/ps'),
        0.1,
    )
    np.testing.assert_allclose(
        puw.get_value(restored.temperature, to_unit='K'),
        [290.0, 310.0],
    )
    np.testing.assert_allclose(
        puw.get_value(restored.potential_energy, to_unit='kJ/mol'),
        [-4.184, -8.368],
    )
    np.testing.assert_allclose(
        puw.get_value(restored.kinetic_energy, to_unit='kJ/mol'),
        [1.046, 2.092],
    )

def test_empty_h5msm_optional_series_are_not_reported_as_present():
    file_traj = msm.systems['pentalanine']['traj_pentalanine.h5msm']
    for attribute in (
        'velocities',
        'temperature',
        'potential_energy',
        'kinetic_energy',
        'total_energy',
    ):
        assert not msm.has_attribute(file_traj, attribute)


def test_h5msm_reader_preserves_nonmonotonic_repeated_frame_order(tmp_path):
    puw = msm.pyunitwizard
    structures = Structures(
        structure_id=[10, 11, 12],
        time=puw.quantity([0.0, 1.0, 2.0], 'ps'),
        coordinates=puw.quantity(np.arange(36).reshape(3, 4, 3), 'angstrom'),
        velocities=puw.quantity(np.arange(36).reshape(3, 4, 3), 'angstrom/ps'),
        box=puw.quantity(np.arange(27).reshape(3, 3, 3), 'angstrom'),
        b_factor=puw.quantity(np.arange(12).reshape(3, 4), 'angstrom**2'),
        temperature=puw.quantity([290.0, 300.0, 310.0], 'K'),
        potential_energy=puw.quantity([-1.0, -2.0, -3.0], 'kcal/mol'),
        kinetic_energy=puw.quantity([0.1, 0.2, 0.3], 'kcal/mol'),
        skip_digestion=True,
    )
    output = tmp_path / 'ordered-subset.h5msm'
    msm.convert(structures, to_form='file:h5msm', output_filename=output)

    selected_time = msm.get(output, time=True, structure_indices=[2, 0, 2])
    selected_coordinates = msm.get(
        output,
        coordinates=True,
        structure_indices=[2, 0, 2],
    )
    np.testing.assert_allclose(
        puw.get_value(selected_time, to_unit='ps'),
        [2.0, 0.0, 2.0],
    )
    np.testing.assert_allclose(
        puw.get_value(selected_coordinates, to_unit='nm')[:, 0, 0],
        [2.4, 0.0, 2.4],
    )

    recovered = msm.convert(
        output,
        to_form='molsysmt.Structures',
        selection=[3, 1],
        structure_indices=[2, 0, 2],
    )

    assert list(recovered.structure_id) == [12, 10, 12]
    assert recovered.coordinates.shape == (3, 2, 3)
    assert recovered.velocities.shape == (3, 2, 3)
    assert recovered.b_factor.shape == (3, 2)
    np.testing.assert_allclose(
        puw.get_value(recovered.time, to_unit='ps'),
        [2.0, 0.0, 2.0],
    )
    np.testing.assert_allclose(
        puw.get_value(recovered.temperature, to_unit='K'),
        [310.0, 290.0, 310.0],
    )
    np.testing.assert_allclose(
        puw.get_value(recovered.potential_energy, to_unit='kJ/mol'),
        [-12.552, -4.184, -12.552],
    )


def test_h5msm_dataset_unit_does_not_require_root_unit_fallback(tmp_path):
    import h5py

    puw = msm.pyunitwizard
    structures = Structures(
        coordinates=puw.quantity(np.ones((1, 1, 3)), 'nm'),
        skip_digestion=True,
    )
    output = tmp_path / 'dataset-unit.h5msm'
    msm.convert(structures, to_form='file:h5msm', output_filename=output)

    with h5py.File(output, 'r+') as file:
        coordinates = file['structures']['coordinates']
        coordinates[:] = 1.0
        coordinates.attrs['unit'] = 'angstrom'
        del file.attrs['length_unit']

    recovered = msm.convert(output, to_form='molsysmt.Structures')

    np.testing.assert_allclose(
        puw.get_value(recovered.coordinates, to_unit='nm'),
        0.1,
    )
