from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
import numpy as np
import types

form = 'molsysmt.MolSys'


#######################################################################
#                 To be customized for each form                      #
#######################################################################


# From atom


@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    """
    Getting coordinates from atom in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_coordinates_from_atom as aux_get
    return aux_get(item.structures, indices=indices, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_velocities_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    """
    Getting velocities from atom in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_velocities_from_atom as aux_get
    return aux_get(item.structures, indices=indices, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_occupancy_from_atom (item, indices='all', structure_indices='all', skip_digestion=False):

    """
    Getting occupancy from atom in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_occupancy_from_atom as aux_get
    return aux_get(item.structures, indices=indices, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_alternate_location_from_atom (item, indices='all', structure_indices='all', skip_digestion=False):

    """
    Getting alternate location from atom in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_alternate_location_from_atom as aux_get
    return aux_get(item.structures, indices=indices, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_b_factor_from_atom (item, indices='all', structure_indices='all', skip_digestion=False):

    """
    Getting b factor from atom in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_b_factor_from_atom as aux_get
    return aux_get(item.structures, indices=indices, structure_indices=structure_indices, skip_digestion=True)


# From system


@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting coordinates from system in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_coordinates_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_velocities_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting velocities from system in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_velocities_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting box from system in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_box_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_box_shape_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting box shape from system in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_box_shape_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_box_lengths_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting box lengths from system in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_box_lengths_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_box_angles_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting box angles from system in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_box_angles_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_box_volume_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting box volume from system in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_box_volume_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting time from system in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_time_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_temperature_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting temperature from system in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_temperature_from_system as aux_get

    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_potential_energy_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting potential energy from system in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_potential_energy_from_system as aux_get

    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_kinetic_energy_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting kinetic energy from system in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_kinetic_energy_from_system as aux_get

    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_total_energy_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting total energy from system in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_total_energy_from_system as aux_get

    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting structure id from system in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_structure_id_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_structure_index_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting structure index from system in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_structure_index_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_structure_chemical_state_index_from_system(
    item, structure_indices='all', skip_digestion=False
):
    """
    Getting structure chemical state index from system in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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

    return item._get_structure_chemical_state_indices(
        structure_indices=structure_indices, resolved=True
    ).tolist()

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting n structures from system in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_n_structures_from_system as aux_get
    return aux_get(item.structures, structure_indices='all', skip_digestion=True)

@arg_digest(form=form)
def get_occupancy_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting occupancy from system in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_occupancy_from_system as aux_get
    return aux_get(item.structures, structure_indices='all', skip_digestion=True)

@arg_digest(form=form)
def get_b_factor_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting b factor from system in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_b_factor_from_system as aux_get
    return aux_get(item.structures, structure_indices='all', skip_digestion=True)

@arg_digest(form=form)
def get_alternate_location_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting alternate location from system in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    from molsysmt.form.molsysmt_Structures import get_alternate_location_from_system as aux_get
    return aux_get(item.structures, structure_indices='all', skip_digestion=True)

@arg_digest(form=form)
def get_bioassembly_from_system(item, skip_digestion=False):

    """
    Getting bioassembly from system in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_Structures import get_bioassembly_from_system as aux_get
    return aux_get(item.structures, skip_digestion=True)

@arg_digest(form=form)
def get_n_bioassemblies_from_system(item, skip_digestion=False):

    """
    Getting n bioassemblies from system in form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_Structures import get_n_bioassemblies_from_system as aux_get
    return aux_get(item.structures, skip_digestion=True)


# List of functions to be imported


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
