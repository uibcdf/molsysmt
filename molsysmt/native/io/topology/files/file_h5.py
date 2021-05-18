def from_file_h5(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.files.api_file_h5 import to_mdtraj_Topology as file_h5_to_mdtraj_Topology
    from molsysmt.native.io.topology.classes import from_mdtraj_Topology as mdtraj_Topology_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = file_h5_to_mdtraj_Topology(item, molecular_system)
    tmp_item, tmp_molecular_system = mdtraj_Topology_to_molsysmt_Topology(tmp_item, tmp_molecular_system)

    return tmp_item, tmp_molecular_system

