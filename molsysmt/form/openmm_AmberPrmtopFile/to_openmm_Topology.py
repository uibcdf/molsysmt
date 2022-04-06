from .is_openmm_AmberPrmtopFile import is_openmm_AmberPrmtopFile
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

    tmp_item = item.topology

    return tmp_item

