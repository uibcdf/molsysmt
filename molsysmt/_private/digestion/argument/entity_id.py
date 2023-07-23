from ...exceptions import ArgumentError
from ...variables import is_all
from numpy import ndarray

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

    if caller is not None:

        if caller.endswith(functions_with_boolean):
            if isinstance(entity_id, bool):
                return entity_id
        elif caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
            return entity_id
        elif '.set.set' in caller:
            if isinstance(entity_id, (int, str, list, tuple, ndarray)):
                return entity_id

        raise ArgumentError('entity_id', value=entity_id, caller=caller, message=None)

    raise ArgumentError('entity_id', value=entity_id, caller=caller, message=None)

