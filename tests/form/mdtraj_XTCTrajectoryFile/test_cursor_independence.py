"""Testing cursor-independent access to MDTraj XTC readers."""

import mdtraj as md
import numpy as np

import molsysmt as msm
from molsysmt.form.mdtraj_XTCTrajectoryFile import (
    get_box_from_system,
    get_coordinates_from_atom,
    get_time_from_system,
)


def test_structural_getters_preserve_cursor_and_can_be_composed():
    xtc = msm.systems['nglview']['md_1u19.xtc']

    with md.open(str(xtc)) as reader:
        reader.seek(7)
        coordinates = get_coordinates_from_atom(
            reader,
            indices=[0, 1],
            structure_indices=[0, 25, 50],
        )
        time = get_time_from_system(
            reader,
            structure_indices=[0, 25, 50],
        )
        box = get_box_from_system(
            reader,
            structure_indices=[0, 25, 50],
        )

        assert reader.tell() == 7

    assert msm.pyunitwizard.get_value(coordinates).shape == (3, 2, 3)
    np.testing.assert_allclose(msm.pyunitwizard.get_value(time), [0.0, 500.0, 1000.0])
    assert msm.pyunitwizard.get_value(box).shape == (3, 3, 3)


def test_xtc_conversion_reads_coordinates_time_and_box_together():
    gro = msm.systems['nglview']['md_1u19.gro']
    xtc = msm.systems['nglview']['md_1u19.xtc']

    molecular_system = msm.convert(
        [gro, xtc],
        structure_indices=[0, 25, 50],
        to_form='molsysmt.MolSys',
    )

    assert molecular_system.structures.coordinates.shape == (3, 5547, 3)
    assert molecular_system.structures.time.shape == (3,)
    assert molecular_system.structures.box.shape == (3, 3, 3)
