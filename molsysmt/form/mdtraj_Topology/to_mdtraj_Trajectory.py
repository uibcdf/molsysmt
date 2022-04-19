from molsysmt._private.digestion import digest_item, digest_atom_indices
from molsysmt._private.digestion import digest_coordinates, digest_box

def to_mdtraj_Trajectory(item, atom_indices='all', coordinates=None, box=None, check=True):

    if check:

        digest_item(item, 'mdtraj.Topology')
        atom_indices = digest_atom_indices(atom_indices)
        coordinates = digest_coordinates(coordinates)
        box = digest_box(box)

    from mdtraj.core.trajectory import Trajectory
    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, check=False)
    tmp_item = Trajectory(coordinates, item)

    return tmp_item
