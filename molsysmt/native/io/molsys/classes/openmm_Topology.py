def to_openmm_Topology (item, atom_indices='all', frame_indices='all', topology_item=None,
                        trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.topology.classes import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology
    from molsysmt import get, set

    tmp_item = molsysmt_Topology_to_openmm_Topology(item.topology, atom_indices=atom_indices)

    if frame_indices is 'all':
        box = get(item, target='system', frame_indices=0, box=True)
    else:
        box = get(item, target='system', frame_indices=frame_indices, box=True)

    set(tmp_item, target='system', box=box)

    return tmp_item

def from_openmm_Topology (item, atom_indices='all', frame_indices='all', topology_item=None,
                          trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.trajectory import Trajectory
    from molsysmt.native.io.topology.classes import from_openmm_Topology as openmm_Topology_to_molsysmt_Topology
    from molsysmt import convert, get, set

    tmp_item = MolSys()
    tmp_item.topology = openmm_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)

    if trajectory_item is None:
        tmp_item.trajectory = Trajectory()
    else:
        tmp_item.trajectory = convert(trajectory_item, selection=atom_indices, frame_indices=frame_indices, to_form='molsysmt.Trajectory')
        if not get(trajectory_item, target='system', has_box=True):
            if get(item, target='system', has_box=True):
                box = get(item, target='system', box=True)
                set(tmp_item.trajectory, target='system', box=box)

    return tmp_item

