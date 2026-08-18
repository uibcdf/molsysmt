from molsysmt._private.argdigest import arg_digest
import types

form='file:inpcrd'

# atom

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    """
    Getting coordinates from atom in form file:inpcrd.

    Parameters
    ----------
    item : file:inpcrd
        Source item in file:inpcrd form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_coordinates_from_atom as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_velocities_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    """
    Getting velocities from atom in form file:inpcrd.

    Parameters
    ----------
    item : file:inpcrd
        Source item in file:inpcrd form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_velocities_from_atom as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)


# system

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting n structures from system in form file:inpcrd.

    Parameters
    ----------
    item : file:inpcrd
        Source item in file:inpcrd form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_n_structures_from_system as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting coordinates from system in form file:inpcrd.

    Parameters
    ----------
    item : file:inpcrd
        Source item in file:inpcrd form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_coordinates_from_system as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_velocities_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting velocities from system in form file:inpcrd.

    Parameters
    ----------
    item : file:inpcrd
        Source item in file:inpcrd form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_velocities_from_system as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting box from system in form file:inpcrd.

    Parameters
    ----------
    item : file:inpcrd
        Source item in file:inpcrd form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_box_from_system as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_box_shape_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting box shape from system in form file:inpcrd.

    Parameters
    ----------
    item : file:inpcrd
        Source item in file:inpcrd form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_box_shape_from_system as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_box_lengths_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting box lengths from system in form file:inpcrd.

    Parameters
    ----------
    item : file:inpcrd
        Source item in file:inpcrd form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_box_lengths_from_system as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_box_angles_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting box angles from system in form file:inpcrd.

    Parameters
    ----------
    item : file:inpcrd
        Source item in file:inpcrd form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_box_angles_from_system as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_box_volume_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting box volume from system in form file:inpcrd.

    Parameters
    ----------
    item : file:inpcrd
        Source item in file:inpcrd form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_box_volume_from_system as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting structure id from system in form file:inpcrd.

    Parameters
    ----------
    item : file:inpcrd
        Source item in file:inpcrd form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.get_structural_attributes import get_structure_id_from_system as aux_get
    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    return aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)


# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
