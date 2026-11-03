"""Assign declared typed fields through the canonical chemical mutation boundary."""

from molsysmt._private.argdigest import arg_digest
from molsysmt.native._chemical_dict_assignments import assign as _assign

form = "molsysmt.ChemicalStatesDict"


@arg_digest(form=form)
def set_formal_charge_to_atom(item, indices="all", value=None, skip_digestion=False):
    """Setting integer formal charges in elementary-charge units.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_formal_charge_to_atom", indices, value)


@arg_digest(form=form)
def set_atom_is_aromatic_to_atom(item, indices="all", value=None, skip_digestion=False):
    """Setting declared atom aromaticity.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_atom_is_aromatic_to_atom", indices, value)


@arg_digest(form=form)
def set_n_unpaired_electrons_to_atom(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting declared unpaired-electron counts.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_n_unpaired_electrons_to_atom", indices, value)


@arg_digest(form=form)
def set_n_implicit_hydrogens_to_atom(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting declared implicit-hydrogen counts.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_n_implicit_hydrogens_to_atom", indices, value)


@arg_digest(form=form)
def set_n_explicit_hydrogens_to_atom(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting declared explicit-hydrogen counts.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_n_explicit_hydrogens_to_atom", indices, value)


@arg_digest(form=form)
def set_allows_implicit_hydrogens_to_atom(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting permission for implicit hydrogens.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_allows_implicit_hydrogens_to_atom", indices, value)


@arg_digest(form=form)
def set_atom_stereochemistry_to_atom(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting declared atom stereochemistry.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_atom_stereochemistry_to_atom", indices, value)


@arg_digest(form=form)
def set_bond_id_to_bond(item, indices="all", value=None, skip_digestion=False):
    """Setting string labels on stored bond positions.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_bond_id_to_bond", indices, value)


@arg_digest(form=form)
def set_bond_order_to_bond(item, indices="all", value=None, skip_digestion=False):
    """Setting integer orders of stored bonds.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_bond_order_to_bond", indices, value)


@arg_digest(form=form)
def set_fractional_bond_order_to_bond(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting dimensionless fractional bond orders.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_fractional_bond_order_to_bond", indices, value)


@arg_digest(form=form)
def set_bond_type_to_bond(item, indices="all", value=None, skip_digestion=False):
    """Setting declared chemical bond types.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_bond_type_to_bond", indices, value)


@arg_digest(form=form)
def set_bond_is_aromatic_to_bond(item, indices="all", value=None, skip_digestion=False):
    """Setting declared bond aromaticity.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_bond_is_aromatic_to_bond", indices, value)


@arg_digest(form=form)
def set_bond_is_conjugated_to_bond(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting declared bond conjugation.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_bond_is_conjugated_to_bond", indices, value)


@arg_digest(form=form)
def set_bond_stereochemistry_to_bond(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting declared bond stereochemistry.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_bond_stereochemistry_to_bond", indices, value)


@arg_digest(form=form)
def set_bond_stereo_atom_indices_to_bond(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting both stereo atom references of stored bonds.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_bond_stereo_atom_indices_to_bond", indices, value)


@arg_digest(form=form)
def set_bond_donor_atom_index_to_bond(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting directed-bond donor atom references.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_bond_donor_atom_index_to_bond", indices, value)


@arg_digest(form=form)
def set_bond_acceptor_atom_index_to_bond(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting directed-bond acceptor atom references.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_bond_acceptor_atom_index_to_bond", indices, value)


@arg_digest(form=form)
def set_bond_joins_components_to_bond(
    item, indices="all", value=None, skip_digestion=False
):
    """Setting declared bond participation in connectivity.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_bond_joins_components_to_bond", indices, value)


@arg_digest(form=form)
def set_bond_evidence_to_bond(item, indices="all", value=None, skip_digestion=False):
    """Setting evidence declarations on stored bonds.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_bond_evidence_to_bond", indices, value)


@arg_digest(form=form)
def set_component_index_to_atom(item, indices="all", value=None, skip_digestion=False):
    """Declaring atom membership in existing state-local components.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_component_index_to_atom", indices, value)


@arg_digest(form=form)
def set_component_id_to_component(
    item, indices="all", value=None, skip_digestion=False
):
    """Assigning string component labels on the selected chemical state.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_component_id_to_component", indices, value)


@arg_digest(form=form)
def set_component_id_to_atom(item, indices="all", value=None, skip_digestion=False):
    """Assigning string component labels on the selected chemical state.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_component_id_to_atom", indices, value)


@arg_digest(form=form)
def set_component_name_to_component(
    item, indices="all", value=None, skip_digestion=False
):
    """Assigning component names on the selected chemical state.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_component_name_to_component", indices, value)


@arg_digest(form=form)
def set_component_name_to_atom(item, indices="all", value=None, skip_digestion=False):
    """Assigning component names on the selected chemical state.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_component_name_to_atom", indices, value)


@arg_digest(form=form)
def set_component_type_to_component(
    item, indices="all", value=None, skip_digestion=False
):
    """Assigning component type labels on the selected chemical state.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_component_type_to_component", indices, value)


@arg_digest(form=form)
def set_component_type_to_atom(item, indices="all", value=None, skip_digestion=False):
    """Assigning component type labels on the selected chemical state.

    Parameters
    ----------
    item : molsysmt.ChemicalStatesDict
        Typed payload with an unambiguous active or reference state.
    indices : 'all' or array-like of int, default='all'
        Unique positions in the selected state's atom, bond or component axis.
    value : scalar or array-like, default=None
        Declared field values under the corresponding ChemicalStates setter's
        dtype, nullability, units and broadcasting contract.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Notes
    -----
    Only the selected state is materialized for controlled editing. Its replacement
    is encoded before publication; failure preserves the complete original payload.
    Other state records, collection order and reference remain unchanged. No graph,
    state or property is perceived. Several attributes are separate assignments.

    .. versionadded:: 1.0.0
    """
    _assign(item, "set_component_type_to_atom", indices, value)


__all__ = [name for name in globals() if name.startswith("set_")]
