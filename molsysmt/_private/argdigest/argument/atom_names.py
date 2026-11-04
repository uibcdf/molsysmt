import numpy as np

from molsysmt._private.smonitor import ArgumentError

from ...variables import is_all


def _flat_atom_name_list(atom_names, caller=None):
    """Return detached flat string names without nested or scalar interpretation."""
    if isinstance(atom_names, (list, tuple, np.ndarray)):
        names = np.asarray(atom_names, dtype=object)
        if names.ndim == 1 and all(isinstance(name, str) for name in names):
            return names.tolist()
    raise ArgumentError(
        "atom_names",
        value=atom_names,
        caller=caller,
        message="Supply a one-dimensional list, tuple or NumPy array of atom-name strings.",
    )


def digest_atom_names(atom_names, caller=None):
    """Checks if atom_names has the expected type and value.

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

    if atom_names is None:
        return None
    elif is_all(atom_names):
        return "all"
    elif isinstance(atom_names, str):
        return [atom_names]
    elif isinstance(atom_names, (np.ndarray, list, tuple, range)):
        if all(isinstance(ii, str) for ii in atom_names):
            if isinstance(atom_names, np.ndarray):
                return atom_names.tolist()
            elif isinstance(atom_names, list):
                return atom_names
            else:
                return list(atom_names)
        else:
            return [digest_atom_names(ii) for ii in atom_names]

    raise ArgumentError("atom_names", caller=caller, message=None)
