from ...exceptions import ArgumentError
from ...variables import is_all
import numpy as np

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        'molsysmt.basic.iterator.__init__',
        'iterators.__init__',
        )

def digest_bond_id(bond_id, caller=None):
    """Checks if `bond_id` has the expected type and value.

    Parameters
    ----------
    bond_id : Any
        The `bond_id` argument for digestion.
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
        If the given `bond_id` has not of the correct type or value.
    """

    if caller is not None:
        if caller.endswith(functions_with_boolean):
            if isinstance(bond_id, bool):
                return bond_id
            else:
                raise ArgumentError('bond_id', value=bond_id, caller=caller, message=None)

    if isinstance(bond_id, (int, np.int64)):
        return [bond_id]

    elif isinstance(bond_id, list):
        return bond_id

    elif isinstance(bond_id, tuple):
        return list(bond_id)

    if isinstance(bond_id, np.ndarray):
        return bond_id.tolist()

    raise ArgumentError('bond_id', value=bond_id, caller=caller, message=None)

