from ..functions import caller_name
from ..webs import github_issues, api_doc

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

        :ref:`Developer Guide \> Exceptions \> BadCallError <developer:exceptions:BadCallError>`

    """

    def __init__(self, argument, value=None, caller=None, message=None):

        if not caller:
            caller = caller_name()

        full_message = f"Error in {caller} due to the {argument} argument with value {value}."

        if message:
            full_message += message


        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )

        super().__init__(full_message)

