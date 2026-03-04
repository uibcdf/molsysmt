from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import types

form='mdtraj.Trajectory'

## From atom

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    coordinates=item.xyz

    if not is_all(structure_indices):
        coordinates=coordinates[structure_indices,:,:]
    if not is_all(indices):
        coordinates=coordinates[:,indices,:]

    coordinates = coordinates*puw.unit('nanometer')

    return coordinates


## From system

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):
        return item.n_frames
    else:
        return len(structure_indices)

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    output = None

    if item.unitcell_vectors is not None:

        output = item.unitcell_vectors * puw.unit('nanometers')
        output = puw.standardize(output)

    return output

@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    if item.time is not None:
        output = item.time * puw.unit('picoseconds')
        if not is_all(structure_indices):
            output = output[structure_indices]
        return puw.standardize(output)
    return None

@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    return None

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
