from molsysmt._private.exceptions import ArgumentError
import numpy as np

def digest_mask(mask, caller=None):

    from molsysmt.syntax.syntaxes import lowercase_syntaxes

    if caller=='select':

        if mask is None:
            return mask
        elif isinstance(to_syntax, (list, tuple, np.ndarray)):
            return mask
        else:
            raise ArgumentError('mask', caller=caller, message=None)

    else:

        if mask is None:
            return mask
        elif isinstance(to_syntax, (list, tuple, np.ndarray)):
            return mask
        else:
            raise ArgumentError('mask', caller=caller, message=None)




