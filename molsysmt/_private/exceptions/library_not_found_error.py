from ..functions import caller_name
from molsysmt._private.smonitor import CATALOG
from ._emit import message_from_catalog

class LibraryNotFoundError(Exception):
    """ Exception raised when a library required by the user is not found.

        Some libraries are not considered as dependencies by MolSysMT. These libraries are required if
        the user choose to execute a method with a not default engine. In this case, the user hat to
        install it previous. It that's not the case, the method will raise these exceptions suggesting
        the manual installation.
    """

    def __init__(self, library, caller=None, message=None):

        if not caller:
            caller = caller_name()

        default_message = f"The python library {library} was not found."
        if message:
            default_message += f" {message}"

        full_message = message_from_catalog(
            CATALOG["exceptions"]["LibraryNotFoundError"],
            extra={"library": library, "caller": caller},
            default_message=default_message,
        )
