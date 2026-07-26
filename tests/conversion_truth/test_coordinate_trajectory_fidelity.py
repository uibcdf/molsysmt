"""Testing exhaustive fidelity for coordinate-only trajectory forms."""

from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


DCD_PATH = (
    Path(msm.__file__).parent
    / 'data'
    / 'dcd'
    / 'traj_chicken_villin_HP35_solvated.dcd'
)


def _coordinate_payload():
    return np.arange(3 * 4 * 3, dtype=np.float64).reshape(3, 4, 3)


def test_xyz_native_routes_are_exhaustive_subset_safe_and_unit_safe(tmp_path):
    values = _coordinate_payload()
    xyz = puw.quantity(values * 10.0, 'angstrom')
    atom_indices = [3, 1]
    structure_indices = [2, 0]
    expected = values[np.ix_(structure_indices, [1, 3], [0, 1, 2])]

    structures, structures_report = msm.convert(
        xyz,
        to_form='molsysmt.Structures',
        selection=atom_indices,
        structure_indices=structure_indices,
        return_report=True,
    )
    molsys, molsys_report = msm.convert(
        xyz,
        to_form='molsysmt.MolSys',
        selection=atom_indices,
        structure_indices=structure_indices,
        return_report=True,
    )

    for report in (structures_report, molsys_report):
        assert report.is_exhaustive is True
        assert report.audited_scopes == ('all',)
        assert report.outcome == 'equivalent'
    assert molsys.topology.n_atoms == 2
    np.testing.assert_allclose(
        puw.get_value(structures.coordinates, to_unit='nm'),
        expected,
    )
    np.testing.assert_allclose(
        puw.get_value(molsys.structures.coordinates, to_unit='nm'),
        expected,
    )

    topology, topology_report = msm.convert(
        xyz,
        to_form='molsysmt.Topology',
        selection=atom_indices,
        return_report=True,
    )
    assert topology.n_atoms == 2
    assert topology_report.is_exhaustive is True
    assert topology_report.outcome == 'lossy'
    assert 'coordinates' in {
        issue.attribute for issue in topology_report.issues
    }
    with pytest.raises(msm.NotCompatibleConversionError, match='coordinates'):
        msm.convert(xyz, to_form='molsysmt.Topology', strict=True)

    output = tmp_path / 'selected.xyznpy'
    _, write_report = msm.convert(
        xyz,
        to_form='file:xyznpy',
        selection=atom_indices,
        structure_indices=structure_indices,
        output_filename=output,
        return_report=True,
    )
    restored, read_report = msm.convert(
        output,
        to_form='XYZ',
        return_report=True,
    )
    for report in (write_report, read_report):
        assert report.is_exhaustive is True
        assert report.outcome == 'equivalent'
    assert msm.get(output, n_atoms=True) == 2
    assert msm.get(output, n_structures=True) == 2
    assert msm.get(output, structure_index=True) == [0, 1]
    np.testing.assert_allclose(
        puw.get_value(restored, to_unit='nm'),
        expected,
    )


def test_ascii_xyz_to_xyz_is_exhaustive_and_preserves_requested_frames(tmp_path):
    filename = tmp_path / 'trajectory.xyz'
    values = _coordinate_payload()
    rows = '\n'.join(
        ' '.join(str(component) for component in coordinate)
        for coordinate in values.reshape(-1, 3)
    )
    filename.write_text(f'3 4\n{rows}\n', encoding='utf-8')

    output, report = msm.convert(
        filename,
        to_form='XYZ',
        selection=[3, 1],
        structure_indices=[2, 0],
        return_report=True,
    )

    assert report.is_exhaustive is True
    assert report.outcome == 'equivalent'
    assert msm.get(filename, structure_index=True) == [0, 1, 2]
    np.testing.assert_allclose(
        puw.get_value(output, to_unit='nm'),
        values[np.ix_([2, 0], [1, 3], [0, 1, 2])],
    )


def test_dcd_native_routes_are_exhaustive_and_preserve_handler_cursor(tmp_path):
    mdtraj = pytest.importorskip('mdtraj')
    atom_indices = [8, 2]
    structure_indices = [8, 1]

    structures, structures_report = msm.convert(
        DCD_PATH,
        to_form='molsysmt.Structures',
        selection=atom_indices,
        structure_indices=structure_indices,
        return_report=True,
    )
    molsys, molsys_report = msm.convert(
        DCD_PATH,
        to_form='molsysmt.MolSys',
        selection=atom_indices,
        structure_indices=structure_indices,
        return_report=True,
    )
    for report in (structures_report, molsys_report):
        assert report.is_exhaustive is True
        assert report.outcome == 'equivalent'
    assert structures.structure_id.tolist() == structure_indices
    assert molsys.topology.n_atoms == 2
    assert molsys.structures.structure_id.tolist() == structure_indices

    with mdtraj.formats.DCDTrajectoryFile(str(DCD_PATH), mode='r') as reader:
        reader.seek(4)
        handler_structures, handler_structures_report = msm.convert(
            reader,
            to_form='molsysmt.Structures',
            selection=atom_indices,
            structure_indices=structure_indices,
            return_report=True,
        )
        handler_molsys, handler_molsys_report = msm.convert(
            reader,
            to_form='molsysmt.MolSys',
            selection=atom_indices,
            structure_indices=structure_indices,
            return_report=True,
        )
        assert reader.tell() == 4
    for report in (handler_structures_report, handler_molsys_report):
        assert report.is_exhaustive is True
        assert report.outcome == 'equivalent'
    np.testing.assert_allclose(
        puw.get_value(handler_structures.coordinates, to_unit='nm'),
        puw.get_value(structures.coordinates, to_unit='nm'),
    )
    np.testing.assert_allclose(
        puw.get_value(handler_structures.box, to_unit='nm'),
        puw.get_value(structures.box, to_unit='nm'),
    )
    assert handler_structures.structure_id.tolist() == structure_indices
    np.testing.assert_allclose(
        puw.get_value(handler_molsys.structures.box, to_unit='nm'),
        puw.get_value(molsys.structures.box, to_unit='nm'),
    )

    h5msm = tmp_path / 'selected-dcd.h5msm'
    _, h5_report = msm.convert(
        DCD_PATH,
        to_form='file:h5msm',
        selection=atom_indices,
        structure_indices=structure_indices,
        output_filename=h5msm,
        return_report=True,
    )
    assert h5_report.is_exhaustive is True
    assert h5_report.outcome == 'equivalent'
    np.testing.assert_allclose(
        puw.get_value(msm.get(h5msm, coordinates=True), to_unit='nm'),
        puw.get_value(structures.coordinates, to_unit='nm'),
        atol=1.0e-6,
    )


def test_xtc_routes_are_exhaustive_and_report_step_id_loss(
    builder_trajectory_xtc_file,
    tmp_path,
):
    mdtraj = pytest.importorskip('mdtraj')
    atom_indices = [3, 1]
    structure_indices = [2, 0]

    structures, structures_report = msm.convert(
        builder_trajectory_xtc_file,
        to_form='molsysmt.Structures',
        selection=atom_indices,
        structure_indices=structure_indices,
        return_report=True,
    )
    assert structures_report.is_exhaustive is True
    assert structures_report.outcome == 'equivalent'
    assert structures.coordinates.shape == (2, 2, 3)
    assert structures.structure_id.tolist() == [2, 0]

    with mdtraj.formats.XTCTrajectoryFile(
        str(builder_trajectory_xtc_file), mode='r'
    ) as reader:
        reader.seek(1)
        handler_structures, handler_report = msm.convert(
            reader,
            to_form='molsysmt.Structures',
            selection=atom_indices,
            structure_indices=structure_indices,
            return_report=True,
        )
        assert reader.tell() == 1
    assert handler_report.is_exhaustive is True
    assert handler_report.outcome == 'equivalent'
    np.testing.assert_allclose(
        puw.get_value(handler_structures.coordinates, to_unit='nm'),
        puw.get_value(structures.coordinates, to_unit='nm'),
    )
    np.testing.assert_allclose(
        puw.get_value(handler_structures.box, to_unit='nm'),
        puw.get_value(structures.box, to_unit='nm'),
    )
    np.testing.assert_allclose(
        puw.get_value(handler_structures.time, to_unit='ps'),
        puw.get_value(structures.time, to_unit='ps'),
    )
    assert handler_structures.structure_id.tolist() == structure_indices

    trajectory, trajectory_report = msm.convert(
        builder_trajectory_xtc_file,
        to_form='mdtraj.Trajectory',
        selection=atom_indices,
        structure_indices=structure_indices,
        return_report=True,
    )
    assert trajectory_report.is_exhaustive is True
    assert trajectory_report.outcome == 'lossy'
    assert 'structure_id' in {
        issue.attribute for issue in trajectory_report.issues
    }
    assert trajectory.topology is None
    assert trajectory.xyz.shape == (2, 2, 3)
    np.testing.assert_allclose(trajectory.xyz, puw.get_value(structures.coordinates))
    np.testing.assert_allclose(
        trajectory.time,
        puw.get_value(structures.time, to_unit='ps'),
    )
    np.testing.assert_allclose(
        trajectory.unitcell_vectors,
        puw.get_value(structures.box, to_unit='nm'),
    )
    with pytest.raises(msm.NotCompatibleConversionError, match='structure_id'):
        msm.convert(
            builder_trajectory_xtc_file,
            to_form='mdtraj.Trajectory',
            strict=True,
        )

    h5msm = tmp_path / 'selected-xtc.h5msm'
    _, h5_report = msm.convert(
        builder_trajectory_xtc_file,
        to_form='file:h5msm',
        selection=atom_indices,
        structure_indices=structure_indices,
        output_filename=h5msm,
        return_report=True,
    )
    assert h5_report.is_exhaustive is True
    assert h5_report.outcome == 'equivalent'
    np.testing.assert_allclose(
        puw.get_value(msm.get(h5msm, coordinates=True), to_unit='nm'),
        puw.get_value(structures.coordinates, to_unit='nm'),
        atol=1.0e-6,
    )
    np.testing.assert_allclose(
        puw.get_value(msm.get(h5msm, box=True), to_unit='nm'),
        puw.get_value(structures.box, to_unit='nm'),
        atol=1.0e-6,
    )
    np.testing.assert_allclose(
        puw.get_value(msm.get(h5msm, time=True), to_unit='ps'),
        puw.get_value(structures.time, to_unit='ps'),
    )
    assert list(msm.get(h5msm, structure_id=True)) == ['2', '0']
