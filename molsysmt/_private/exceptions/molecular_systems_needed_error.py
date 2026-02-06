from ..functions import caller_name
from molsysmt._private.smonitor import CATALOG
from ._emit import message_from_catalog

class MolecularSystemsNeededError(Exception):

    def __init__(self, caller=None, message=None):

        if not caller:
            caller = caller_name()

        default_message = (
            f"The function or method {caller} works over multiple molecular systems. "
            f"Either no molecular system or a single system was provided."
        )
        if message:
            default_message += message

        full_message = message_from_catalog(
            CATALOG["exceptions"]["MolecularSystemsNeededError"],
            extra={"caller": caller},
            default_message=default_message,
        )

        super().__init__(full_message)
