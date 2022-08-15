from ...exceptions import ArgumentError
from ...variables import is_all

def digest_molecule_indices(molecule_indices, caller):
    """ Checks if molecule_indices has the expected type and value.

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

    if molecule_indices is None:
        return None
    elif is_all(molecule_indices):
        return 'all'
    elif isinstance(molecule_indices, (int, np.int64, np.int32)):
        return np.array([molecule_indices], dtype='int64')
    elif isinstance(molecule_indices, (np.ndarray, list, tuple, range)):
        return np.array(molecule_indices, dtype='int64')

    raise ArgumentError('molecule_indices', value=molecule_indices, caller=caller, message=None)

