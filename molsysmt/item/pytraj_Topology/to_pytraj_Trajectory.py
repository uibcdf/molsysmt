from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import LibraryNotFoundError

@digest(form='pytraj.Topology')
def to_pytraj_Trajectory(item, atom_indices='all', coordinates=None, box=None):

    try:
        import pytraj as pt
    except:
        raise LibraryNotFoundError('pytraj')

    from . import extract
    from molsysmt import pyunitwizard as puw
    from molsysmt.pbc import box_to_box_angles

    tmp_item = extract(item, atom_indices=atom_indices, copy_if_all=False)

    coordinates = puw.get_value(coordinates, to_unit='angstroms')
    tmp_item = pt.Trajectory(xyz=coordinates, top=tmp_item)

    box_lengths = box_lengths_from_box(box)
    box_angles = box_angles_from_box(box)

    box_lengths = puw.get_value(box_lengths, to_unit='angstroms')
    box_angles = puw.get_value(box_angles, to_unit='degrees')

    tmp_item.unitcells = np.hstack([box_lengths, box_angles])

    return tmp_item

