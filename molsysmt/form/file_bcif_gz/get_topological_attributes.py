#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.smonitor import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.arg_digestion import arg_digest

form='file:bcif.gz'
# List of functions to be imported
import types
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
