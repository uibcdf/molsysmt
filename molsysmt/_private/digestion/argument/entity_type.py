from ...exceptions import ArgumentError
from ...variables import is_all

def digest_entity_type(entity_type, caller=None):
    """Checks if `entity_type` has the expected type and value.

    Parameters
    ----------
    entity_type : Any
        The `entity_type` argument for digestion.
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
        If the given `entity_type` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get.get':
        if isinstance(entity_type, bool):
            return entity_type

    raise ArgumentError('entity_type', value=entity_type, caller=caller, message=None)

