def to_biopython_Seq(item, atom_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
    from molsysmt.tools.molsysmt_MolSys import to_string_aminoacids1
    from molsysmt.tools.string_aminoacids1 import to_biopython_Seq as string_aminoacids1_to_biopython_Seq

    if not is_molsysmt_MolSys(item):
        raise ValueError

    tmp_item = to_string_aminoacids1(item, atom_indices=atom_indices)
    tmp_item = string_aminoacids1_to_biopython_Seq(tmp_item)

    return tmp_item

