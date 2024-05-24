#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
import types

form='openmm.Modeller'


## From atom

@digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    unit = puw.get_unit(item.positions)
    coordinates = np.array(puw.get_value(item.positions))
    coordinates = coordinates.reshape(1, coordinates.shape[0], coordinates.shape[1])

    if not is_all(structure_indices):
        coordinates = coordinates[structure_indices,:,:]

    if not is_all(indices):
        coordinates = coordinates[:,indices,:]

    coordinates = coordinates * unit
    coordinates = puw.standardize(coordinates)

    return coordinates


## From system


@digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    return 1

@digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    from . import to_openmm_Topology
    from ..openmm_Topology import get_box_from_system as aux_get

    tmp_item = to_openmm_Topology(item, structure_indices=structure_indices, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output

@digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    return None

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    return None


# List of functions to be imported

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
