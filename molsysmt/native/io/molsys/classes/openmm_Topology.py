def to_openmm_Topology (item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology
    from molsysmt import get, set

    tmp_item = item.topology
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)

    tmp_item, tmp_molecular_system = molsysmt_Topology_to_openmm_Topology(tmp_item, tmp_molecular_system, atom_indices=atom_indices)

    if frame_indices is 'all':
        box = get(item, target='system', frame_indices=0, box=True)
    else:
        box = get(item, target='system', frame_indices=frame_indices, box=True)

    if box is not None:
        set(tmp_item, target='system', box=box)

    return tmp_item, tmp_molecular_system

def from_openmm_Topology (item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.trajectory import Trajectory
    from molsysmt.native.io.topology.classes import from_openmm_Topology as openmm_Topology_to_molsysmt_Topology
    from molsysmt import convert, get, set

    tmp_item = MolSys()
    tmp_item.topology, _ = openmm_Topology_to_molsysmt_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    if trajectory_item is None:
        tmp_item.trajectory = Trajectory()
    else:
        tmp_item.trajectory = convert(trajectory_item, selection=atom_indices, frame_indices=frame_indices, to_form='molsysmt.Trajectory')
        if not get(trajectory_item, target='system', has_box=True):
            if get(item, target='system', has_box=True):
                box = get(item, target='system', box=True)
                if box is not None:
                    set(tmp_item.trajectory, target='system', box=box)

    tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

