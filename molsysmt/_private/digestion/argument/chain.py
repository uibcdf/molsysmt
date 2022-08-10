from molsysmt._private.exceptions import ArgumentError
from molsysmt._private.variables import is_all
import numpy as np

def digest_chain(chain, caller=None):

    if caller=='molsysmt.topology.get_covalent_chains.get_covalent_chains':
        if isinstance(chain, (list, tuple, np.ndarray)):
            return chain

    raise ArgumentError('chain', value=chain, caller=caller, message=None)
