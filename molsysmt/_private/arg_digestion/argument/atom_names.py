from ...exceptions import ArgumentError
from ...variables import is_all
import numpy as np

def digest_atom_names(atom_names, caller=None):
    """ Checks if atom_names has the expected type and value.

    Parameters
    ----------
    indices : str or int or list or tuple or range.
        The indices

    caller: str, optional
        Name of the function or method that is being digested.
        For debugging purposes.

    Returns
    -------
    str or ndarray or None
        Either None, 'all' or an numpy array of integers with the indices.

    Raises
    -------
    ArgumentError
        If the given indices are not of the correct type.
    """

    if atom_names is None:
        return None
    elif is_all(atom_names):
        return 'all'
    elif isinstance(atom_names, str):
        return [atom_names]
    elif isinstance(atom_names, (np.ndarray, list, tuple, range)):
        if all(isinstance(ii, str) for ii in atom_names):
            if isinstance(atom_names, np.ndarray):
                return atom_names.tolist()
            elif isinstance(atom_names, list):
                return atom_names
            else:
                return list(atom_names)
        else:
            return [digest_atom_names(ii) for ii in atom_names]

    raise ArgumentError('atom_names', caller=caller, message=None)

