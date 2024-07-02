from ...exceptions import ArgumentError
from ...variables import is_all

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        'molsysmt.basic.iterator.__init__',
        'iterators.__init__',
        )

def digest_group_name(group_name, caller=None):
    """Checks if `group_name` has the expected type and value.

    Parameters
    ----------
    group_name : Any
        The `group_name` argument for digestion.
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
        If the given `group_name` has not of the correct type or value.
    """

    if caller.endswith(functions_with_boolean):
        if isinstance(group_name, bool):
            return group_name
    elif caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return group_name

    if isinstance(group_name, str):
        return group_name

    elif isinstance(group_name, list):
        return group_name

    elif isinstance(group_name, tuple):
        return list(group_name)

    if isinstance(group_name, np.ndarray):
        return group_name.tolist()

    raise ArgumentError('group_name', value=group_name, caller=caller, message=None)
