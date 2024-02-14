from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
from molsysmt._private.get_topological_attributes import _auxiliary_getter
import types
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError

form='openmm.Topology'


#######################################################################
#                 To be customized for each form                      #
#######################################################################

## From atom

@digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    box = item.getPeriodicBoxVectors()

    output = None

    if box is not None:
        unit = puw.get_unit(box)
        box = np.array(puw.get_value(box))
        box = box.reshape(1, box.shape[0], box.shape[1])
        box = box * unit
        output = puw.standardize(box)

    return output

@digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    return None

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    return None


# List of functions to be imported


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]

