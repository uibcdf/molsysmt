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

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )

        try:
            emit_from_catalog(
                CATALOG["exceptions"]["IteratorError"],
                package_root=PACKAGE_ROOT,
                extra=with_meta({"caller": caller}),
            )
        except Exception:
            pass
