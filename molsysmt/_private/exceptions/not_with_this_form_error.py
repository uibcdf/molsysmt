from ..functions import caller_name
from ..webs import github_issues, api_doc
from smonitor.integrations import emit_from_catalog, merge_extra
from molsysmt._private.smonitor import CATALOG, PACKAGE_ROOT, META

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
            event = emit_from_catalog(
                CATALOG["exceptions"]["NotWithThisFormError"],
                package_root=PACKAGE_ROOT,
                extra=merge_extra(META, {"caller": caller}),
            )
            if event.get("message"):
                full_message = event["message"]
            hint = (event.get("extra") or {}).get("hint")
            if hint:
                full_message = f"{full_message} {hint}"
        except Exception:
            pass

        # Legacy message composition replaced by smonitor catalog
        super().__init__(full_message)
