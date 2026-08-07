from molsysmt._private.smonitor import LibraryNotFoundError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Modeller')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    try:
        from mdtraj.core.trajectory import Trajectory as mdtraj_Trajectory
    except Exception:
        raise LibraryNotFoundError('MDTraj')

    from molsysmt.form.mdtraj_Topology import to_mdtraj_Topology
    from ..mdtraj_Trajectory.extract import extract as extract_mdtraj_Trajectory
    from molsysmt import pyunitwizard as puw

    tmp_topology  = to_mdtraj_Topology(item, skip_digestion=False)
    positions = puw.get_value(item.positions, to_unit='nanometers')
    tmp_item = mdtraj_Trajectory(positions, tmp_topology)
    tmp_item = extract_mdtraj_Trajectory(tmp_item, atom_indices=atom_indices,
                                         structure_indices=structure_indices, copy_if_all=False, skip_digestion=False)

    return tmp_item

