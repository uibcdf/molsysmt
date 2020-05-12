def from_h5(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.files.api_h5 import to_mdtraj_Topology as h5_to_mdtraj_Topology
    from molsysmt.native.io.dataframe.classes import from_mdtraj_Topology as mdtraj_Topology_to_molsysmt_DataFrame

    tmp_item = h5_to_mdtraj_Topology(item)
    tmp_item = mdtraj_Topology_to_molsysmt_DataFrame(tmp_item)

    return tmp_item

