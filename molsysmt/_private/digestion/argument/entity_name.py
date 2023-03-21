from ...exceptions import ArgumentError
from ...variables import is_all

def digest_entity_name(entity_name, caller=None):
    """Checks if `entity_name` has the expected type and value.

    Parameters
    ----------
    entity_name : Any
        The `entity_name` argument for digestion.
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
        If the given `entity_name` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get.get':
        if isinstance(entity_name, bool):
            return entity_name
    elif isinstance(entity_name, str):
        return entity_name
    elif caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return entity_name

    raise ArgumentError('entity_name', value=entity_name, caller=caller, message=None)

