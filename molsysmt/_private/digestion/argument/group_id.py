from ...exceptions import ArgumentError
from ...variables import is_all

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
        Either True or False when caller is `molsysmt.basic.get`.

    Raises
    -------
    ArgumentError
        If the given `group_id` has not of the correct type or value.
    """

    if caller=='molsysmt.basic.get':
        if is_instance(group_id, bool):
            return group_id

    raise ArgumentError('group_id', caller=caller, message=None)

