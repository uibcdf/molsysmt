def from_h5(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.files.api_h5 import to_mdtraj_Topology as h5_to_mdtraj_Topology
    from molsysmt.native.io.topology.classes import from_mdtraj_Topology as mdtraj_Topology_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = h5_to_mdtraj_Topology(item, molecular_system)
    tmp_item, tmp_molecular_system = mdtraj_Topology_to_molsysmt_Topology(tmp_item, tmp_molecular_system)

    return tmp_item, tmp_molecular_system

