#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.smonitor import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='openmm.GromacsGroFile'

def _get_positions_array(item, indices, structure_indices):
    """Return coordinates as numpy array shape (n_frames, n_atoms, 3) in nm."""
    n_frames = item.getNumFrames()
    frame_list = list(range(n_frames)) if is_all(structure_indices) else list(structure_indices)

    frames_data = []
    for frame in frame_list:
        pos = item.getPositions(asNumpy=True, frame=frame)
        pos_array = np.array(puw.get_value(pos, to_unit='nanometers'))
        if not is_all(indices):
            pos_array = pos_array[indices, :]
        frames_data.append(pos_array)

    return np.array(frames_data)

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    output = _get_positions_array(item, indices, structure_indices) * puw.unit('nanometer')
    return output

@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):

    output = _get_positions_array(item, 'all', structure_indices) * puw.unit('nanometer')
    return output

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    n_frames = item.getNumFrames()
    frame_list = list(range(n_frames)) if is_all(structure_indices) else list(structure_indices)

    frames_data = []
    for frame in frame_list:
        vecs = item.getPeriodicBoxVectors(frame=frame)
        if vecs is None:
            return None
        box_array = np.array(puw.get_value(vecs, to_unit='nanometers'))
        frames_data.append(box_array)

    output = np.array(frames_data) * puw.unit('nanometer')
    return output

@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):
    return None

@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):
    return None

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):
        return item.getNumFrames()
    else:
        return len(structure_indices)

# List of functions to be imported
import types
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
