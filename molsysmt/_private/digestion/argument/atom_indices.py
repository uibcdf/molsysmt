from ...exceptions import ArgumentError
from ...variables import is_all

def digest_atom_indices(atom_indices, caller):
    """ Checks if atom_indices has the expected type and value.

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

    if atom_indices is None:
        pass
    elif is_all(atom_indices):
        atom_indices = 'all'
    elif isinstance(atom_indices, (int, np.int64, np.int32)):
        atom_indices = np.array([atom_indices], dtype='int64')
    elif isinstance(atom_indices, (np.ndarray, list, tuple, range)):
        atom_indices = np.array(atom_indices, dtype='int64')
    else:
        raise ArgumentError('atom_indices', caller=caller, message=None)

    return atom_indices

