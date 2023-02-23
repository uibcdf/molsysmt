#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest

form='molsysmt.MolecularMechanics'

## molecular mechanics

@digest(form=form)
def get_forcefield_from_system(item):          

    return item.forcefield

