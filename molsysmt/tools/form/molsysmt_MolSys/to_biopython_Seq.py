from molsysmt.tools.molsysmt_MolSys.is_molsysmt_MolSys import is_molsysmt_MolSys
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private_tools.group_indices import digest_group_indices

def to_biopython_Seq(item, group_indices='all', check=True):

    if check:

        try:
            is_molsysmt_MolSys(item)
        except:
            raise WrongFormError('molsysmt.MolSys')

        try:
            group_indices = digest_atom_indices(group_indices)
        except:
            raise WrongAtomIndicesError()

    from molsysmt.tools.molsysmt_MolSys import to_string_aminoacids1 as molsysmt_MolSys_to_string_aminoacids1
    from molsysmt.tools.string_aminoacids1 import to_biopython_Seq as string_aminoacids1_to_biopython_Seq

    tmp_item = molsysmt_MolSys_to_string_aminoacids1(item, group_indices=group_indices, check=False)
    tmp_item = string_aminoacids1_to_biopython_Seq(tmp_item, check=False)

    return tmp_item

