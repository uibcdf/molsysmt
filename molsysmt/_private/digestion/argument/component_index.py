from ...exceptions import ArgumentError
from ...variables import is_all
import numpy as np

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        'molsysmt.basic.iterator.__init__',
        'iterators.__init__',
        )

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
        Either True or False when caller is `get`.

    Raises
    -------
    ArgumentError
        If the given `component_index` has not of the correct type or value.
    """

    if caller is not None:
        if caller.endswith(functions_with_boolean):
            if isinstance(component_index, bool):
                return component_index
            else:
                raise ArgumentError('component_index', value=component_index, caller=caller, message=None)

    if isinstance(component_index, (int, np.int64)):
        component_index=np.ndarray([component_index])

    if isinstance(component_index, (tuple, list)):
        component_index=np.ndarray(component_index)

    if isinstance(component_index, np.ndarray):
        return component_index

    raise ArgumentError('component_index', value=component_index, caller=caller, message=None)

