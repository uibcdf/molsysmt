from ..functions import caller_name
from ..webs import github_issues, api_doc
from smonitor.integrations import emit_from_catalog
from molsysmt._private.smonitor import CATALOG, PACKAGE_ROOT, with_meta

class NotCompatibleConversionError(Exception):

    def __init__(self, from_form, to_form, missing_arguments, caller=None, message=None):

        if not caller:
            caller = caller_name()

        full_message = (
                f"Error in conversion from {from_form} to {to_form}. "
                f"The following input attributes of arguments are missing: {missing_arguments}."
                )

        if message:
            full_message += message

        try:
            emit_from_catalog(
                CATALOG["exceptions"]["NotCompatibleConversionError"],
                package_root=PACKAGE_ROOT,
                extra=with_meta({
                    "from_form": from_form,
                    "to_form": to_form,
                    "missing_arguments": missing_arguments,
                    "caller": caller,
                }),
            )
        except Exception:
            pass

        super().__init__(full_message)

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
            )
