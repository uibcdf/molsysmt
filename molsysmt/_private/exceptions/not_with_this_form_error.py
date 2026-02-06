from ..functions import caller_name
from molsysmt._private.smonitor import CATALOG
from ._emit import message_from_catalog

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

        full_message = message_from_catalog(
            CATALOG["exceptions"]["NotWithThisFormError"],
            extra={"caller": caller},
            default_message="",
        )

        # Legacy message composition replaced by smonitor catalog
        super().__init__(full_message)
