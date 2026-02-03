from molsysmt._private.exceptions import ArgumentError
import numpy as np

def digest_center(center, syntax="MolSysMT", caller=None):
    """ Checks if a given center has the correct type and syntax

        Parameters
        ----------
        item : str or list of int
            An instance of one of the forms supported by MolSysMT.
        syntax : str, default="MolSysMT"
            Name of the syntax used in the center.
        caller: str, optional
            Name of the function or method that is being digested.

        Raises
        ------
        WrongSelectionError or WrongSelectionSyntaxError or WrongSyntaxError
            A WrongSelectionError is raised if the center object is not in deed a center.
            A WrongSelectionSyntaxError is raised if the center is not using the expected
            syntax.
            A WrongSyntaxError is raised if the syntax given is not in deed a syntax.

    """

    if caller=='molsysmt.basic.convert.convert':

        if syntax=='MolSysMT':
            if isinstance(center, str):
                return center
            elif isinstance(center, (int, np.int64, np.int32)):
                return np.array([center], dtype='int64')
            elif isinstance(center, (np.ndarray, list, tuple, range)):
                return np.array(center, dtype='int64')
            elif center is None:
                return None
        else:
            if isinstance(center, str):
                return center
            elif isinstance(center, (int, np.int64, np.int32)):
                return np.array([center], dtype='int64')
            elif isinstance(center, (np.ndarray, list, tuple, range)):
                return np.array(center, dtype='int64')
            elif center is None:
                return None

    elif caller=='molsysmt.structure.align_principal_axes.align_principal_axes':
        if isinstance(center, bool):
            return center


    raise ArgumentError('center', value=center, caller=caller, message=None)

