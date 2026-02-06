from ..functions import caller_name
from ..webs import github_issues, api_doc
from smonitor.integrations import emit_from_catalog, merge_extra
from molsysmt._private.smonitor import CATALOG, PACKAGE_ROOT, META

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
            event = emit_from_catalog(
                CATALOG["exceptions"]["NotCompatibleConversionError"],
                package_root=PACKAGE_ROOT,
                extra=merge_extra(META, {
                    "from_form": from_form,
                    "to_form": to_form,
                    "missing_arguments": missing_arguments,
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

        # Legacy message composition replaced by smonitor catalog
