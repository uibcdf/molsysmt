from ..functions import caller_name
from ..webs import github_issues, api_doc
from smonitor.integrations import emit_from_catalog
from molsysmt._private.smonitor import CATALOG, PACKAGE_ROOT, with_meta

class NotImplementedMethodError(Exception):

    def __init__(self, method=None, arguments=None, caller=None, message=None):

        if not caller:
            caller = caller_name()

        full_message = f"This method was not implemented yet."

        if message:
            full_message += message

        try:
            emit_from_catalog(
                CATALOG["exceptions"]["NotImplementedMethodError"],
                package_root=PACKAGE_ROOT,
                extra=with_meta({"caller": caller}),
            )
        except Exception:
            pass

        super().__init__(full_message)

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )
