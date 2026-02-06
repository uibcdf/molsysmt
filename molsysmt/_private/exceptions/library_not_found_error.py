from ..functions import caller_name
from ..webs import github_issues, api_doc
from smonitor.integrations import emit_from_catalog, merge_extra
from molsysmt._private.smonitor import CATALOG, PACKAGE_ROOT, META

class LibraryNotFoundError(Exception):
    """ Exception raised when a library required by the user is not found.

        Some libraries are not considered as dependencies by MolSysMT. These libraries are required if
        the user choose to execute a method with a not default engine. In this case, the user hat to
        install it previous. It that's not the case, the method will raise these exceptions suggesting
        the manual installation.
    """

    def __init__(self, library, caller=None, message=None):

        if not caller:
            caller = caller_name()

        full_message = f"The python library {library} was not found. "

        if message:
            full_message += message

        # Legacy message composition replaced by smonitor catalog

        try:
            event = emit_from_catalog(
                CATALOG["exceptions"]["LibraryNotFoundError"],
                package_root=PACKAGE_ROOT,
                extra=merge_extra(META, {"library": library, "caller": caller}),
            )
            if event.get("message"):
                full_message = event["message"]
            hint = (event.get("extra") or {}).get("hint")
            if hint:
                full_message = f"{full_message} {hint}"
        except Exception:
            pass
