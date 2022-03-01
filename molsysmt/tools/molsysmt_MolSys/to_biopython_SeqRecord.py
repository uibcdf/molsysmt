def to_biopython_SeqRecord(item, atom_indices='all', check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
        from molsysmt._private_tools.exceptions import WrongFormError
        if not is_molsysmt_MolSys(item):
            raise WrongFormError('molsysmt.MolSys')

    from molsysmt.tools.molsysmt_MolSys import to_string_aminoacids1 as molsysmt_MolSys_to_string_aminoacids1
    from molsysmt.tools.string_aminoacids1 import to_biopython_SeqRecord as string_aminoacids1_to_biopython_SeqRecord

    tmp_item = molsysmt_MolSys_to_string_aminoacids1(item, atom_indices=atom_indices, check_form=False)
    tmp_item = string_aminoacids1_to_biopython_SeqRecord(tmp_item, check_form=False)

    return tmp_item

