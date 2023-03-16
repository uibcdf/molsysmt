from ...exceptions import ArgumentError
from ...variables import is_all

def digest_component_type(component_type, caller=None):
    """Checks if `component_type` has the expected type and value.

    Parameters
    ----------
    component_type : Any
        The `component_type` argument for digestion.
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
        If the given `component_type` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get.get':
        if isinstance(component_type, bool):
            return component_type
    elif caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return component_type

    raise ArgumentError('component_type', value=component_type, caller=caller, message=None)

