from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='openmm.State'

###### Set

## to atom

@digest(form=form)
def set_coordinates_to_atom(item, indices='all', value=None, skip_digestion=False):

    value = puw.convert(value[0], to_unit='nanometers', to_form='openmm.unit')

    if is_all(indices):
        item.setPositions(value)
    else:
        positions = item.getPositions(asNumpy=True)
        positions[indices,:]=value
        item.setPositions(positions)

    pass

###
### System
###

@digest(form=form)
def set_coordinates_to_system(item, value=None, skip_digestion=False):

    return set_coordinates_to_atom(item, indices='all', value=value)

