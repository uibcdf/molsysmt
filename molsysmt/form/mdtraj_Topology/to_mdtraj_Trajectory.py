from molsysmt._private.digestion import digest

@digest(form='mdtraj.Topology')
def to_mdtraj_Trajectory(item, atom_indices='all', coordinates=None, box=None):

    from mdtraj.core.trajectory import Trajectory
    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices)
    tmp_item = Trajectory(coordinates, item)

    return tmp_item

def _to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.basic import get

    coordinates = get(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                      coordinates=True)
    box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)

    return to_mdtraj_Trajectory(item, atom_indices=atom_indices, coordinates=coordinates, box=box)

