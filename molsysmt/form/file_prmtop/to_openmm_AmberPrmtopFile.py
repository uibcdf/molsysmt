from .is_file_prmtop import is_file_prmtop
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_openmm_AmberPrmtopFile(item, atom_indices='all', check=True):

    if check:

        try:
            is_file_prmtop(item)
        except:
            raise WrongFormError('file:prmtop')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

    from openmm.app import AmberPrmtopFile

    tmp_item = AmberPrmtopFile(item)

    return tmp_item

