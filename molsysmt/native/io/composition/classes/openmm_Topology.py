def from_openmm_Topology(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.classes import from_openmm_Topology as openmm_Topology_to_molsysmt_DataFrame
    from .molsysmt_DataFrame import from_molsysmt_DataFrame as molsysmt_DataFrame_to_molsysmt_Composition

    tmp_item = openmm_Topology_to_molsysmt_DataFrame(item)
    tmp_item = molsysmt_DataFrame_to_molsysmt_Composition(tmp_item)

    return tmp_item
