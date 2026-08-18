#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.smonitor import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
import numpy as np
import types


form='openmm.System'

## From atom

@arg_digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting atom index from atom in form openmm.System.

    Parameters
    ----------
    item : openmm.System
        Source item in openmm.System form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
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

    """
    Getting n atoms from system in form openmm.System.

    Parameters
    ----------
    item : openmm.System
        Source item in openmm.System form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return item.getNumParticles()

## From bond

# List of functions to be imported

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]

