from ..functions import caller_name
from ..webs import github_issues, api_doc
from smonitor.integrations import emit_from_catalog, merge_extra
from molsysmt._private.smonitor import CATALOG, PACKAGE_ROOT, META

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

        full_message = f"Error in {caller} due to the {argument} argument with value {value}."

        if message:
            full_message += message


        # Legacy message composition replaced by smonitor catalog

        try:
            event = emit_from_catalog(
                CATALOG["exceptions"]["ArgumentError"],
                package_root=PACKAGE_ROOT,
                extra=merge_extra(META, {
                    "argument": argument,
                    "value": value,
                    "caller": caller,
                }),
            )
            if event.get("message"):
                full_message = event["message"]
            hint = (event.get("extra") or {}).get("hint")
            if hint:
                full_message = f"{full_message} {hint}"
        except Exception:
            pass

        super().__init__(full_message)
