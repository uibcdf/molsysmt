from ..functions import caller_name
from molsysmt._private.smonitor import CATALOG
from ._emit import message_from_catalog

class IteratorError(Exception):

    def __init__(self, caller=None, message=None):

        if not caller:
            caller = caller_name()

        default_message = "An error was found in the iterator arguments."
        if message:
            default_message += f" {message}"

        full_message = message_from_catalog(
            CATALOG["exceptions"]["IteratorError"],
            extra={"caller": caller},
            default_message=default_message,
        )
