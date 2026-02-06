from ..webs import github_issues, api_doc
from smonitor.integrations import emit_from_catalog
from molsysmt._private.smonitor import CATALOG, PACKAGE_ROOT, with_meta

class NotDigestedArgumentWarning(Warning):

    def __init__(self, argument):

        full_message = f"The {argument} argument was not digested."

        # Legacy message composition replaced by smonitor catalog

        try:
            event = emit_from_catalog(
                CATALOG["warnings"]["NotDigestedArgumentWarning"],
                package_root=PACKAGE_ROOT,
                extra=with_meta({"argument": argument}),
            )
            if event.get("message"):
                full_message = event["message"]
            hint = (event.get("extra") or {}).get("hint")
            if hint:
                full_message = f"{full_message} {hint}"
        except Exception:
            pass

        super().__init__(full_message)
