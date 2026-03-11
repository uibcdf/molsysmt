from molsysmt._private.smonitor import ArgumentError
from ...variables import is_all
import numpy as np
from argdigest.core.caller import caller_matches, caller_startswith

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        )

def digest_entity_id(entity_id, caller=None):
    """Checks if `entity_id` has the expected type and value.

    Parameters
    ----------
    entity_id : Any
        The `entity_id` argument for digestion.
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
        If the given `entity_id` has not of the correct type or value.
    """

    if entity_id is None and caller_matches(caller, 'add_entity'):
        return None
    if caller_matches(caller, 'add_entity'):
        if isinstance(entity_id, (int, np.int64, str)):
            return entity_id

    if caller is not None:

        if caller.endswith(functions_with_boolean):
            if isinstance(entity_id, bool):
                return entity_id
        elif caller_startswith(caller, 'molsysmt.form.') and caller.count('.to_')==2:
            return entity_id

    if isinstance(entity_id, (int, np.int64)):
        return [entity_id]

    elif isinstance(entity_id, list):
        return entity_id

    elif isinstance(entity_id, tuple):
        return list(entity_id)

    elif isinstance(entity_id, np.ndarray):
        return entity_id.tolist()

    raise ArgumentError('entity_id', value=entity_id, caller=caller, message=None)
