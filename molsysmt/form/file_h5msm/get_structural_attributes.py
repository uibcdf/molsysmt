from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
import numpy as np
import types

form = 'file:h5msm'


#######################################################################
#                 To be customized for each form                      #
#######################################################################


# From atom


@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    """
    Getting coordinates from atom in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_coordinates_from_atom as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output

@arg_digest(form=form)
def get_velocities_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    """
    Getting velocities from atom in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_velocities_from_atom as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output

@arg_digest(form=form)
def get_occupancy_from_atom (item, indices='all', structure_indices='all', skip_digestion=False):

    """
    Getting occupancy from atom in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_occupancy_from_atom as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output

@arg_digest(form=form)
def get_alternate_location_from_atom (item, indices='all', structure_indices='all', skip_digestion=False):

    """
    Getting alternate location from atom in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_alternate_location_from_atom as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output

@arg_digest(form=form)
def get_b_factor_from_atom (item, indices='all', structure_indices='all', skip_digestion=False):

    """
    Getting b factor from atom in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_b_factor_from_atom as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output


# From system


@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting coordinates from system in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_coordinates_from_system as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output

@arg_digest(form=form)
def get_velocities_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting velocities from system in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_velocities_from_system as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting box from system in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_box_from_system as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output

@arg_digest(form=form)
def get_box_shape_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting box shape from system in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_box_shape_from_system as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output

@arg_digest(form=form)
def get_box_lengths_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting box lengths from system in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_box_lengths_from_system as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output

@arg_digest(form=form)
def get_box_angles_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting box angles from system in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_box_angles_from_system as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output

@arg_digest(form=form)
def get_box_volume_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting box volume from system in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_box_volume_from_system as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output

@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting time from system in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_time_from_system as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output


@arg_digest(form=form)
def get_temperature_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting temperature from system in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_temperature_from_system as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()
    return output


@arg_digest(form=form)
def get_potential_energy_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting potential energy from system in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_potential_energy_from_system as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()
    return output


@arg_digest(form=form)
def get_kinetic_energy_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting kinetic energy from system in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_kinetic_energy_from_system as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()
    return output


@arg_digest(form=form)
def get_total_energy_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting total energy from system in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_total_energy_from_system as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()
    return output


@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting structure id from system in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_structure_id_from_system as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()
    return output


@arg_digest(form=form)
def get_structure_chemical_state_index_from_system(
    item, structure_indices='all', skip_digestion=False
):
    """
    Getting structure chemical state index from system in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_structure_chemical_state_index_from_system as aux_get,
    )

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(
        tmp_item, structure_indices=structure_indices, skip_digestion=True
    )
    tmp_item.close()
    return output

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting n structures from system in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_n_structures_from_system as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()
    return output

@arg_digest(form=form)
def get_occupancy_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting occupancy from system in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_occupancy_from_system as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()
    return output

@arg_digest(form=form)
def get_b_factor_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting b factor from system in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_b_factor_from_system as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()
    return output

@arg_digest(form=form)
def get_alternate_location_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting alternate location from system in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
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
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_alternate_location_from_system as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()
    return output

@arg_digest(form=form)
def get_bioassembly_from_system(item, skip_digestion=False):

    """
    Getting bioassembly from system in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_bioassembly_from_system as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)
    tmp_item.close()
    return output

@arg_digest(form=form)
def get_n_bioassemblies_from_system(item, skip_digestion=False):

    """
    Getting n bioassemblies from system in form file:h5msm.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_n_bioassemblies_from_system as aux_get

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)
    tmp_item.close()
    return output


# List of functions to be imported

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
