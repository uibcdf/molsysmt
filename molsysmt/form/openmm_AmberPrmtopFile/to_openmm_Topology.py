from .is_file_openmm_AmberPrmtopFile import is_file_openmm_AmberPrmtopFile
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_openmm_Topology(item, atom_indices='all', check=True):

    if check:

        try:
            is_openmm_AmberPrmtopFile(item)
        except:
            raise WrongFormError('openmm.AmberPrmtopFile')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

    from . import to_openmm_Topology

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, check=check)

    return tmp_item

