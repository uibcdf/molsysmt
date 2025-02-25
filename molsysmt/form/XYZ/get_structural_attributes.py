#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np
import types

form='XYZ'


## From atom

@digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    from . import get_rank_3_XYZ

    tmp_coordinates = get_rank_3_XYZ(item)

    if not is_all(indices):
        tmp_coordinates = tmp_coordinates[:,indices,:]

    if not is_all(structure_indices):
        tmp_coordinates = tmp_coordinates[structure_indices,:,:]

    return tmp_coordinates

## From group

## From component

## From molecule

## From chain

## From entity

## From system

def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):

        from . import get_rank_3_XYZ

        tmp_coordinates = get_rank_3_XYZ(item)

        return tmp_coordinates.shape[0]

    else:
        
        return len(structure_indices)

## From bond

# List of functions to be imported

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]


