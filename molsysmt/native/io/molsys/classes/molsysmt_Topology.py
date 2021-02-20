def to_molsysmt_Topology(item, atom_indices='all', frame_indices='all', topology_item=None,
                         trajectory_item=None, coordinates_item=None, box_item=None):

    return item.topology.copy()

