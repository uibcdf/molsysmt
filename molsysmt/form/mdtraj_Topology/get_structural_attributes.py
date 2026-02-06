#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
import numpy as np
import types


form='mdtraj.Topology'

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]

