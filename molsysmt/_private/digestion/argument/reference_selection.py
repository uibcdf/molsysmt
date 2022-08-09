from molsysmt._private.exceptions import ArgumentError
import numpy as np

def digest_reference_selection(reference_selection, syntax="MolSysMT", caller=None):
    """ Checks if a given reference_selection has the correct type and syntax

        Parameters
        ----------
        item : str or list of int
            An instance of one of the forms supported by MolSysMT.
        syntax : str, default="MolSysMT"
            Name of the syntax used in the reference_selection.
        caller: str, optional
            Name of the function or method that is being digested.

        Raises
        ------
        WrongSelectionError or WrongSelectionSyntaxError or WrongSyntaxError
            A WrongSelectionError is raised if the reference_selection object is not in deed a reference_selection.
            A WrongSelectionSyntaxError is raised if the reference_selection is not using the expected
            syntax.
            A WrongSyntaxError is raised if the syntax given is not in deed a syntax.

    """

    if syntax=='MolSysMT':
        if isinstance(reference_selection, str):
            return reference_selection
        elif isinstance(reference_selection, (int, np.int64, np.int32)):
            return np.array([reference_selection], dtype='int64')
        elif isinstance(reference_selection, (np.ndarray, list, tuple, range)):
            return np.array(reference_selection, dtype='int64')
        elif reference_selection is None:
            return None
    else:
        if isinstance(reference_selection, str):
            return reference_selection
        elif isinstance(reference_selection, (int, np.int64, np.int32)):
            return np.array([reference_selection], dtype='int64')
        elif isinstance(reference_selection, (np.ndarray, list, tuple, range)):
            return np.array(reference_selection, dtype='int64')
        elif reference_selection is None:
            return None

    raise ArgumentError('reference_selection', value=reference_selection, caller=caller, message=None)

