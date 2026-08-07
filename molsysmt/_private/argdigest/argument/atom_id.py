from molsysmt._private.smonitor import ArgumentError
from ...variables import is_all
import numpy as np
from argdigest.core.caller import caller_matches, caller_startswith

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        )

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
        Either True or False when caller is `get`.

    Raises
    -------
    ArgumentError
        If the given `atom_id` has not of the correct type or value.
    """

    if atom_id is None and caller_matches(caller, 'add_atom'):
        return None
    if caller_matches(caller, 'add_atom'):
        if isinstance(atom_id, (int, np.int64, str)):
            return atom_id

    if is_all(atom_id):
        return 'all'

    if caller is not None:

        if caller.endswith(functions_with_boolean):
            if isinstance(atom_id, bool):
                return atom_id
        elif caller_startswith(caller, 'molsysmt.form.') and caller.count('.to_')==2:
            return atom_id

    if isinstance(atom_id, (int, np.int64)):
        return [atom_id]

    elif isinstance(atom_id, list):
        return atom_id

    elif isinstance(atom_id, tuple):
        return list(atom_id)

    elif isinstance(atom_id, np.ndarray):
        return atom_id.tolist()

    raise ArgumentError('atom_id', value=atom_id, caller=caller, message=None)
