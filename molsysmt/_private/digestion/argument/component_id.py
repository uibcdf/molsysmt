from ...exceptions import ArgumentError
from ...variables import is_all
from numpy import ndarray

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        )


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


    if caller is not None:

        if caller.endswith(functions_with_boolean):
            if isinstance(component_id, bool):
                return component_id
        elif caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
            return component_id
        elif '.set.set' in caller:
            if isinstance(component_id, (int, list, tuple, ndarray)):
                return component_id

    raise ArgumentError('component_id', value=component_id, caller=caller, message=None)

