from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_file_prmtop import is_file_prmtop

def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, check=True):

    if check:

        try:
            is_file_prmtop(item)
        except:
            raise WrongFormError('file:prmtop')

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

            from shutil import copy as copy_file
            copy_file(item, output_filename)
            tmp_item = output_filename

        else:
            tmp_item = item
    else:

        raise NotImplementedError()

    return tmp_item

