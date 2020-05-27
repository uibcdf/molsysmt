def from_parmed_Structure(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.classes import from_parmed_Structure as parmed_Structure_to_molsysmt_DataFrame
    from .molsysmt_DataFrame import from_molsysmt_DataFrame as molsysmt_DataFrame_to_molsysmt_Topology

    tmp_item = parmed_Structure_to_molsysmt_DataFrame(item)
    tmp_item = molsysmt_DataFrame_to_molsysmt_Topology(tmp_item)

    return tmp_item

