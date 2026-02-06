from ..functions import caller_name
from molsysmt._private.smonitor import CATALOG
from ._emit import message_from_catalog

class MolecularSystemNeededError(Exception):

    def __init__(self, caller=None, message=None):

        if not caller:
            caller = caller_name()

        default_message = (
            f"The function or method {caller} works over a molecular system. "
            f"Either no molecular system or multiple systems were provided."
        )
        if message:
            default_message += message

        full_message = message_from_catalog(
            CATALOG["exceptions"]["MolecularSystemNeededError"],
            extra={"caller": caller},
            default_message=default_message,
        )

        super().__init__(full_message)
