def from_h5(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.files.api_h5 import to_mdtraj_Topology as h5_to_mdtraj_Topology
    from molsysmt.native.io.topology.classes import from_mdtraj_Topology as mdtraj_Topology_to_molsysmt_Topology

    tmp_item = h5_to_mdtraj_Topology(item)
    tmp_item = mdtraj_Topology_to_molsysmt_Topology(tmp_item)

    return tmp_item

