from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import types

form='openmm.AmberInpcrdFile'

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    # OpenMM returns positions as a list of Vec3 with units
    tmp_positions = item.getPositions()
    # Convert to pure numpy array in nanometers
    tmp_positions = puw.get_value(tmp_positions, to_unit='nanometers')
    tmp_positions = np.array(tmp_positions)
    
    if not is_all(indices):
        tmp_positions = tmp_positions[indices,:]

    output = np.zeros([1, tmp_positions.shape[0], 3])
    output[0,:,:] = tmp_positions
    output = output * puw.unit('nanometers')

    return output

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    tmp_box = item.getBoxVectors()
    if tmp_box is not None:
        tmp_box = puw.get_value(tmp_box, to_unit='nanometers')
        tmp_box = np.array(tmp_box)
        output = np.zeros([1, 3, 3])
        output[0,:,:] = tmp_box
        output = output * puw.unit('nanometers')
        return output
    return None

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):
    return 1

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
