from molsysmt._private.argdigest import arg_digest
import types

form='mdtraj.Trajectory'

## From atom

@arg_digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting atom id from atom in form mdtraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_atom_id_from_atom as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting atom name from atom in form mdtraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_atom_name_from_atom as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_atom_type_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting atom type from atom in form mdtraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_atom_type_from_atom as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_group_index_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting group index from atom in form mdtraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_group_index_from_atom as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_component_index_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting component index from atom in form mdtraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_component_index_from_atom as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_chain_index_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting chain index from atom in form mdtraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_chain_index_from_atom as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_molecule_index_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting molecule index from atom in form mdtraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_molecule_index_from_atom as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_entity_index_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting entity index from atom in form mdtraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_entity_index_from_atom as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting inner bonded atoms from atom in form mdtraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_inner_bonded_atoms_from_atom as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting n inner bonds from atom in form mdtraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_n_inner_bonds_from_atom as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

## From system

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    """
    Getting n atoms from system in form mdtraj.Trajectory.


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
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_n_atoms_from_system as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, skip_digestion=True)

@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):
    """
    Getting n groups from system in form mdtraj.Trajectory.


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
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_n_groups_from_system as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, skip_digestion=True)

@arg_digest(form=form)
def get_n_components_from_system(item, skip_digestion=False):
    """
    Getting n components from system in form mdtraj.Trajectory.


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
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_n_components_from_system as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, skip_digestion=True)

@arg_digest(form=form)
def get_n_chains_from_system(item, skip_digestion=False):
    """
    Getting n chains from system in form mdtraj.Trajectory.


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
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_n_chains_from_system as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, skip_digestion=True)

@arg_digest(form=form)
def get_n_molecules_from_system(item, skip_digestion=False):
    """
    Getting n molecules from system in form mdtraj.Trajectory.


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
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_n_molecules_from_system as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, skip_digestion=True)

@arg_digest(form=form)
def get_n_entities_from_system(item, skip_digestion=False):
    """
    Getting n entities from system in form mdtraj.Trajectory.


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
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_n_entities_from_system as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, skip_digestion=True)

@arg_digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):
    """
    Getting n bonds from system in form mdtraj.Trajectory.


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
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_n_bonds_from_system as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, skip_digestion=True)

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
