from ..functions import caller_name
from ..webs import github_issues, api_doc
from smonitor.integrations import emit_from_catalog
from molsysmt._private.smonitor import CATALOG, PACKAGE_ROOT, with_meta

class MolecularSystemsNeededError(Exception):

    def __init__(self, caller=None, message=None):

        if not caller:
            caller = caller_name()

        full_message = (f"The function or method {caller} works over multiple molecular systems. "
                       f"Either no molecular system or a single system was provided.")

        if message:
            full_message += message

        # Legacy message composition replaced by smonitor catalog

        try:
            event = emit_from_catalog(
                CATALOG["exceptions"]["MolecularSystemsNeededError"],
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

        super().__init__(full_message)
