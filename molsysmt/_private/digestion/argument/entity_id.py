from ...exceptions import ArgumentError
from ...variables import is_all

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
        Either True or False when caller is `molsysmt.basic.get`.

    Raises
    -------
    ArgumentError
        If the given `entity_id` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(entity_id, bool):
            return entity_id

    raise ArgumentError('entity_id', caller=caller, message=None)

