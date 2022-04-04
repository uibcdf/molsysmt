from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_molsysmt_MolecularMechanicsDict import is_molsysmt_MolecularMechanicsDict

def to_molsysmt_MolecularMechanics(item, check=True):

    if check:

        try:
            is_molsysmt_MolecularMechanicsDict(item)
        except:
            raise WrongFormError('molsysmt.MolecularMechanicsDict')

    from molsysmt.native.molecular_mechanics import MolecularMechanics as molsysmt_MolecularMechanics

    tmp_item = molsysmt_MolecularMechanics(**item)

    return tmp_item

