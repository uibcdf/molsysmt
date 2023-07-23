from ...exceptions import ArgumentError
from ...variables import is_all
from numpy import ndarray

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        )


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
        Either True or False when caller is `get`.

    Raises
    -------
    ArgumentError
        If the given `component_name` has not of the correct type or value.
    """

    if caller is not None:

        if caller.endswith(functions_with_boolean):
            if isinstance(component_name, bool):
                return component_name
        elif caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
            return component_name
        elif '.set.set' in caller:
            if isinstance(component_name, (int, str, list, tuple, ndarray)):
                return component_name

        raise ArgumentError('component_name', value=component_name, caller=caller, message=None)

    if isinstance(component_name, str):
            return component_name

    raise ArgumentError('component_name', value=component_name, caller=caller, message=None)

