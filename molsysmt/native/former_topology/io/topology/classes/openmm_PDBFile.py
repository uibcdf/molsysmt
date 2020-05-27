def from_openmm_PDBFile (item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.classes import from_openmm_PDBFile as openmm_PDBFile_to_molsysmt_DataFrame
    from .molsysmt_DataFrame import from_molsysmt_DataFrame as molsysmt_DataFrame_to_molsysmt_Topology

    tmp_item = openmm_PDBFile_to_molsysmt_DataFrame(item)
    tmp_item = molsysmt_DataFrame_to_molsysmt_Topology(tmp_item)

    return tmp_item

