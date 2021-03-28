def to_openmm_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from .molsysmt_DataFrame import to_molsysmt_DataFrame as molsysmt_Topology_to_molsysmt_DataFrame
    from molsysmt.native.io.dataframe.classes import to_openmm_Topology as molsysmt_DataFrame_to_openmm_Topology

    tmp_item = molsysmt_Topology_to_molsysmt_DataFrame(item)
    tmp_item = molsysmt_DataFrame_to_openmm_Topology(tmp_item)

    return tmp_item


def from_openmm_Topology(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.classes import from_openmm_Topology as openmm_Topology_to_molsysmt_DataFrame
    from .molsysmt_DataFrame import from_molsysmt_DataFrame as molsysmt_DataFrame_to_molsysmt_Topology

    tmp_item = openmm_Topology_to_molsysmt_DataFrame(item)
    tmp_item = molsysmt_DataFrame_to_molsysmt_Topology(tmp_item)

    return tmp_item
