from molsysmt._private.smonitor import ArgumentError
from ...variables import is_all
import numpy as np
from argdigest.core.caller import caller_matches, caller_startswith


functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        )


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
        Either True or False when caller is `get`.

    Raises
    -------
    ArgumentError
        If the given `molecule_id` has not of the correct type or value.
    """

    if molecule_id is None and caller_matches(caller, 'add_molecule'):
        return None
    if caller_matches(caller, 'add_molecule'):
        if isinstance(molecule_id, (int, np.int64, str)):
            return molecule_id

    if caller is not None:
        if caller.endswith(functions_with_boolean):
            if isinstance(molecule_id, bool):
                return molecule_id
        elif caller_startswith(caller, 'molsysmt.form.') and caller.count('.to_')==2:
            return molecule_id

    if isinstance(molecule_id, (int, np.int64)):
        return [molecule_id]

    elif isinstance(molecule_id, list):
        return molecule_id

    elif isinstance(molecule_id, tuple):
        return list(molecule_id)

    elif isinstance(molecule_id, np.ndarray):
        return molecule_id.tolist()

    raise ArgumentError('molecule_id', value=molecule_id, caller=caller, message=None)
