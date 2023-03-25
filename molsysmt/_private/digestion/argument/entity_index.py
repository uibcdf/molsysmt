from ...exceptions import ArgumentError
from ...variables import is_all
import numpy as np

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.iterator.__init__',
        'iterators.__init__',
        )

def digest_entity_index(entity_index, caller=None):
    """Checks if `entity_index` has the expected type and value.

    Parameters
    ----------
    entity_index : Any
        The `entity_index` argument for digestion.
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
        If the given `entity_index` has not of the correct type or value.
    """

    if caller is not None:
        if caller.endswith(functions_with_boolean):
            if isinstance(entity_index, bool):
                return entity_index
            else:
                raise ArgumentError('entity_index', value=entity_index, caller=caller, message=None)

    if isinstance(entity_index, (int, np.int64)):
        entity_index=np.ndarray([entity_index])

    if isinstance(entity_index, (tuple, list)):
        entity_index=np.ndarray(entity_index)

    if isinstance(entity_index, np.ndarray):
        return entity_index

    raise ArgumentError('entity_index', value=entity_index, caller=caller, message=None)

