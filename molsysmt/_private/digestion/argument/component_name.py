from ...exceptions import ArgumentError
from ...variables import is_all

def digest_component_name(component_name, caller=None):
    """Checks if `component_name` has the expected type and value.

    Parameters
    ----------
    component_name : Any
        The `component_name` argument for digestion.
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
        If the given `component_name` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(component_name, bool):
            return component_name

    raise ArgumentError('component_name', caller=caller, message=None)

