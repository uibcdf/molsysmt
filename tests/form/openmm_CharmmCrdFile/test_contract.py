"""Contract tests for native data retained by OpenMM CHARMM readers."""

import numpy as np
import pytest

import molsysmt as msm


def test_charmm_crd_delivers_native_topology_and_coordinates():
    openmm_app = pytest.importorskip('openmm.app')
    item = openmm_app.CharmmCrdFile(str(msm.systems['POPC']['popc.crd']))

    output = msm.get(
        item,
        element='atom',
        selection=[0, 1],
        atom_index=True,
        atom_id=True,
        atom_name=True,
        atom_type=True,
        group_index=True,
        group_id=True,
        group_name=True,
        group_type=True,
        coordinates=True,
    )

    assert output[:-1] == [
        [0, 1],
        ['1', '2'],
        ['N', 'C12'],
        ['N', 'C'],
        [0, 0],
        ['1', '1'],
        ['POPC', 'POPC'],
        ['lipid', 'lipid'],
    ]
    assert output[-1].shape == (1, 2, 3)
    assert np.all(np.isfinite(msm.pyunitwizard.get_value(output[-1])))


def test_charmm_crd_group_level_getters_preserve_group_semantics():
    openmm_app = pytest.importorskip('openmm.app')
    item = openmm_app.CharmmCrdFile(str(msm.systems['POPC']['popc.crd']))

    group_index, group_id, group_name, group_type = msm.get(
        item,
        element='group',
        selection=[0],
        group_index=True,
        group_id=True,
        group_name=True,
        group_type=True,
    )

    assert group_index == [0]
    assert group_id == ['1']
    assert group_name == ['POPC']
    assert group_type == ['lipid']


def test_charmm_psf_delivers_optional_periodic_box():
    openmm = pytest.importorskip('openmm')
    openmm_app = pytest.importorskip('openmm.app')
    item = openmm_app.CharmmPsfFile(
        str(msm.systems['POPC']['popc.psf']),
        unitCellDimensions=openmm.Vec3(4.0, 5.0, 6.0) * openmm.unit.nanometer,
    )

    box = msm.get(item, box=True)

    assert box.shape == (1, 3, 3)
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(box, to_unit='nm')[0],
        np.diag([4.0, 5.0, 6.0]),
    )
