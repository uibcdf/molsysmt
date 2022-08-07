from ...exceptions import ArgumentError
from ...variables import is_all

def digest_component_id(component_id, caller=None):
    """Checks if `component_id` has the expected type and value.

    Parameters
    ----------
    component_id : Any
        The `component_id` argument for digestion.
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
        If the given `component_id` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get.get':
        if isinstance(component_id, bool):
            return component_id

    raise ArgumentError('component_id', value=component_id, caller=caller, message=None)

