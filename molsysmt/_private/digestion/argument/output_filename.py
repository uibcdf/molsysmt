from ...exceptions import ArgumentError
from ...variables import is_all

def digest_output_filename(output_filename, caller=None):
    """Checks if `group_type` has the expected type and value.

    Parameters
    ----------
    group_type : Any
        The `group_type` argument for digestion.
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
        If the given `group_type` has not of the correct type or value.
    """

    if output_filename is None:
        return output_filename
    elif isinstance(output_filename, str):
        return output_filename

    raise ArgumentError('output_filename', value=output_filename, caller=caller, message=None)

