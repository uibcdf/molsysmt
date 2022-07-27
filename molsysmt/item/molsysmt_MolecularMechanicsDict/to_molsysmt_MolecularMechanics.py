from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_molsysmt_MolecularMechanics(item):

    if check:

        digest_item('molsysmt.MolecularMechanicsDict')

    from molsysmt.native.molecular_mechanics import MolecularMechanics as molsysmt_MolecularMechanics

    tmp_item = molsysmt_MolecularMechanics(**item)

    return tmp_item

