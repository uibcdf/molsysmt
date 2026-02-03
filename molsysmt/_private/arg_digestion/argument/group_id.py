from ...exceptions import ArgumentError
from ...variables import is_all

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.compare.compare',
        'molsysmt.basic.iterator.__init__',
        'iterators.__init__',
        )

def digest_group_id(group_id, caller=None):
    """Checks if `group_id` has the expected type and value.

    Parameters
    ----------
    group_id : Any
        The `group_id` argument for digestion.
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
        If the given `group_id` has not of the correct type or value.
    """

    if caller.endswith(functions_with_boolean):
        if isinstance(group_id, bool):
            return group_id
    elif caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return group_id

    if isinstance(group_id, (int, np.int64)):
        return [group_id]

    elif isinstance(group_id, list):
        return group_id

    elif isinstance(group_id, tuple):
        return list(group_id)

    elif isinstance(group_id, np.ndarray):
        return group_id.tolist()

    raise ArgumentError('group_id', value=group_id, caller=caller, message=None)


