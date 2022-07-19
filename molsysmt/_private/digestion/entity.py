from ..exceptions.entity import WrongEntityIndexError, WrongEntityIdError
from ..exceptions.entity import WrongEntityNameError, WrongEntityTypeError
from ..exceptions.entity import WrongEntityIndicesError
from ..variables import is_all

def digest_entity_index(entity_index, caller=None):
    """Checks if `entity_index` has the expected type and value.

    Parameters
    ----------
    entity_index : Any
        The `entity_index` argument for digestion.
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
    WrongEntityIndexError
        If the given `entity_index` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(entity_index, bool):
            return entity_index

    raise WrongEntityIndexError(entity_index, caller)

def digest_entity_id(entity_id, caller=None):
    """Checks if `entity_id` has the expected type and value.

    Parameters
    ----------
    entity_id : Any
        The `entity_id` argument for digestion.
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
    WrongEntityIdError
        If the given `entity_id` has not the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(entity_id, bool):
            return entity_id

    raise WrongEntityIdError(entity_id, caller)

def digest_entity_type(entity_type, caller):
    """Checks if `entity_type` has the expected type and value.

    Parameters
    ----------
    entity_type : Any
        The `entity_type` argument for digestion.
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
    WrongEntityTypeError
        If the given `entity_type` has not the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(entity_type, bool):
            return entity_type

    raise WrongEntityTypeError(entity_type, caller)

def digest_entity_name(entity_name, caller):
    """Checks if `entity_name` has the expected type and value.

    Parameters
    ----------
    entity_name : Any
        The `entity_name` argument for digestion.
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
    WrongEntityNameError
        If the given `entity_name` has not the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(entity_name, bool):
            return entity_name

    raise WrongEntityNameError(entity_name, caller)

def digest_entity_indices(entity_indices, caller):
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

    if entity_indices is None:
        pass
    elif is_all(entity_indices):
        entity_indices = 'all'
    elif isinstance(entity_indices, (int, np.int64, np.int32)):
        indices = np.array([entity_indices], dtype='int64')
    elif isinstance(entity_indices, (np.ndarray, list, tuple, range)):
        indices = np.array(entity_indices, dtype='int64')
    else:
        raise WrongEntityIndicesError(entity_indices, caller)

    return indices

