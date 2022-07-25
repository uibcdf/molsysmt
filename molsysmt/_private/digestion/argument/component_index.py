from ...exceptions import ArgumentError
from ...variables import is_all

def digest_component_index(component_index, caller=None):
    """Checks if `component_index` has the expected type and value.

    Parameters
    ----------
    component_index : Any
        The `component_index` argument for digestion.
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
        If the given `component_index` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(component_index, bool):
            return component_index

    raise ArgumentError('component_index', caller=caller, message=None)

