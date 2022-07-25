from ...exceptions import ArgumentError
from ...variables import is_all

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
        Either True or False when caller is `molsysmt.basic.get`.

    Raises
    -------
    ArgumentError
        If the given `entity_index` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(entity_index, bool):
            return entity_index

    raise ArgumentError('entity_index', caller=caller, message=None)

