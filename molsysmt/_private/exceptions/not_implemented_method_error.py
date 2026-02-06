from ..functions import caller_name
from ..webs import github_issues, api_doc
from smonitor.integrations import emit_from_catalog, merge_extra
from molsysmt._private.smonitor import CATALOG, PACKAGE_ROOT, META

class NotImplementedMethodError(Exception):

    def __init__(self, method=None, arguments=None, caller=None, message=None):

        if not caller:
            caller = caller_name()

        full_message = f"This method was not implemented yet."

        if message:
            full_message += message

        try:
            event = emit_from_catalog(
                CATALOG["exceptions"]["NotImplementedMethodError"],
                package_root=PACKAGE_ROOT,
                extra=merge_extra(META, {"caller": caller}),
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
