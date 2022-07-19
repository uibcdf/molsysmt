from ..exceptions.chain import WrongChainIndexError, WrongChainIdError
from ..exceptions.chain import WrongChainNameError, WrongChainTypeError
from ..exceptions.chain import WrongChainIndicesError
from ..variables import is_all

def digest_chain_index(chain_index, caller=None):
    """Checks if `chain_index` has the expected type and value.

    Parameters
    ----------
    chain_index : Any
        The `chain_index` argument for digestion.
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
    WrongChainIndexError
        If the given `chain_index` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(chain_index, bool):
            return chain_index

    raise WrongChainIndexError(chain_index, caller)

def digest_chain_id(chain_id, caller=None):
    """Checks if `chain_id` has the expected type and value.

    Parameters
    ----------
    chain_id : Any
        The `chain_id` argument for digestion.
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
    WrongChainIdError
        If the given `chain_id` has not the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(chain_id, bool):
            return chain_id

    raise WrongChainIdError(chain_id, caller)

def digest_chain_type(chain_type, caller):
    """Checks if `chain_type` has the expected type and value.

    Parameters
    ----------
    chain_type : Any
        The `chain_type` argument for digestion.
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
    WrongChainTypeError
        If the given `chain_type` has not the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(chain_type, bool):
            return chain_type

    raise WrongChainTypeError(chain_type, caller)

def digest_chain_name(chain_name, caller):
    """Checks if `chain_name` has the expected type and value.

    Parameters
    ----------
    chain_name : Any
        The `chain_name` argument for digestion.
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
    WrongChainNameError
        If the given `chain_name` has not the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(chain_name, bool):
            return chain_name

    raise WrongChainNameError(chain_name, caller)

def digest_chain_indices(chain_indices, caller):
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

    if chain_indices is None:
        pass
    elif is_all(chain_indices):
        chain_indices = 'all'
    elif isinstance(chain_indices, (int, np.int64, np.int32)):
        indices = np.array([chain_indices], dtype='int64')
    elif isinstance(chain_indices, (np.ndarray, list, tuple, range)):
        indices = np.array(chain_indices, dtype='int64')
    else:
        raise WrongChainIndicesError(chain_indices, caller)

    return indices

