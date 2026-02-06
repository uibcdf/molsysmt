from ..functions import caller_name
from ..webs import github_issues, api_doc
from smonitor.integrations import emit_from_catalog
from molsysmt._private.smonitor import CATALOG, PACKAGE_ROOT, with_meta

class IteratorError(Exception):

    def __init__(self, caller=None, message=None):

        if not caller:
            caller = caller_name()

        full_message = f"An error was found in the iterator arguments. "

        if message:
            full_message += message

        # Legacy message composition replaced by smonitor catalog

        try:
            event = emit_from_catalog(
                CATALOG["exceptions"]["IteratorError"],
                package_root=PACKAGE_ROOT,
                extra=with_meta({"caller": caller}),
            )
            if event.get("message"):
                full_message = event["message"]
            hint = (event.get("extra") or {}).get("hint")
            if hint:
                full_message = f"{full_message} {hint}"
        except Exception:
            pass
