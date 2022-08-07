from molsysmt._private.exceptions import ArgumentError
import numpy as np

def digest_selection(selection, syntax="MolSysMT", caller=None):
    """ Checks if a given selection has the correct type and syntax

        Parameters
        ----------
        item : str or list of int
            An instance of one of the forms supported by MolSysMT.
        syntax : str, default="MolSysMT"
            Name of the syntax used in the selection.
        caller: str, optional
            Name of the function or method that is being digested.

        Raises
        ------
        WrongSelectionError or WrongSelectionSyntaxError or WrongSyntaxError
            A WrongSelectionError is raised if the selection object is not in deed a selection.
            A WrongSelectionSyntaxError is raised if the selection is not using the expected
            syntax.
            A WrongSyntaxError is raised if the syntax given is not in deed a syntax.

    """

    if syntax=='MolSysMT':
        if isinstance(selection, str):
            return selection
        elif isinstance(selection, (int, np.int64, np.int32)):
            return np.array([selection], dtype='int64')
        elif isinstance(selection, (np.ndarray, list, tuple, range)):
            return np.array(selection, dtype='int64')
    else:
        if isinstance(selection, str):
            return selection
        elif isinstance(selection, (int, np.int64, np.int32)):
            return np.array([selection], dtype='int64')
        elif isinstance(selection, (np.ndarray, list, tuple, range)):
            return np.array(selection, dtype='int64')

    raise ArgumentError('selection', value=selection, caller=caller, message=None)

