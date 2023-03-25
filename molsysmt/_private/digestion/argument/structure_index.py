from ...exceptions import ArgumentError
from ...variables import is_all
import numpy as np

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.iterator.__init__',
        'iterators.__init__',
        )

def digest_structure_index(structure_index, caller=None):
    """Checks if `structure_index` has the expected type and value.

    Parameters
    ----------
    structure_index : Any
        The `structure_index` argument for digestion.
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
        If the given `structure_index` has not of the correct type or value.
    """

    if caller is not None:
        if caller.endswith(functions_with_boolean):
            if isinstance(structure_index, bool):
                return structure_index
            else:
                raise ArgumentError('structure_index', value=structure_index, caller=caller, message=None)

    if isinstance(structure_index, (int, np.int64)):
        structure_index=np.ndarray([structure_index])

    if isinstance(structure_index, (tuple, list)):
        structure_index=np.ndarray(structure_index)

    if isinstance(structure_index, np.ndarray):
        return structure_index

    raise ArgumentError('structure_index', value=structure_index, caller=caller, message=None)

