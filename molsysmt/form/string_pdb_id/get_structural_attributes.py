#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
import types

form='string:pdb_id'


## From atom

@digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import get_coordinates_from_atom as aux_get

    tmp_item = to_mmtf_MMTFDecoder(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)

    return output

@digest(form=form)
def get_occupancy_from_atom (item, indices='all', structure_indices='all', skip_digestion=False):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import get_occupancy_from_atom as aux_get

    tmp_item = to_mmtf_MMTFDecoder(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices='all', skip_digestion=True)

    return output

@digest(form=form)
def get_alternate_location_from_atom (item, indices='all', structure_indices='all', skip_digestion=False):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import get_alternate_location_from_atom as aux_get

    tmp_item = to_mmtf_MMTFDecoder(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices='all', skip_digestion=True)

    return output

@digest(form=form)
def get_b_factor_from_atom (item, indices='all', structure_indices='all', skip_digestion=False):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import get_b_factor_from_atom as aux_get

    tmp_item = to_mmtf_MMTFDecoder(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices='all', skip_digestion=True)

    return output

@digest(form=form)
def get_formal_charge_from_atom (item, indices='all', skip_digestion=False):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import get_formal_charge_from_atom as aux_get

    tmp_item = to_mmtf_MMTFDecoder(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_partial_charge_from_atom (item, indices='all', skip_digestion=False):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import get_partial_charge_from_atom as aux_get

    tmp_item = to_mmtf_MMTFDecoder(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From system

@digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):

        from . import to_mmtf_MMTFDecoder
        from ..mmtf_MMTFDecoder import get_n_structures_from_system as aux_get

        tmp_item = to_mmtf_MMTFDecoder(item, skip_digestion=True)
        output = aux_get(tmp_item, skip_digestion=True)

    else:

        output = len(structure_indices)

    return output

@digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import get_coordinates_from_system as aux_get

    tmp_item = to_mmtf_MMTFDecoder(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)

    return output

@digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import get_box_from_system as aux_get

    tmp_item = to_mmtf_MMTFDecoder(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)

    return output

@digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import get_time_from_system as aux_get

    tmp_item = to_mmtf_MMTFDecoder(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)

    return output

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import get_structure_id_from_system as aux_get

    tmp_item = to_mmtf_MMTFDecoder(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)

    return output

@digest(form=form)
def get_bioassembly_from_system(item, skip_digestion=False):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import get_bioassembly_from_system as aux_get

    tmp_item = to_mmtf_MMTFDecoder(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output

@digest(form=form)
def get_n_bioassemblies_from_system(item, skip_digestion=False):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import get_n_bioassemblies_from_system as aux_get

    tmp_item = to_mmtf_MMTFDecoder(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


# List of functions to be imported

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
