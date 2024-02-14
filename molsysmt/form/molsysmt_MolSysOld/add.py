from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(form='molsysmt.MolSysOld', to_form='molsysmt.MolSysOld')
def add(to_item, item, atom_indices='all', structure_indices='all'):

    to_item.add(item)

    pass

