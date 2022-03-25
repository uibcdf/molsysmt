from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_mmtf_MMTFDecoder import is_mmtf_MMTFDecoder

def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, check=True):

    if check:

        try:
            is_mmtf_MMTFDecoder(item)
        except:
            raise WrongFormError('mmtf.MMTFDecoder')

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
            from copy import deepcopy
            tmp_item = deepcopy(item)
        else:
            tmp_item = item
    else:
        raise NotImplementedMethodError()

    return tmp_item

