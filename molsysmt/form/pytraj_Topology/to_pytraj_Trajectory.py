from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import LibraryNotFoundError
import numpy as np

@digest(form='pytraj.Topology')
def to_pytraj_Trajectory(item, atom_indices='all', coordinates=None, box=None):

    try:
        import pytraj as pt
    except:
        raise LibraryNotFoundError('pytraj')

    from . import extract
    from molsysmt import pyunitwizard as puw
    from molsysmt.pbc import get_lengths_and_angles_from_box

    tmp_item = extract(item, atom_indices=atom_indices, copy_if_all=False)

    coordinates = puw.get_value(coordinates, to_unit='angstroms')
    tmp_item = pt.Trajectory(xyz=coordinates.astype('float64'), top=tmp_item)

    box_lengths, box_angles = get_lengths_and_angles_from_box(box)

    box_lengths = puw.get_value(box_lengths, to_unit='angstroms')
    box_angles = puw.get_value(box_angles, to_unit='degrees')

    tmp_item.unitcells = np.hstack([box_lengths, box_angles])
    tmp_item.unitcells = tmp_item.unitcells.astype('float64')

    return tmp_item

def _to_pytraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_pytraj_Trajectory(item, atom_indices=atom_indices)

