from molsysmt._private.smonitor import CATALOG
from ._emit import message_from_catalog

class NotDigestedArgumentWarning(Warning):

    def __init__(self, argument):

        default_message = f"The {argument} argument was not digested."

        full_message = message_from_catalog(
            CATALOG["warnings"]["NotDigestedArgumentWarning"],
            extra={"argument": argument},
            default_message=default_message,
        )

        super().__init__(full_message)
