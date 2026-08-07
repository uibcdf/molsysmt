import numpy as np
from argdigest.core.caller import caller_matches
from molsysmt._private.smonitor import ArgumentError
from ...variables import is_all


def digest_structure_indices(structure_indices, molecular_systems=None, caller=None):
    """ Checks if atom_indices has the expected type and value.

    Parameters
    ----------
    structure_indices : str or int or list or tuple or range.
        The structure indices.

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
        If the given structure_indices has not of the correct type.
    """

    if molecular_systems is not None and caller_matches(
        caller,
        'merge',
        'concatenate_structures',
    ):
        from molsysmt._private.smonitor import ArgumentLengthError

        n_molecular_systems = len(molecular_systems)
        if isinstance(structure_indices, (list, tuple)):
            if len(structure_indices) != n_molecular_systems:
                raise ArgumentLengthError(
                    argument='structure_indices',
                    expected=n_molecular_systems,
                    actual=len(structure_indices),
                    caller=caller,
                )
            return [digest_structure_indices(indices) for indices in structure_indices]

        return [
            digest_structure_indices(structure_indices)
            for _ in range(n_molecular_systems)
        ]

    if structure_indices is None:
        return None
    elif is_all(structure_indices):
        return 'all'
    elif isinstance(structure_indices, (int, np.int64, np.int32)):
        return np.array([structure_indices], dtype='int64')
    elif isinstance(structure_indices, (np.ndarray, list, tuple, range)):
        if all(isinstance(ii, (int, np.int64, np.int32)) for ii in structure_indices):
            return np.array(structure_indices, dtype='int64')
        else:
            return [digest_structure_indices(ii, caller=caller) for ii in structure_indices]

    raise ArgumentError('structure_indices', caller=caller, message=None)
