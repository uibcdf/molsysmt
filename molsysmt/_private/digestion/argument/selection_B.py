from molsysmt._private.exceptions import ArgumentError
import numpy as np

def digest_selection_B(selection_B, syntax="MolSysMT", caller=None):
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
        if isinstance(selection_B, str):
            return selection_B
        elif isinstance(selection_B, (int, np.int64, np.int32)):
            return np.array([selection_B], dtype='int64')
        elif isinstance(selection_B, (np.ndarray, list, tuple, range)):
            return np.array(selection_B, dtype='int64')
    else:
        if isinstance(selection_B, str):
            return selection_B
        elif isinstance(selection_B, (int, np.int64, np.int32)):
            return np.array([selection_B], dtype='int64')
        elif isinstance(selection_B, (np.ndarray, list, tuple, range)):
            return np.array(selection_B, dtype='int64')

    raise ArgumentError('selection_B', value=selection_B, caller=caller, message=None)

