from ..exceptions import WrongMoleculeIndexError, WrongMoleculeIdError
from ..exceptions import WrongMoleculeNameError, WrongMoleculeTypeError
from ..exceptions import WrongMoleculeIndicesError
from ..variables import is_all

def digest_molecule_index(molecule_index, caller=None):
    """Checks if `molecule_index` has the expected type and value.

    Parameters
    ----------
    molecule_index : Any
        The `molecule_index` argument for digestion.
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
    WrongMoleculeIndexError
        If the given `molecule_index` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(molecule_index, bool):
            return molecule_index

    raise WrongMoleculeIndexError(molecule_index, caller)

def digest_molecule_id(molecule_id, caller=None):
    """Checks if `molecule_id` has the expected type and value.

    Parameters
    ----------
    molecule_id : Any
        The `molecule_id` argument for digestion.
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
    WrongMoleculeIdError
        If the given `molecule_id` has not the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(molecule_id, bool):
            return molecule_id

    raise WrongMoleculeIdError(molecule_id, caller)

def digest_molecule_type(molecule_type, caller):
    """Checks if `molecule_type` has the expected type and value.

    Parameters
    ----------
    molecule_type : Any
        The `molecule_type` argument for digestion.
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
    WrongMoleculeTypeError
        If the given `molecule_type` has not the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(molecule_type, bool):
            return molecule_type

    raise WrongMoleculeTypeError(molecule_type, caller)

def digest_molecule_name(molecule_name, caller):
    """Checks if `molecule_name` has the expected type and value.

    Parameters
    ----------
    molecule_name : Any
        The `molecule_name` argument for digestion.
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
    WrongMoleculeNameError
        If the given `molecule_name` has not the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(molecule_name, bool):
            return molecule_name

    raise WrongMoleculeNameError(molecule_name, caller)

def digest_molecule_indices(molecule_indices, caller):
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

    if molecule_indices is None:
        pass
    elif is_all(molecule_indices):
        molecule_indices = 'all'
    elif isinstance(molecule_indices, (int, np.int64, np.int32)):
        indices = np.array([molecule_indices], dtype='int64')
    elif isinstance(molecule_indices, (np.ndarray, list, tuple, range)):
        indices = np.array(molecule_indices, dtype='int64')
    else:
        raise WrongMoleculeIndicesError(molecule_indices, caller)

    return indices

