#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.smonitor import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
import types

form='string:pdb_id'


## From atom

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    """
    Getting coordinates from atom in form string:pdb_id.

    Parameters
    ----------
    item : string:pdb_id
        Source item in string:pdb_id form.
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
    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys import get_coordinates_from_atom as aux_get

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_occupancy_from_atom (item, indices='all', structure_indices='all', skip_digestion=False):

    """
    Getting occupancy from atom in form string:pdb_id.

    Parameters
    ----------
    item : string:pdb_id
        Source item in string:pdb_id form.
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
    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys import get_occupancy_from_atom as aux_get

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices='all', skip_digestion=True)

    return output

@arg_digest(form=form)
def get_alternate_location_from_atom (item, indices='all', structure_indices='all', skip_digestion=False):

    """
    Getting alternate location from atom in form string:pdb_id.

    Parameters
    ----------
    item : string:pdb_id
        Source item in string:pdb_id form.
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
    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys import get_alternate_location_from_atom as aux_get

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices='all', skip_digestion=True)

    return output

@arg_digest(form=form)
def get_b_factor_from_atom (item, indices='all', structure_indices='all', skip_digestion=False):

    """
    Getting b factor from atom in form string:pdb_id.

    Parameters
    ----------
    item : string:pdb_id
        Source item in string:pdb_id form.
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
    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys import get_b_factor_from_atom as aux_get

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices='all', skip_digestion=True)

    return output

@arg_digest(form=form)
def get_formal_charge_from_atom (item, indices='all', skip_digestion=False):

    """
    Getting formal charge from atom in form string:pdb_id.

    Parameters
    ----------
    item : string:pdb_id
        Source item in string:pdb_id form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys import get_formal_charge_from_atom as aux_get

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_partial_charge_from_atom (item, indices='all', skip_digestion=False):

    """
    Getting partial charge from atom in form string:pdb_id.

    Parameters
    ----------
    item : string:pdb_id
        Source item in string:pdb_id form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys import get_partial_charge_from_atom as aux_get

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From system

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting n structures from system in form string:pdb_id.

    Parameters
    ----------
    item : string:pdb_id
        Source item in string:pdb_id form.
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
    if is_all(structure_indices):

        from .to_molsysmt_MolSys import to_molsysmt_MolSys
        from molsysmt.form.molsysmt_MolSys import get_n_structures_from_system as aux_get

        tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
        output = aux_get(tmp_item, skip_digestion=True)

    else:

        output = len(structure_indices)

    return output

@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting coordinates from system in form string:pdb_id.

    Parameters
    ----------
    item : string:pdb_id
        Source item in string:pdb_id form.
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
    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys import get_coordinates_from_system as aux_get

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting box from system in form string:pdb_id.

    Parameters
    ----------
    item : string:pdb_id
        Source item in string:pdb_id form.
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
    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys import get_box_from_system as aux_get

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting time from system in form string:pdb_id.

    Parameters
    ----------
    item : string:pdb_id
        Source item in string:pdb_id form.
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
    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys import get_time_from_system as aux_get

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    """
    Getting structure id from system in form string:pdb_id.

    Parameters
    ----------
    item : string:pdb_id
        Source item in string:pdb_id form.
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
    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys import get_structure_id_from_system as aux_get

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_bioassembly_from_system(item, skip_digestion=False):

    """
    Getting bioassembly from system in form string:pdb_id.

    Parameters
    ----------
    item : string:pdb_id
        Source item in string:pdb_id form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys import get_bioassembly_from_system as aux_get

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_n_bioassemblies_from_system(item, skip_digestion=False):

    """
    Getting n bioassemblies from system in form string:pdb_id.

    Parameters
    ----------
    item : string:pdb_id
        Source item in string:pdb_id form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys import get_n_bioassemblies_from_system as aux_get

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_alternate_location_from_system (item, structure_indices='all', skip_digestion=False):

    """
    Getting alternate location from system in form string:pdb_id.

    Parameters
    ----------
    item : string:pdb_id
        Source item in string:pdb_id form.
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
    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys import get_alternate_location_from_system as aux_get

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)

    return output


# List of functions to be imported

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
