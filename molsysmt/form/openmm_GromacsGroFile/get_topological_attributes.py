#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.smonitor import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='openmm.GromacsGroFile'

@arg_digest(form=form)
def get_n_atoms_from_system(item, structure_indices='all', skip_digestion=False):

    return len(item.atomNames)

@arg_digest(form=form)
def get_n_groups_from_system(item, structure_indices='all', skip_digestion=False):

    n = 0
    prev = None
    for resid, resname in zip(item.residueIds, item.residueNames):
        curr = (resid, resname)
        if curr != prev:
            n += 1
            prev = curr
    return n

# List of functions to be imported
import types
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
