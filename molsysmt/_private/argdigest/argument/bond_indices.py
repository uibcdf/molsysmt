import numpy as np

from molsysmt._private.smonitor import ArgumentError

from ...variables import is_all


def digest_bond_indices(bond_indices, caller=None, native_topology_bonds=False):
    """Checks if bond_indices has the expected type and value.

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

    if native_topology_bonds:
        if hasattr(bond_indices, "unit") or hasattr(bond_indices, "units"):
            raise ArgumentError("bond_indices", value=bond_indices, caller=caller)
        if is_all(bond_indices):
            return "all"
        try:
            values = np.asarray(bond_indices)
            booleans = any(
                isinstance(value, (bool, np.bool_))
                for value in np.asarray(bond_indices, dtype=object).flat
            )
            if values.ndim == 0:
                values = values.reshape(1)
            if values.ndim == 1 and not len(values):
                return np.empty(0, dtype=np.int64)
            if values.ndim == 1 and values.dtype.kind in "iu" and not booleans:
                return values
        except (TypeError, ValueError):
            pass
        raise ArgumentError("bond_indices", value=bond_indices, caller=caller)

    if (
        caller == "molsysmt.chemical_states.get_rigid_fragments.get_rigid_fragments"
        and bond_indices is not None
    ):
        values = np.asarray(bond_indices, dtype=object)
        if any(isinstance(value, (bool, np.bool_)) for value in values.flat):
            raise ArgumentError("bond_indices", value=bond_indices, caller=caller)
    if bond_indices is None:
        return None
    elif is_all(bond_indices):
        return "all"
    elif isinstance(bond_indices, (int, np.int64, np.int32)):
        return np.array([bond_indices], dtype="int64")
    elif isinstance(bond_indices, (np.ndarray, list, tuple, range)):
        if all(isinstance(ii, (int, np.int64, np.int32)) for ii in bond_indices):
            return np.array(bond_indices, dtype="int64")
        else:
            return [digest_bond_indices(ii) for ii in bond_indices]

    raise ArgumentError("bond_indices", caller=caller, message=None)
