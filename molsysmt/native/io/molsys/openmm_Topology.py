def from_openmm_Topology (item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.trajectory import Trajectory
    from molsysmt.native.io.topology import from_openmm_Topology as openmm_Topology_to_molsysmt_Topology
    from molsysmt import convert, get, set

    tmp_item = MolSys()
    tmp_item.topology, _ = openmm_Topology_to_molsysmt_Topology(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    if trajectory_item is None:
        tmp_item.trajectory = Trajectory()
    else:
        tmp_item.trajectory = convert(trajectory_item, selection=atom_indices, frame_indices=frame_indices, to_form='molsysmt.Trajectory')
        if not get(trajectory_item, target='system', has_box=True):
            if get(item, target='system', has_box=True):
                box = get(item, target='system', box=True)
                if box is not None:
                    set(tmp_item.trajectory, target='system', box=box)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

