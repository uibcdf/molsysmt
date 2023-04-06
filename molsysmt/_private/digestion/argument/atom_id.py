from ...exceptions import ArgumentError
from ...variables import is_all
import numpy as np

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

    if caller is not None:

        if caller.endswith(functions_with_boolean):
            if isinstance(atom_id, bool):
                return atom_id
        elif caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
            return atom_id

        raise ArgumentError('atom_id', value=atom_id, caller=caller, message=None)

    if isinstance(atom_id, (tuple, list)):
        return np.array(atom_id)

    if isinstance(atom_id, np.ndarray):
        return atom_id

    raise ArgumentError('atom_id', value=atom_id, caller=caller, message=None)

