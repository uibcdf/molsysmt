from ..functions import caller_name
from molsysmt._private.smonitor import CATALOG
from ._emit import message_from_catalog

class ArgumentError(Exception):
    """Exception raised when a method, or a class, was not properly called or instantiated.

    This exception is raised when a method or a class was not properly called or instantiated.

    Parameters
    ----------
    argument : str, optional
        The name of the possible wrong input argument.

    Raises
    ------
    BadCallError
        A message is printed out with the name of the class or the method raising the exception,
        the possible wrong argument, the link to the API documentation, and the link to the
        issues board of Sabueso's GitHub repository.

    Examples
    --------
    >>> from molsysmt._private.exceptions import BadCallError
    >>> def method_name(item, a=True):
    ...    if type(a) not in [int, float]:
    ...       raise BadCallError('a')
    ...    pass

    .. admonition:: See Also
       :class: attention

        :ref:`Developer Guide > Exceptions > BadCallError <developer:exceptions:BadCallError>`

    """

    def __init__(self, argument, value=None, caller=None, message=None):

        if not caller:
            caller = caller_name()

        default_message = f"Error in {caller} due to the {argument} argument with value {value}."
        if message:
            default_message += message

        full_message = message_from_catalog(
            CATALOG["exceptions"]["ArgumentError"],
            extra={"argument": argument, "value": value, "caller": caller},
            default_message=default_message,
        )

        super().__init__(full_message)
