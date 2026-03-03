#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.smonitor import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
import numpy as np
import types

form='openmm.Context'


## From atom

def get_atom_index_from_atom(item, indices='all', skip_digestion=False):

    from ..openmm_System.to_openmm_System import to_openmm_System
    from ..openmm_System.get_atom_index_from_atom import get_atom_index_from_atom as aux_get

    tmp_item = to_openmm_System(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

## From group

## From component

## From molecule

## From chain

## From entity

## From system

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    return item.getSystem().getNumParticles()

## From bond


# List of functions to be imported

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]

