import types

from molsysmt._private.argdigest import arg_digest
from molsysmt.form._query_delegation import make_routed_getter as _make_routed_getter

from ._modular_query import route_getter as _route_getter

form = "file:h5msm"


#######################################################################
#                 To be customized for each form                      #
#######################################################################


# From atom


@arg_digest(form=form)
def get_coordinates_from_atom(
    item, indices="all", structure_indices="all", skip_digestion=False
):
    """
    Getting coordinates from atom in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_coordinates_from_atom as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(
        tmp_item,
        indices=indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    tmp_item.close()

    return output


@arg_digest(form=form)
def get_velocities_from_atom(
    item, indices="all", structure_indices="all", skip_digestion=False
):
    """
    Getting velocities from atom in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_velocities_from_atom as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(
        tmp_item,
        indices=indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    tmp_item.close()

    return output


@arg_digest(form=form)
def get_occupancy_from_atom(
    item, indices="all", structure_indices="all", skip_digestion=False
):
    """
    Getting occupancy from atom in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_occupancy_from_atom as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(
        tmp_item,
        indices=indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    tmp_item.close()

    return output


@arg_digest(form=form)
def get_alternate_location_from_atom(
    item, indices="all", structure_indices="all", skip_digestion=False
):
    """
    Getting alternate location from atom in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_alternate_location_from_atom as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(
        tmp_item,
        indices=indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    tmp_item.close()

    return output


@arg_digest(form=form)
def get_b_factor_from_atom(
    item, indices="all", structure_indices="all", skip_digestion=False
):
    """
    Getting b factor from atom in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_b_factor_from_atom as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(
        tmp_item,
        indices=indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    tmp_item.close()

    return output


# From system


@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting coordinates from system in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_coordinates_from_system as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output


@arg_digest(form=form)
def get_velocities_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting velocities from system in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_velocities_from_system as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output


@arg_digest(form=form)
def get_box_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting box from system in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_box_from_system as aux_get

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output


@arg_digest(form=form)
def get_box_shape_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting box shape from system in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_box_shape_from_system as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output


@arg_digest(form=form)
def get_box_lengths_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting box lengths from system in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_box_lengths_from_system as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output


@arg_digest(form=form)
def get_box_angles_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting box angles from system in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_box_angles_from_system as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output


@arg_digest(form=form)
def get_box_volume_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting box volume from system in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_box_volume_from_system as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output


@arg_digest(form=form)
def get_time_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting time from system in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import get_time_from_system as aux_get

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()

    return output


@arg_digest(form=form)
def get_temperature_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting temperature from system in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_temperature_from_system as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()
    return output


@arg_digest(form=form)
def get_potential_energy_from_system(
    item, structure_indices="all", skip_digestion=False
):
    """
    Getting potential energy from system in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_potential_energy_from_system as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()
    return output


@arg_digest(form=form)
def get_kinetic_energy_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting kinetic energy from system in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_kinetic_energy_from_system as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()
    return output


@arg_digest(form=form)
def get_total_energy_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting total energy from system in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_total_energy_from_system as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()
    return output


@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting structure id from system in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_structure_id_from_system as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()
    return output


@arg_digest(form=form)
def get_structure_chemical_state_index_from_system(
    item, structure_indices="all", skip_digestion=False
):
    """
    Getting structure chemical state index from system in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_structure_chemical_state_index_from_system as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()
    return output


@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting n structures from system in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_n_structures_from_system as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()
    return output


@arg_digest(form=form)
def get_structure_index_from_system(
    item, structure_indices="all", skip_digestion=False
):
    """Getting structure positions from a legacy H5MSM file.

    Parameters
    ----------
    item : str or pathlib.Path
        Path to a legacy H5MSM 0.3 or 0.4 file, opened read-only for this query.
    structure_indices : int, list, tuple, range, numpy.ndarray, str or None, default='all'
        Zero-based positions to return, preserving order and repetitions.
        'all' returns every written position; None returns None.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of int or None
        Requested dimensionless positions, independent of stored structure IDs.
        An empty selection returns an empty list.

    Raises
    ------
    ArgumentError
        If explicit positions are not a flat integer axis or are out of bounds.

    Notes
    -----
    Reads only metadata; coordinates and other dataset payloads stay on disk.
    The owned handler closes even when validation fails. Existing unit checks
    and the legacy deprecation warning remain active. No migration is performed.
    H5MSM 0.5 queries use the separate public modular reader.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_structure_index_from_system as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    with to_molsysmt_H5MSMFileHandler(item, skip_digestion=True) as handler:
        return aux_get(
            handler, structure_indices=structure_indices, skip_digestion=True
        )


@arg_digest(form=form)
def get_occupancy_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting occupancy from system in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_occupancy_from_system as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()
    return output


@arg_digest(form=form)
def get_b_factor_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting b factor from system in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_b_factor_from_system as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.close()
    return output


@arg_digest(form=form)
def get_alternate_location_from_system(
    item, structure_indices="all", skip_digestion=False
):
    """
    Getting alternate location from system in form file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_alternate_location_from_system as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

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
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_bioassembly_from_system as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

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
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler import (
        get_n_bioassemblies_from_system as aux_get,
    )

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    tmp_item = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)
    tmp_item.close()
    return output


# List of functions to be imported

__all__ = [
    name
    for name, obj in globals().items()
    if isinstance(obj, types.FunctionType) and name.startswith("get_")
]

for _name in __all__:
    globals()[_name] = _make_routed_getter(_name, globals()[_name], form, _route_getter)
del _name, _make_routed_getter, _route_getter
