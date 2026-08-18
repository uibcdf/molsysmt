from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import StructuralInconsistencyError, InternalAlgorithmError, FormatError
from molsysmt._private.variables import is_all

form = "molsysmt.MolSysBuilder"


@arg_digest(form=form)
def set_atom_name_to_atom(item, indices="all", value=None, skip_digestion=False):
    """
    Setting atom name to atom on form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    from ..molsysmt_Topology.set import set_atom_name_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_atom_id_to_atom(item, indices="all", value=None, skip_digestion=False):
    """
    Setting atom id to atom on form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    from ..molsysmt_Topology.set import set_atom_id_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_atom_type_to_atom(item, indices="all", value=None, skip_digestion=False):
    """
    Setting atom type to atom on form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    from ..molsysmt_Topology.set import set_atom_type_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_group_name_to_group(item, indices="all", value=None, skip_digestion=False):
    """
    Setting group name to group on form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    from ..molsysmt_Topology.set import set_group_name_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_group_id_to_group(item, indices="all", value=None, skip_digestion=False):
    """
    Setting group id to group on form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    from ..molsysmt_Topology.set import set_group_id_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_group_type_to_group(item, indices="all", value=None, skip_digestion=False):
    """
    Setting group type to group on form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    from ..molsysmt_Topology.set import set_group_type_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_chain_name_to_chain(item, indices="all", value=None, skip_digestion=False):
    """
    Setting chain name to chain on form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    from ..molsysmt_Topology.set import set_chain_name_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_chain_id_to_chain(item, indices="all", value=None, skip_digestion=False):
    """
    Setting chain id to chain on form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    from ..molsysmt_Topology.set import set_chain_id_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_chain_type_to_chain(item, indices="all", value=None, skip_digestion=False):
    """
    Setting chain type to chain on form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    from ..molsysmt_Topology.set import set_chain_type_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_molecule_name_to_molecule(item, indices="all", value=None, skip_digestion=False):
    """
    Setting molecule name to molecule on form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    from ..molsysmt_Topology.set import set_molecule_name_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_molecule_id_to_molecule(item, indices="all", value=None, skip_digestion=False):
    """
    Setting molecule id to molecule on form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    from ..molsysmt_Topology.set import set_molecule_id_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_molecule_type_to_molecule(item, indices="all", value=None, skip_digestion=False):
    """
    Setting molecule type to molecule on form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    from ..molsysmt_Topology.set import set_molecule_type_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_entity_name_to_entity(item, indices="all", value=None, skip_digestion=False):
    """
    Setting entity name to entity on form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    from ..molsysmt_Topology.set import set_entity_name_to_entity as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_entity_id_to_entity(item, indices="all", value=None, skip_digestion=False):
    """
    Setting entity id to entity on form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    from ..molsysmt_Topology.set import set_entity_id_to_entity as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_entity_type_to_entity(item, indices="all", value=None, skip_digestion=False):
    """
    Setting entity type to entity on form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    from ..molsysmt_Topology.set import set_entity_type_to_entity as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_coordinates_to_atom(item, indices="all", structure_indices="all", value=None, skip_digestion=False):
    """
    Setting coordinates to atom on form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    from ..molsysmt_Structures.set import set_coordinates_to_atom as aux_set

    if is_all(indices):
        n_atoms = item.topology.n_atoms
        if n_atoms != value.shape[1]:
            raise StructuralInconsistencyError("Coordinates mismatch with atoms count", caller="molsysmt.form.molsysmt_MolSysBuilder.set")

    return aux_set(
        item.structures,
        indices=indices,
        structure_indices=structure_indices,
        value=value,
        skip_digestion=True,
    )


@arg_digest(form=form)
def set_coordinates_to_system(item, indices="all", structure_indices="all", value=None, skip_digestion=False):
    """
    Setting coordinates to system on form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    from ..molsysmt_Structures.set import set_coordinates_to_system as aux_set

    return aux_set(
        item.structures,
        indices=indices,
        structure_indices=structure_indices,
        value=value,
        skip_digestion=True,
    )


@arg_digest(form=form)
def set_box_to_system(item, structure_indices="all", value=None, skip_digestion=False):
    """
    Setting box to system on form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    from ..molsysmt_Structures.set import set_box_to_system as aux_set

    return aux_set(item.structures, structure_indices=structure_indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_time_to_system(item, structure_indices="all", value=None, skip_digestion=False):
    """
    Setting time to system on form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    from ..molsysmt_Structures.set import set_time_to_system as aux_set

    return aux_set(item.structures, structure_indices=structure_indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_structure_id_to_system(item, structure_indices="all", value=None, skip_digestion=False):
    """
    Setting structure id to system on form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    from ..molsysmt_Structures.set import set_structure_id_to_system as aux_set

    return aux_set(item.structures, structure_indices=structure_indices, value=value, skip_digestion=True)
