def from_file_h5(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.api_file_h5 import to_mdtraj_Topology as file_h5_to_mdtraj_Topology
    from molsysmt.native.io.topology import from_mdtraj_Topology as mdtraj_Topology_to_molsysmt_Topology

    tmp_item, _ = file_h5_to_mdtraj_Topology(item)
    tmp_item, _ = mdtraj_Topology_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

