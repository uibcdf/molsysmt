from ..webs import github_issues, api_doc
from smonitor.integrations import emit_from_catalog
from molsysmt._private.smonitor import CATALOG, PACKAGE_ROOT, with_meta

class NotDigestedArgumentWarning(Warning):

    def __init__(self, argument):

        full_message = f"The {argument} argument was not digested."

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )

        try:
            emit_from_catalog(
                CATALOG["warnings"]["NotDigestedArgumentWarning"],
                package_root=PACKAGE_ROOT,
                extra=with_meta({"argument": argument}),
            )
        except Exception:
            pass

        super().__init__(full_message)
