from ...exceptions import ArgumentError
from ...variables import is_all

def digest_component_indices(component_indices, caller):
    """ Checks if component_indices has the expected type and value.

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

    if component_indices is None:
        pass
    elif is_all(component_indices):
        component_indices = 'all'
    elif isinstance(component_indices, (int, np.int64, np.int32)):
        component_indices = np.array([component_indices], dtype='int64')
    elif isinstance(component_indices, (np.ndarray, list, tuple, range)):
        component_indices = np.array(component_indices, dtype='int64')
    else:
        raise ArgumentError('component_indices', caller=caller, message=None)

    return component_indices

