#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
import numpy as np
import types


form='openmm.System'

## From atom

@arg_digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_aux = get_n_atoms_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output

## From group

## From component

## From molecule

## From chain

## From entity

## From system

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    return item.getNumParticles()

## From bond

# List of functions to be imported

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]

