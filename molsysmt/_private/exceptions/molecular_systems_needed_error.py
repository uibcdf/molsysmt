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

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )

        try:
            emit_from_catalog(
                CATALOG["exceptions"]["MolecularSystemsNeededError"],
                package_root=PACKAGE_ROOT,
                extra=with_meta({"caller": caller}),
            )
        except Exception:
            pass

        super().__init__(full_message)
