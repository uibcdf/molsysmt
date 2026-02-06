from ..functions import caller_name
from ..webs import github_issues, api_doc
from smonitor.integrations import emit_from_catalog
from molsysmt._private.smonitor import CATALOG, PACKAGE_ROOT, with_meta

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

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )

        try:
            emit_from_catalog(
                CATALOG["exceptions"]["LibraryNotFoundError"],
                package_root=PACKAGE_ROOT,
                extra=with_meta({"library": library, "caller": caller}),
            )
        except Exception:
            pass
