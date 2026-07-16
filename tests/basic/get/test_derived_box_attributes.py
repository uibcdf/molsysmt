import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


def _mdtraj_trajectory_with_cubic_boxes():
    mdtraj = pytest.importorskip('mdtraj')
    topology = mdtraj.Topology()
    chain = topology.add_chain()
    residue = topology.add_residue('ALA', chain)
    topology.add_atom('CA', mdtraj.element.carbon, residue)
    return mdtraj.Trajectory(
        np.zeros((3, 1, 3), dtype=float),
        topology,
        unitcell_lengths=np.array([[2.0, 2.0, 2.0], [3.0, 3.0, 3.0], [4.0, 4.0, 4.0]]),
        unitcell_angles=np.full((3, 3), 90.0),
    )


def test_get_derives_box_attributes_without_converting_mdtraj_coordinates():
    trajectory = _mdtraj_trajectory_with_cubic_boxes()

    lengths, angles, shape, volume = msm.get(
        trajectory,
        element='system',
        structure_indices=[0, 2],
        box_lengths=True,
        box_angles=True,
        box_shape=True,
        box_volume=True,
    )

    assert np.allclose(puw.get_value(lengths), [[2.0, 2.0, 2.0], [4.0, 4.0, 4.0]])
    assert puw.get_unit(lengths) == puw.unit('nanometer')
    assert np.allclose(puw.get_value(angles), np.full((2, 3), np.pi / 2), atol=1.0e-6)
    assert puw.get_unit(angles) == puw.unit('radian')
    assert shape == 'cubic'
    assert np.allclose(puw.get_value(volume), [8.0, 64.0])
    assert puw.get_unit(volume) == puw.unit('nanometer**3')


def test_mdtraj_box_getter_applies_structure_indices():
    trajectory = _mdtraj_trajectory_with_cubic_boxes()

    box = msm.get(trajectory, element='system', structure_indices=[0, 2], box=True)

    assert puw.get_value(box).shape == (2, 3, 3)
    assert np.allclose(puw.get_value(box)[:, 0, 0], [2.0, 4.0])


def test_openmm_prmtop_exposes_and_derives_its_periodic_box():
    pytest.importorskip('openmm')
    prmtop = msm.convert(
        msm.systems['pentalanine']['pentalanine.prmtop'],
        to_form='openmm.AmberPrmtopFile',
    )

    box, lengths, angles, shape, volume = msm.get(
        prmtop,
        element='system',
        structure_indices=[0],
        box=True,
        box_lengths=True,
        box_angles=True,
        box_shape=True,
        box_volume=True,
    )

    assert puw.get_value(box).shape == (1, 3, 3)
    assert np.allclose(puw.get_value(lengths), [[4.295111, 4.295111, 4.295111]], atol=1.0e-6)
    assert np.allclose(puw.get_value(angles), [[1.910633, 1.910633, 1.910633]], atol=1.0e-6)
    assert shape == 'triclinic'
    assert np.allclose(puw.get_value(volume), [60.9959907779])
