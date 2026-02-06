from ..functions import caller_name
from molsysmt._private.smonitor import CATALOG
from ._emit import message_from_catalog

class NotSupportedFormError(Exception):

    def __init__(self, form, caller=None, message=None):

        if not caller:
            caller = caller_name()

        default_message = f"The form {form} used in {caller} is not supported by MolSysMT."
        if message:
            default_message += message

        full_message = message_from_catalog(
            CATALOG["exceptions"]["NotSupportedFormError"],
            extra={"form": form, "caller": caller},
            default_message=default_message,
        )

        super().__init__(full_message)

        # Legacy message composition replaced by smonitor catalog
