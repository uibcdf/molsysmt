from molsysmt.tools.openmm_Modeller.is_openmm_Modeller import is_openmm_Modeller
from molsysmt._private_tools.exceptions import WrongFormError
from molsysmt._private_tools.exceptions import NotImplementedMethodError

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_openmm_Modeller(item_1)
        except:
            raise WrongFormError('openmm.Modeller')

        try:
            is_openmm_Modeller(item_2)
        except:
            raise WrongFormError('openmm.Modeller')

    raise NotImplementedMethodError()

