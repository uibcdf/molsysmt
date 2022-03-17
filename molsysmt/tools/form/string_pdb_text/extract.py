from molsysmt.tools.string_pdb_text.is_string_pdb_text import is_string_pdb_text
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private_tools.exceptions import NotImplementedMethodError
from molsysmt._private_tools.atom_indices import digest_atom_indices
from molsysmt._private_tools.structure_indices import digest_structure_indices

def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, check=True):

    if check:

        try:
            is_pdbfixer_PDBFixer(item)
        except:
            raise WrongFormError('pdbfixer.PDBFixer')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()


    if (atom_indices is 'all') and (structure_indices is 'all'):

        if copy_if_all:
            from copy import copy
            tmp_item = copy(item)
        else:
            tmp_item = item
    else:

        from molsysmt.tools.string_pdb_text import to_molsysmt_MolSys as string_pdb_text_to_molsysmt_MolSys
        from molsysmt.tools.molsysmt_MolSys import to_string_pdb_text as molsysmt_MolSys_to_string_pdb_text
        tmp_item = string_pdb_text_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
        tmp_item = molsysmt_MolSys_to_string_pdb_text(tmp_item, output_filename=output_filename, check=False)

    return tmp_item

