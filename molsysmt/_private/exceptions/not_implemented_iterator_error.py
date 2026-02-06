from ..functions import caller_name
from ..webs import github_issues, api_doc
from smonitor.integrations import emit_from_catalog
from molsysmt._private.smonitor import CATALOG, PACKAGE_ROOT, with_meta

class NotImplementedIteratorError(Exception):

    def __init__(self, form, caller=None, message=None):

        if not caller:
            caller = caller_name()

        full_message = f"Iterator has not been implemented for form {form}"

        if message:
            full_message += message

        try:
            emit_from_catalog(
                CATALOG["exceptions"]["NotImplementedIteratorError"],
                package_root=PACKAGE_ROOT,
                extra=with_meta({"form": form, "caller": caller}),
            )
        except Exception:
            pass

        super().__init__(full_message)

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )
