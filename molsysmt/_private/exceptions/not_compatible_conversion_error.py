from ..functions import caller_name
from molsysmt._private.smonitor import CATALOG
from ._emit import message_from_catalog

class NotCompatibleConversionError(Exception):

    def __init__(self, from_form, to_form, missing_arguments, caller=None, message=None):

        if not caller:
            caller = caller_name()

        default_message = (
            f"Error in conversion from {from_form} to {to_form}. "
            f"The following input attributes of arguments are missing: {missing_arguments}."
        )
        if message:
            default_message += message

        full_message = message_from_catalog(
            CATALOG["exceptions"]["NotCompatibleConversionError"],
            extra={
                "from_form": from_form,
                "to_form": to_form,
                "missing_arguments": missing_arguments,
                "caller": caller,
            },
            default_message=default_message,
        )

        super().__init__(full_message)

        # Legacy message composition replaced by smonitor catalog
