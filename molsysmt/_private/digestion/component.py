from ..exceptions.component import WrongComponentIndexError, WrongComponentIdError
from ..exceptions.component import WrongComponentNameError, WrongComponentTypeError
from ..exceptions.component import WrongComponentIndicesError
from ..variables import is_all

def digest_component_index(component_index, caller=None):
    """Checks if `component_index` has the expected type and value.

    Parameters
    ----------
    component_index : Any
        The `component_index` argument for digestion.
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
    WrongComponentIndexError
        If the given `component_index` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(component_index, bool):
            return component_index

    raise WrongComponentIndexError(component_index, caller)

def digest_component_id(component_id, caller=None):
    """Checks if `component_id` has the expected type and value.

    Parameters
    ----------
    component_id : Any
        The `component_id` argument for digestion.
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
    WrongComponentIdError
        If the given `component_id` has not the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(component_id, bool):
            return component_id

    raise WrongComponentIdError(component_id, caller)

def digest_component_type(component_type, caller):
    """Checks if `component_type` has the expected type and value.

    Parameters
    ----------
    component_type : Any
        The `component_type` argument for digestion.
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
    WrongComponentTypeError
        If the given `component_type` has not the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(component_type, bool):
            return component_type

    raise WrongComponentTypeError(component_type, caller)

def digest_component_name(component_name, caller):
    """Checks if `component_name` has the expected type and value.

    Parameters
    ----------
    component_name : Any
        The `component_name` argument for digestion.
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
    WrongComponentNameError
        If the given `component_name` has not the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(component_name, bool):
            return component_name

    raise WrongComponentNameError(component_name, caller)

def digest_component_indices(component_indices, caller):
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

    if component_indices is None:
        pass
    elif is_all(component_indices):
        component_indices = 'all'
    elif isinstance(component_indices, (int, np.int64, np.int32)):
        indices = np.array([component_indices], dtype='int64')
    elif isinstance(component_indices, (np.ndarray, list, tuple, range)):
        indices = np.array(component_indices, dtype='int64')
    else:
        raise WrongComponentIndicesError(component_indices, caller)

    return indices

