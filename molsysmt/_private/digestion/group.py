from ..exceptions import WrongGroupIndexError, WrongGroupIdError
from ..exceptions import WrongGroupNameError, WrongGroupTypeError
from ..exceptions import WrongGroupIndicesError
from ..variables import is_all

def digest_group_index(group_index, caller=None):
    """Checks if `group_index` has the expected type and value.

    Parameters
    ----------
    group_index : Any
        The `group_index` argument for digestion.
    caller: str, optional
        Name of the function or method that is being digested.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/#the-any-type

    Returns
    -------
    bool
        Either True or False when caller is `molsysmt.basic.get`.

    Raises
    -------
    WrongGroupIndexError
        If the given `group_index` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(group_index, bool):
            return group_index

    raise WrongGroupIndexError(group_index, caller)

def digest_group_id(group_id, caller=None):
    """Checks if `group_id` has the expected type and value.

    Parameters
    ----------
    group_id : Any
        The `group_id` argument for digestion.
    caller: str, optional
        Name of the function or method that is being digested.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/#the-any-type

    Returns
    -------
    bool
        Either True or False when caller is `molsysmt.basic.get`.

    Raises
    -------
    WrongGroupIdError
        If the given `group_id` has not the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(group_id, bool):
            return group_id

    raise WrongGroupIdError(group_id, caller)

def digest_group_type(group_type, caller):
    """Checks if `group_type` has the expected type and value.

    Parameters
    ----------
    group_type : Any
        The `group_type` argument for digestion.
    caller: str, optional
        Name of the function or method that is being digested.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/#the-any-type

    Returns
    -------
    bool
        Either True or False when caller is `molsysmt.basic.get`.

    Raises
    -------
    WrongGroupTypeError
        If the given `group_type` has not the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(group_type, bool):
            return group_type

    raise WrongGroupTypeError(group_type, caller)

def digest_group_name(group_name, caller):
    """Checks if `group_name` has the expected type and value.

    Parameters
    ----------
    group_name : Any
        The `group_name` argument for digestion.
    caller: str, optional
        Name of the function or method that is being digested.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/#the-any-type

    Returns
    -------
    bool
        Either True or False when caller is `molsysmt.basic.get`.

    Raises
    -------
    WrongGroupNameError
        If the given `group_name` has not the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(group_name, bool):
            return group_name

    raise WrongGroupNameError(group_name, caller)

def digest_group_indices(group_indices, caller):
    """ Checks if indices are of the expected type and value.

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
        WrongIndicesError
            If the given indices are not of the correct type.
    """

    if group_indices is None:
        pass
    elif is_all(group_indices):
        group_indices = 'all'
    elif isinstance(group_indices, (int, np.int64, np.int32)):
        indices = np.array([group_indices], dtype='int64')
    elif isinstance(group_indices, (np.ndarray, list, tuple, range)):
        indices = np.array(group_indices, dtype='int64')
    else:
        raise WrongGroupIndicesError(group_indices, caller)

    return indices

