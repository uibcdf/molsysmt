from ..functions import caller_name
from ..webs import github_issues, api_doc
from smonitor.integrations import emit_from_catalog
from molsysmt._private.smonitor import CATALOG, PACKAGE_ROOT, with_meta

class NotWithThisFormError(Exception):
    """ Exception raised when a method or a class can not accept a specific item's form -by no means-.

        This exception is raised when a method or a class should be able to work with an item's form,
        but it has not been implemented yet. For instance, the method used to get the value of the
        dihedral angle defined by four atoms can not work over a GROMACS topology file (.top). In this
        case the method will raise a 'NotWithTisFormError' exception.
    """

    def __init__(self, caller=None, message=None):

        if not caller:
            caller = caller_name()

        full_message = f""

        try:
            emit_from_catalog(
                CATALOG["exceptions"]["NotWithThisFormError"],
                package_root=PACKAGE_ROOT,
                extra=with_meta({"caller": caller}),
            )
        except Exception:
            pass

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )
        super().__init__(full_message)
