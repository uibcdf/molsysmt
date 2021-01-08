def to_openmm_Topology (item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology

    tmp_item = molsysmt_Topology_to_openmm_Topology(item.topology, atom_indices=atom_indices)

    return tmp_item

def from_openmm_Topology (item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.trajectory import Trajectory
    from molsysmt.native.io.topology.classes import from_openmm_Topology as openmm_Topology_to_molsysmt_Topology
    from molsysmt import convert

    tmp_item = MolSys()
    tmp_item.topology = openmm_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    if trajectory_item is None:
        tmp_item.trajectory = Trajectory()
    else:
        tmp_item.trajectory = convert(trajectory_item, selection=atom_indices, frame_indices=frame_indices, to_form='molsysmt.Trajectory')
    return tmp_item

