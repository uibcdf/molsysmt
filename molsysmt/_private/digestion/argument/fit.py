from molsysmt._private.exceptions import ArgumentError
import numpy as np

def digest_fit(fit, syntax="MolSysMT", caller=None):
    """ Checks if a given fit has the correct type and syntax

        Parameters
        ----------
        item : str or list of int
            An instance of one of the forms supported by MolSysMT.
        syntax : str, default="MolSysMT"
            Name of the syntax used in the fit.
        caller: str, optional
            Name of the function or method that is being digested.

        Raises
        ------
        WrongSelectionError or WrongSelectionSyntaxError or WrongSyntaxError
            A WrongSelectionError is raised if the fit object is not in deed a fit.
            A WrongSelectionSyntaxError is raised if the fit is not using the expected
            syntax.
            A WrongSyntaxError is raised if the syntax given is not in deed a syntax.

    """

    if caller=='molsysmt.basic.convert.convert':

        if syntax=='MolSysMT':
            if isinstance(fit, str):
                return fit
            elif isinstance(fit, (int, np.int64, np.int32)):
                return np.array([fit], dtype='int64')
            elif isinstance(fit, (np.ndarray, list, tuple, range)):
                return np.array(fit, dtype='int64')
            elif fit is None:
                return None
        else:
            if isinstance(fit, str):
                return fit
            elif isinstance(fit, (int, np.int64, np.int32)):
                return np.array([fit], dtype='int64')
            elif isinstance(fit, (np.ndarray, list, tuple, range)):
                return np.array(fit, dtype='int64')
            elif fit is None:
                return None

    raise ArgumentError('fit', value=fit, caller=caller, message=None)

