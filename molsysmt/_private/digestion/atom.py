from ..exceptions.atom import WrongAtomIndexError, WrongAtomIdError
from ..exceptions.atom import WrongAtomNameError, WrongAtomTypeError
from ..exceptions.atom import WrongAtomIndicesError
from ..variables import is_all

def digest_atom_index(atom_index, caller=None):
    """Checks if `atom_index` has the expected type and value.

    Parameters
    ----------
    atom_index : Any
        The `atom_index` argument for digestion.
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
    WrongAtomIndexError
        If the given `atom_index` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(atom_index, bool):
            return atom_index

    raise WrongAtomIndexError(atom_index, caller)

def digest_atom_id(atom_id, caller=None):
    """Checks if `atom_id` has the expected type and value.

    Parameters
    ----------
    atom_id : Any
        The `atom_id` argument for digestion.
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
    WrongAtomIdError
        If the given `atom_id` has not the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(atom_id, bool):
            return atom_id

    raise WrongAtomIdError(atom_id, caller)

def digest_atom_type(atom_type, caller):
    """Checks if `atom_type` has the expected type and value.

    Parameters
    ----------
    atom_type : Any
        The `atom_type` argument for digestion.
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
    WrongAtomTypeError
        If the given `atom_type` has not the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(atom_type, bool):
            return atom_type

    raise WrongAtomTypeError(atom_type, caller)

def digest_atom_name(atom_name, caller):
    """Checks if `atom_name` has the expected type and value.

    Parameters
    ----------
    atom_name : Any
        The `atom_name` argument for digestion.
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
    WrongAtomNameError
        If the given `atom_name` has not the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(atom_name, bool):
            return atom_name

    raise WrongAtomNameError(atom_name, caller)

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
    WrongIndicesError
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
        raise WrongAtomIndicesError(atom_indices, caller=caller)

    return atom_indices

