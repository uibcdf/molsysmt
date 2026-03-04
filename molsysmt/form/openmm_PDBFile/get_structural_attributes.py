from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import types
import os

form='openmm.PDBFile'

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    from openmm.app import PDBFile
    import numpy as np

    if isinstance(item, (str, os.PathLike)):
        item = PDBFile(str(item))
    elif str(type(item)).endswith("PDBFileHandler'>"):
        item = PDBFile(item.file.name)

    tmp_positions = item.getPositions()
    tmp_positions = np.array(puw.get_value(tmp_positions, to_unit='nanometers'))
    
    if not is_all(indices):
        tmp_positions = tmp_positions[indices,:]

    output = np.zeros([1, tmp_positions.shape[0], 3])
    output[0,:,:] = tmp_positions
    output = output * puw.unit('nanometers')

    return output

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    from openmm.app import PDBFile
    import numpy as np

    if isinstance(item, (str, os.PathLike)):
        item = PDBFile(str(item))
    elif str(type(item)).endswith("PDBFileHandler'>"):
        item = PDBFile(item.file.name)

    tmp_box = item.getTopology().getPeriodicBoxVectors()
    if tmp_box is not None:
        tmp_box = np.array(puw.get_value(tmp_box, to_unit='nanometers'))
        output = np.zeros([1, 3, 3])
        output[0,:,:] = tmp_box
        output = output * puw.unit('nanometers')
        return output
    return None

@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):
    return None

@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):
    return None

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):
    return 1

# List of functions to be imported
import types
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
