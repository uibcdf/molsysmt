from ..functions import caller_name
from molsysmt._private.smonitor import CATALOG
from ._emit import message_from_catalog

class NotImplementedMethodError(Exception):

    def __init__(self, method=None, arguments=None, caller=None, message=None):

        if not caller:
            caller = caller_name()

        default_message = "This method was not implemented yet."
        if message:
            default_message += message

        full_message = message_from_catalog(
            CATALOG["exceptions"]["NotImplementedMethodError"],
            extra={"caller": caller},
            default_message=default_message,
        )

        super().__init__(full_message)

        # Legacy message composition replaced by smonitor catalog
