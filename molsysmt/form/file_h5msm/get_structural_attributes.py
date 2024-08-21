from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np
import types

form = 'file:h5msm'


#######################################################################
#                 To be customized for each form                      #
#######################################################################


# From atom


@digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    from . import to_molsysmt_H5MSMFileHandler
    from ..molsysmt_H5MSMFileHandler import get_coordinates_from_atom as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output

@digest(form=form)
def get_velocities_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    from . import to_molsysmt_H5MSMFileHandler
    from ..molsysmt_H5MSMFileHandler import get_velocities_from_atom as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output

@digest(form=form)
def get_occupancy_from_atom (item, indices='all', structure_indices='all', skip_digestion=False):

    from . import to_molsysmt_H5MSMFileHandler
    from ..molsysmt_H5MSMFileHandler import get_occupancy_from_atom as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output

@digest(form=form)
def get_alternate_location_from_atom (item, indices='all', structure_indices='all', skip_digestion=False):

    from . import to_molsysmt_H5MSMFileHandler
    from ..molsysmt_H5MSMFileHandler import get_alternate_location_from_atom as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output

@digest(form=form)
def get_b_factor_from_atom (item, indices='all', structure_indices='all', skip_digestion=False):

    from . import to_molsysmt_H5MSMFileHandler
    from ..molsysmt_H5MSMFileHandler import get_b_factor_from_atom as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output


# From system


@digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):

    from ..molsysmt_Structures import get_coordinates_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@digest(form=form)
def get_velocities_from_system(item, structure_indices='all', skip_digestion=False):

    from ..molsysmt_Structures import get_velocities_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    from ..molsysmt_Structures import get_box_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@digest(form=form)
def get_box_shape_from_system(item, structure_indices='all', skip_digestion=False):

    from ..molsysmt_Structures import get_box_shape_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@digest(form=form)
def get_box_lengths_from_system(item, structure_indices='all', skip_digestion=False):

    from ..molsysmt_Structures import get_box_lengths_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@digest(form=form)
def get_box_angles_from_system(item, structure_indices='all', skip_digestion=False):

    from ..molsysmt_Structures import get_box_angles_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@digest(form=form)
def get_box_volume_from_system(item, structure_indices='all', skip_digestion=False):

    from ..molsysmt_Structures import get_box_volume_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    from ..molsysmt_Structures import get_time_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    from ..molsysmt_Structures import get_structure_id_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    from ..molsysmt_Structures import get_n_structures_from_system as aux_get
    return aux_get(item.structures, structure_indices='all', skip_digestion=True)

@digest(form=form)
def get_occupancy_from_system(item, structure_indices='all', skip_digestion=False):

    from ..molsysmt_Structures import get_occupancy_from_system as aux_get
    return aux_get(item.structures, structure_indices='all', skip_digestion=True)

@digest(form=form)
def get_b_factor_from_system(item, structure_indices='all', skip_digestion=False):

    from ..molsysmt_Structures import get_b_factor_from_system as aux_get
    return aux_get(item.structures, structure_indices='all', skip_digestion=True)

@digest(form=form)
def get_alternate_location_from_system(item, structure_indices='all', skip_digestion=False):

    from ..molsysmt_Structures import get_alternate_location_from_system as aux_get
    return aux_get(item.structures, structure_indices='all', skip_digestion=True)

@digest(form=form)
def get_bioassembly_from_system(item, skip_digestion=False):

    from ..molsysmt_Structures import get_bioassembly_from_system as aux_get
    return aux_get(item.structures, skip_digestion=True)

@digest(form=form)
def get_n_bioassemblies_from_system(item, skip_digestion=False):

    from ..molsysmt_Structures import get_n_bioassemblies_from_system as aux_get
    return aux_get(item.structures, skip_digestion=True)


# List of functions to be imported


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]

