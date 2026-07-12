from molsysmt._private.arg_digestion import arg_digest
import types

form='file:inpcrd'

# atom

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_coordinates_from_atom as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_velocities_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_velocities_from_atom as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)


# system

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_n_structures_from_system as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):

    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_coordinates_from_system as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_velocities_from_system(item, structure_indices='all', skip_digestion=False):

    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_velocities_from_system as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_box_from_system as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_box_shape_from_system(item, structure_indices='all', skip_digestion=False):

    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_box_shape_from_system as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_box_lengths_from_system(item, structure_indices='all', skip_digestion=False):

    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_box_lengths_from_system as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_box_angles_from_system(item, structure_indices='all', skip_digestion=False):

    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_box_angles_from_system as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_box_volume_from_system(item, structure_indices='all', skip_digestion=False):

    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_box_volume_from_system as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_structure_id_from_system as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)


# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
