

def from_h5(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.api_h5 import to_mdtraj_Topology as h5_to_mdtraj_Topology
    from molsysmt.native.io.topology import from_mdtraj_Topology as mdtraj_Topology_to_molsysmt_Topology

    tmp_item = h5_to_mdtraj_Topology(item)
    tmp_item = mdtraj_Topology_to_molsysmt_Topology(tmp_item)

    return tmp_item

