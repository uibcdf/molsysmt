from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest

@digest(form='openmm.Modeller')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', digest=True):

    try:
        from mdtraj.core.trajectory import Trajectory as mdtraj_Trajectory
    except:
        raise LibraryNotFoundError('MDTraj')

    from . import to_mdtraj_Topology
    from ..mdtraj_Trajectory import extract as extract_mdtraj_Trajectory
    from molsysmt import pyunitwizard as puw

    tmp_topology  = to_mdtraj_Topology(item, digest=False)
    positions = puw.get_value(item.positions, to_unit='nanometers')
    tmp_item = mdtraj_Trajectory(positions, tmp_topology)
    tmp_item = extract_mdtraj_Trajectory(tmp_item, atom_indices=atom_indices,
                                         structure_indices=structure_indices, copy_if_all=False, digest=False)

    return tmp_item

